import json
import sys
import difflib
import os
import joblib
import numpy as np
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "food_health_regressor.pkl")
DATABASE_PATH = os.path.join(BASE_DIR, "food_database.json")


FEATURE_COLS = [
    "calories",
    "protein_g",
    "fat_g",
    "carbs_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
]

def json_safe(obj):
    """
    Convert numpy/pandas NaN and numpy types into JSON-safe Python values.
    NaN / inf -> None
    numpy number -> Python number
    """
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [json_safe(v) for v in obj]

    if isinstance(obj, tuple):
        return tuple(json_safe(v) for v in obj)

    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating, float)):
        if pd.isna(obj) or np.isinf(obj):
            return None
        return float(obj)

    if pd.isna(obj):
        return None

    return obj


class FoodHealthPredictor:
    def __init__(self, model_path=MODEL_PATH, database_path=DATABASE_PATH):
        self.model = joblib.load(model_path)

        with open(database_path, "r", encoding="utf-8") as f:
            self.food_db = json.load(f)

        self.food_names = list(self.food_db.keys())

    def search_food(self, food_name, top_n=5):
        """
        Search food by exact match, substring match, then fuzzy match.
        """
        key = food_name.strip().lower()

        # 1. Exact match
        if key in self.food_db:
            return [key]

        # 2. Substring match
        substring_matches = [
            name for name in self.food_names
            if key in name
        ]

        if substring_matches:
            return substring_matches[:top_n]

        # 3. Fuzzy match
        fuzzy_matches = difflib.get_close_matches(
            key,
            self.food_names,
            n=top_n,
            cutoff=0.4
        )

        return fuzzy_matches

    def build_feature_vector(self, nutrients):
        """
        Build model input.
        Missing values are converted to np.nan,
        then handled by SimpleImputer inside the saved Pipeline.
        """
        values = []

        for col in FEATURE_COLS:
            value = nutrients.get(col)

            if value is None:
                value = np.nan

            values.append(value)

        return pd.DataFrame([values], columns=FEATURE_COLS)

    def predict(self, food_name):
        # Invalid input
        if not food_name or not str(food_name).strip():
            return {
                "success": False,
                "status": "invalid_input",
                "message": "Food name cannot be empty.",
                "candidates": [],
                "data": None
            }

        matches = self.search_food(food_name)

        # Not found
        if not matches:
            return {
                "success": False,
                "status": "not_found",
                "message": f"No food found for: {food_name}",
                "candidates": [],
                "data": None
            }

        # Multiple matches
        if len(matches) > 1:
            return {
                "success": False,
                "status": "multiple_matches",
                "message": (
                    f"Multiple foods matched '{food_name}'. "
                    "Please choose one specific food name."
                ),
                "candidates": [
                    self.food_db[m]["original_name"] for m in matches
                ],
                "data": None
            }

        # Success
        selected_key = matches[0]
        record = self.food_db[selected_key]

        X = self.build_feature_vector(record["nutrients"])

        predicted_score = float(self.model.predict(X)[0])
        predicted_score = max(0, min(100, predicted_score))

        return {
            "success": True,
            "status": "success",
            "message": "Prediction completed successfully.",
            "candidates": [],
            "data": {
                "input_food": food_name,
                "matched_food": record["original_name"],
                "category": record["category"],
                "health_score": round(predicted_score, 2),
                "nutrition": X.to_dict(orient="records")[0]
            }
        }


# Load predictor only once
predictor = FoodHealthPredictor()


def predict_health_score(food_name: str):
    """
    Main function for backend/API integration.
    """
    result = predictor.predict(food_name)
    return json_safe(result)

def print_result(result):
    """
    CLI display only.
    API will directly return the JSON-style dict.
    """
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        food_name = " ".join(sys.argv[1:])
        result = predict_health_score(food_name)
        print_result(result)

    else:
        while True:
            food_name = input("\nEnter a food name, or q to quit: ").strip()

            if food_name.lower() in ["q", "quit", "exit"]:
                break

            result = predict_health_score(food_name)
            print_result(result)