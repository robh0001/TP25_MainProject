"""
Family Plan Lambda Function

This AWS Lambda function builds a 4-week HealthyKids family plan for a saved
parent profile.

Main responsibilities:
- Handles GET and OPTIONS requests from API Gateway.
- Reads the username from the query string.
- Loads the saved parent profile from PostgreSQL/RDS.
- Loads nutrition, exercise, workout, and sleep plan data from database tables.
- Uses the parent profile to decide the family's main focus.
- Builds a structured 4-week plan with daily meals, movement, workouts, sleep tips, and time slots.
- Returns the plan as JSON for the Vue parent dashboard.

API route:
- GET /family-plan?username={username}

Required environment variables:
- DB_HOST
- DB_NAME
- DB_USER
- DB_PASSWORD

Optional environment variables:
- DB_PORT
- DB_SSL
"""

import os
import json
import decimal
import datetime
import traceback
from typing import Any, Dict, List, Optional

import pg8000.native


# Reused database connection for warm Lambda invocations.
_connection = None


# Shared CORS and JSON headers for all API responses.
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
}


# Standard day order used when building each weekly plan.
DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def lambda_handler(event, context):
    """
    Main Lambda entry point.

    Loads the parent profile and plan source tables, then assembles a
    frontend-ready 4-week family plan.
    """
    # Return early for browser CORS preflight requests.
    if is_options_request(event):
        return response(200, {"message": "CORS preflight OK"})

    try:
        # Read the username / family code from the query string.
        username = get_query_param(event, "username")

        if not username:
            return response(400, {
                "error": "username query parameter is required"
            })

        # Open or reuse a PostgreSQL/RDS connection.
        db = get_connection()

        # Load the saved parent profile.
        profile = fetch_parent_profile(db, username)

        if not profile:
            return response(404, {
                "error": "Parent profile not found",
                "username": username
            })

        # Convert quiz/profile data into planning context.
        context_data = build_query_context(profile)

        # Load source plan data from database tables.
        nutrition_rows = query_nutrition_plan(db)
        exercise_rows = query_exercise_plan(db)
        workout_rows = query_workout_plan(db)
        sleep_rows = query_sleep_plan(db)

        # Build the final 4-week family plan.
        plan = assemble_four_week_plan(
            profile=profile,
            context_data=context_data,
            nutrition_rows=nutrition_rows,
            exercise_rows=exercise_rows,
            workout_rows=workout_rows,
            sleep_rows=sleep_rows,
        )

        # Return the saved profile summary and generated plan to the dashboard.
        return response(200, {
            "username": profile["username"],
            "generatedAt": datetime.datetime.utcnow().isoformat() + "Z",
            "profile": {
                "username": profile["username"],
                "parentName": profile.get("parent_name"),
                "childName": profile.get("child_name"),
                "ageRange": profile.get("age_range"),
                "routineType": profile.get("routine_type"),
                "habits": safe_json_array(profile.get("habits")),
                "concerns": safe_json_array(profile.get("concerns")),
                "supportStyle": profile.get("support_style"),
                "mission": profile.get("mission"),
                "streakDays": profile.get("streak_days", 0),
            },
            "plan": plan,
        })

    except Exception as error:
        # Log detailed errors in CloudWatch for debugging.
        print("ERROR in getFamilyPlan Lambda")
        print(str(error))
        print(traceback.format_exc())

        return response(500, {
            "error": "Internal server error",
            "detail": str(error)
        })


# API Gateway helpers

def is_options_request(event: Dict[str, Any]) -> bool:
    """
    Checks whether the request is a CORS preflight OPTIONS request.

    Supports both REST API and HTTP API Gateway event formats.
    """
    method_v1 = event.get("httpMethod")
    method_v2 = event.get("requestContext", {}).get("http", {}).get("method")
    return method_v1 == "OPTIONS" or method_v2 == "OPTIONS"


def get_query_param(event: Dict[str, Any], key: str) -> Optional[str]:
    """
    Reads a query string value from the API Gateway event.
    """
    params = event.get("queryStringParameters") or {}
    return params.get(key)


def response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Builds a standard API Gateway JSON response.
    """
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body, default=json_default),
    }


def json_default(value):
    """
    Converts database/date values into JSON-safe values.
    """
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    return str(value)


# Database connection

def get_connection():
    """
    Creates or reuses a PostgreSQL/RDS database connection.

    Reusing the connection helps reduce overhead on warm Lambda invocations.
    """
    global _connection

    # Reuse the connection if it is still healthy.
    if _connection is not None:
        try:
            _connection.run("SELECT 1")
            return _connection
        except Exception:
            _connection = None

    # Read database settings from Lambda environment variables.
    host = os.environ["DB_HOST"]
    port = int(os.environ.get("DB_PORT", "5432"))
    database = os.environ["DB_NAME"]
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]

    use_ssl = os.environ.get("DB_SSL", "true").lower() == "true"

    # Create a new PostgreSQL/RDS connection.
    _connection = pg8000.native.Connection(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        ssl_context=True if use_ssl else None,
        timeout=10,
    )

    return _connection


# Profile query

def fetch_parent_profile(db, username: str) -> Optional[Dict[str, Any]]:
    """
    Loads a parent profile by username / family code.

    Returns None when no matching profile exists.
    """
    sql = """
        SELECT
            id,
            username,
            parent_name,
            child_name,
            age_range,
            routine_type,
            habits,
            concerns,
            struggle,
            confidence,
            support_style,
            recommendations,
            daily_plan,
            progress_items,
            next_action,
            mission,
            streak_days,
            created_at,
            updated_at
        FROM parent_profiles
        WHERE username = :username
        LIMIT 1
    """

    rows = db.run(sql, username=username)

    if not rows:
        return None

    # Column names are used to convert the returned row into a dictionary.
    columns = [
        "id",
        "username",
        "parent_name",
        "child_name",
        "age_range",
        "routine_type",
        "habits",
        "concerns",
        "struggle",
        "confidence",
        "support_style",
        "recommendations",
        "daily_plan",
        "progress_items",
        "next_action",
        "mission",
        "streak_days",
        "created_at",
        "updated_at",
    ]

    return dict(zip(columns, rows[0]))


# Plan table queries

def query_nutrition_plan(db) -> List[Dict[str, Any]]:
    """
    Loads nutrition plan rows ordered by week, day, and meal type.
    """
    sql = """
        SELECT
            week_number,
            day_number,
            meal_type,
            meal_name,
            description,
            calories,
            protein_g,
            carbohydrates_g,
            fat_g,
            fibre_g,
            sodium_mg,
            calcium_mg,
            iron_mg
        FROM nutrition_plan
        ORDER BY
            week_number,
            day_number,
            CASE meal_type
                WHEN 'Breakfast' THEN 1
                WHEN 'Lunch' THEN 2
                WHEN 'Dinner' THEN 3
                WHEN 'Snack' THEN 4
                ELSE 5
            END
    """

    rows = db.run(sql)

    columns = [
        "week_number",
        "day_number",
        "meal_type",
        "meal_name",
        "description",
        "calories",
        "protein_g",
        "carbohydrates_g",
        "fat_g",
        "fibre_g",
        "sodium_mg",
        "calcium_mg",
        "iron_mg",
    ]

    return [dict(zip(columns, row)) for row in rows]


def query_exercise_plan(db) -> List[Dict[str, Any]]:
    """
    Loads weekly letter-based exercise activities.
    """
    sql = """
        SELECT
            week_number,
            letter,
            exercise_name,
            description
        FROM exercise_plan
        ORDER BY week_number, letter
    """

    rows = db.run(sql)

    columns = [
        "week_number",
        "letter",
        "exercise_name",
        "description",
    ]

    return [dict(zip(columns, row)) for row in rows]


def query_workout_plan(db) -> List[Dict[str, Any]]:
    """
    Loads daily workout plan rows ordered by week, day, and database id.
    """
    sql = """
        SELECT
            id,
            week_number,
            day_number,
            workout_number,
            exercise_name,
            description
        FROM workout_plan
        ORDER BY week_number, day_number, id
    """

    rows = db.run(sql)

    columns = [
        "id",
        "week_number",
        "day_number",
        "workout_number",
        "exercise_name",
        "description",
    ]

    return [dict(zip(columns, row)) for row in rows]


def query_sleep_plan(db) -> List[Dict[str, Any]]:
    """
    Loads sleep plan rows ordered by week and weekday.
    """
    sql = """
        SELECT
            week_number,
            week_theme,
            day_name,
            daily_tip
        FROM sleep_plan
        ORDER BY
            week_number,
            CASE day_name
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
                ELSE 8
            END
    """

    rows = db.run(sql)

    columns = [
        "week_number",
        "week_theme",
        "day_name",
        "daily_tip",
    ]

    return [dict(zip(columns, row)) for row in rows]


# Quiz/profile logic

def build_query_context(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts parent quiz/profile answers into planning flags.

    These flags help the plan decide whether the family mainly needs support
    with sleep, nutrition, movement, routine, or a balanced mix.
    """
    habits = safe_json_array(profile.get("habits"))
    concerns = safe_json_array(profile.get("concerns"))

    primary_focus = "balanced"

    concerns_text = " ".join(concerns).lower()

    # Choose the strongest planning focus based on the parent's concerns.
    if "sleep" in concerns_text or "bedtime" in concerns_text:
        primary_focus = "sleep"
    elif "snack" in concerns_text or "nutrition" in concerns_text or "meal" in concerns_text:
        primary_focus = "nutrition"
    elif "active" in concerns_text or "movement" in concerns_text or "activity" in concerns_text:
        primary_focus = "movement"
    elif "routine" in concerns_text or "manage" in concerns_text:
        primary_focus = "routine"

    age_range = profile.get("age_range") or "8-10 years"

    # Map the selected age range into a simple age group.
    if age_range.startswith("5"):
        age_group = "young"
    elif age_range.startswith("11"):
        age_group = "older"
    else:
        age_group = "middle"

    # Detect families that may need a shorter, simpler daily plan.
    routine_type = profile.get("routine_type") or ""
    is_busy = "busy" in routine_type.lower() or "hard" in routine_type.lower()

    return {
        "primaryFocus": primary_focus,
        "ageGroup": age_group,
        "isBusy": is_busy,
        "wantsNutrition": (
            "Balanced meals" in habits or
            "Healthier snacks" in habits
        ),
        "wantsMovement": "Daily movement" in habits,
        "wantsSleep": "Sleep routine" in habits,
        "wantsScreens": "Screen time balance" in habits,
    }


def safe_json_array(value: Any) -> List[Any]:
    """
    Safely converts a database JSON value into a Python list.

    Returns an empty list if the value is missing, invalid, or not a list.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except Exception:
            return []

    return []


# Assemble final 4-week plan

def assemble_four_week_plan(
    profile: Dict[str, Any],
    context_data: Dict[str, Any],
    nutrition_rows: List[Dict[str, Any]],
    exercise_rows: List[Dict[str, Any]],
    workout_rows: List[Dict[str, Any]],
    sleep_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Builds the final 4-week plan from source table rows.

    Each week contains seven days, and each day includes nutrition, movement,
    workout, sleep, and dashboard time slot data.
    """
    # Build indexes so plan data can be looked up quickly by week/day.
    nutrition_index = build_nutrition_index(nutrition_rows)
    exercise_index = build_exercise_index(exercise_rows)
    workout_index = build_workout_index(workout_rows)
    sleep_index = build_sleep_index(sleep_rows)

    weeks = []

    # Build four weekly plan sections.
    for week_number in range(1, 5):
        sleep_week = sleep_index.get(week_number, {
            "theme": f"Week {week_number}",
            "days": {},
        })

        exercises_this_week = exercise_index.get(week_number, [])

        days = []

        # Build each day in Monday to Sunday order.
        for day_index, day_name in enumerate(DAY_NAMES):
            day_number = day_index + 1

            nutrition = nutrition_index.get(week_number, {}).get(day_number, {})

            # Rotate through the week's exercise list across the seven days.
            exercise = None
            if exercises_this_week:
                exercise = exercises_this_week[day_index % len(exercises_this_week)]

            workout_rows_for_day = workout_index.get(week_number, {}).get(day_number, [])

            workout = format_workout(workout_rows_for_day)

            sleep_tip = sleep_week.get("days", {}).get(day_name, "")

            # Build the dashboard's time-based task list for this day.
            time_slots = build_time_slots_from_db(
                day_name=day_name,
                day_number=day_number,
                week_number=week_number,
                nutrition=nutrition,
                exercise=exercise,
                workout=workout,
                sleep_tip=sleep_tip,
                context_data=context_data,
                profile=profile,
            )

            days.append({
                "dayNumber": day_number,
                "dayName": day_name,
                "nutrition": {
                    "breakfast": format_meal(nutrition.get("breakfast")),
                    "lunch": format_meal(nutrition.get("lunch")),
                    "dinner": format_meal(nutrition.get("dinner")),
                    "snack": format_meal(nutrition.get("snack")),
                },
                "exercise": format_exercise(exercise),
                "workout": workout,
                "sleep": {
                    "theme": sleep_week.get("theme"),
                    "tip": sleep_tip,
                },
                "timeSlots": time_slots,
            })

        weeks.append({
            "weekNumber": week_number,
            "theme": sleep_week.get("theme"),
            "days": days,
        })

    return {
        "weeks": weeks,
    }


def build_nutrition_index(rows: List[Dict[str, Any]]) -> Dict[int, Dict[int, Dict[str, Dict[str, Any]]]]:
    """
    Groups nutrition rows by week, day, and meal type.
    """
    index = {}

    for row in rows:
        week = int(row["week_number"])
        day = int(row["day_number"])
        meal = row["meal_type"].lower()

        index.setdefault(week, {})
        index[week].setdefault(day, {})
        index[week][day][meal] = row

    return index


def build_exercise_index(rows: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
    """
    Groups exercise rows by week.
    """
    index = {}

    for row in rows:
        week = int(row["week_number"])
        index.setdefault(week, [])
        index[week].append(row)

    return index


def build_workout_index(rows: List[Dict[str, Any]]) -> Dict[int, Dict[int, List[Dict[str, Any]]]]:
    """
    Groups workout rows by week and day.
    """
    index = {}

    for row in rows:
        week = int(row["week_number"])
        day = int(row["day_number"])

        index.setdefault(week, {})
        index[week].setdefault(day, [])
        index[week][day].append(row)

    return index


def build_sleep_index(rows: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    Groups sleep tips by week and day name.
    """
    index = {}

    for row in rows:
        week = int(row["week_number"])

        if week not in index:
            index[week] = {
                "theme": row["week_theme"],
                "days": {},
            }

        index[week]["days"][row["day_name"]] = row["daily_tip"]

    return index


# Format individual blocks

def format_meal(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Converts one nutrition database row into a frontend meal object.
    """
    if not row:
        return None

    return {
        "name": row.get("meal_name"),
        "description": row.get("description"),
        "calories": to_number(row.get("calories")),
        "protein_g": to_number(row.get("protein_g")),
        "carbs_g": to_number(row.get("carbohydrates_g")),
        "fat_g": to_number(row.get("fat_g")),
        "fibre_g": to_number(row.get("fibre_g")),
        "sodium_mg": to_number(row.get("sodium_mg")),
        "calcium_mg": to_number(row.get("calcium_mg")),
        "iron_mg": to_number(row.get("iron_mg")),
    }


def format_exercise(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Converts one exercise database row into a frontend exercise object.
    """
    if not row:
        return None

    return {
        "letter": row.get("letter"),
        "name": row.get("exercise_name"),
        "description": row.get("description"),
    }


def format_workout(rows: List[Dict[str, Any]]) -> Any:
    """
    Converts workout database rows into a frontend workout object or list.

    Rest days are returned as a single object. Normal workout days are returned
    as a list of activities.
    """
    if not rows:
        return []

    is_rest_day = any(row.get("exercise_name") == "Rest Day" for row in rows)

    if is_rest_day:
        first = rows[0]
        return {
            "isRestDay": True,
            "description": first.get("description", ""),
        }

    return [
        {
            "workoutNumber": row.get("workout_number"),
            "exerciseName": row.get("exercise_name"),
            "description": row.get("description"),
        }
        for row in rows
    ]


def to_number(value: Any) -> Optional[float]:
    """
    Converts database numeric values into Python numbers.

    Returns None if the value cannot be converted.
    """
    if value is None:
        return None

    if isinstance(value, decimal.Decimal):
        return float(value)

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return value

    try:
        return float(value)
    except Exception:
        return None


# Build dashboard time slots

def build_time_slots_from_db(
    day_name: str,
    day_number: int,
    week_number: int,
    nutrition: Dict[str, Any],
    exercise: Optional[Dict[str, Any]],
    workout: Any,
    sleep_tip: str,
    context_data: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Builds the daily timeline shown on the parent dashboard.

    The timeline combines meals, movement, workouts, rest days, and sleep tips
    into ordered task cards with fixed suggested times.
    """
    slots = []

    is_weekend = day_name in ["Saturday", "Sunday"]
    child_name = profile.get("child_name") or "your child"

    def slot_id(suffix: str) -> str:
        """
        Creates a stable frontend id for a daily timeline task.
        """
        return f"week-{week_number}-{day_name.lower()}-{suffix}"

    # Pull meal objects from the day's nutrition data.
    breakfast = nutrition.get("breakfast")
    lunch = nutrition.get("lunch")
    snack = nutrition.get("snack")
    dinner = nutrition.get("dinner")

    # Add breakfast if available.
    if breakfast:
        slots.append({
            "id": slot_id("breakfast"),
            "time": "8:30 am" if is_weekend else "7:00 am",
            "category": "nutrition",
            "categoryLabel": "Nutrition",
            "text": breakfast["meal_name"],
            "tip": breakfast["description"],
            "detail": f"{to_number(breakfast['calories'])} kcal",
            "done": False,
            "source": "nutrition_plan",
        })

    # Add weekday exercise activity if available.
    if exercise and not is_weekend:
        slots.append({
            "id": slot_id("exercise"),
            "time": "8:30 am",
            "category": "movement",
            "categoryLabel": "Movement",
            "text": f"{exercise['letter']} is for {exercise['exercise_name']}",
            "tip": exercise["description"],
            "detail": "Short kid-friendly movement activity",
            "done": False,
            "source": "exercise_plan",
        })

    # Add lunch if available.
    if lunch:
        slots.append({
            "id": slot_id("lunch"),
            "time": "12:30 pm" if is_weekend else "12:00 pm",
            "category": "nutrition",
            "categoryLabel": "Nutrition",
            "text": lunch["meal_name"],
            "tip": lunch["description"],
            "detail": f"{to_number(lunch['calories'])} kcal",
            "done": False,
            "source": "nutrition_plan",
        })

    # Add snack if available.
    if snack:
        slots.append({
            "id": slot_id("snack"),
            "time": "3:30 pm",
            "category": "nutrition",
            "categoryLabel": "Nutrition",
            "text": snack["meal_name"],
            "tip": snack["description"],
            "detail": f"{to_number(snack['calories'])} kcal",
            "done": False,
            "source": "nutrition_plan",
        })

    # Add workout block for normal workout days.
    if isinstance(workout, list) and len(workout) > 0:
        workout_names = ", ".join(
            item["exerciseName"] for item in workout[:3]
        )

        slots.append({
            "id": slot_id("workout"),
            "time": "10:30 am" if is_weekend else "5:00 pm",
            "category": "movement",
            "categoryLabel": "Movement",
            "text": f"Workout: {workout_names}",
            "tip": workout[0].get("description") or "Complete today's movement block at a comfortable pace.",
            "detail": f"{len(workout)} activities",
            "done": False,
            "source": "workout_plan",
        })

    # Add rest-day block when the workout plan marks the day as rest.
    if isinstance(workout, dict) and workout.get("isRestDay"):
        slots.append({
            "id": slot_id("rest"),
            "time": "10:30 am" if is_weekend else "5:00 pm",
            "category": "movement",
            "categoryLabel": "Movement",
            "text": "Rest day",
            "tip": workout.get("description") or "Use today for gentle movement, rest, and recovery.",
            "detail": "Recovery focus",
            "done": False,
            "source": "workout_plan",
        })

    # Add dinner if available.
    if dinner:
        slots.append({
            "id": slot_id("dinner"),
            "time": "6:30 pm",
            "category": "nutrition",
            "categoryLabel": "Nutrition",
            "text": dinner["meal_name"],
            "tip": dinner["description"],
            "detail": f"{to_number(dinner['calories'])} kcal",
            "done": False,
            "source": "nutrition_plan",
        })

    # Add sleep wind-down task if a sleep tip exists.
    if sleep_tip:
        slots.append({
            "id": slot_id("sleep"),
            "time": "7:30 pm" if context_data["primaryFocus"] == "sleep" else "8:00 pm",
            "category": "sleep",
            "categoryLabel": "Wind-down",
            "text": f"Sleep routine for {child_name}",
            "tip": sleep_tip,
            "detail": "Evening routine",
            "done": False,
            "source": "sleep_plan",
        })

    # If parent said routine is very busy/hard, return fewer tasks per day.
    if context_data.get("isBusy"):
        return slots[:5]

    return slots