import json
import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


HEALTHY_DB_PATH = "healthy_foods_database.csv"
FOODSTRUCT_PATH = "foodstruct_nutritional_facts.csv"

MODEL_OUTPUT_PATH = "food_health_regressor.pkl"
DATABASE_OUTPUT_PATH = "food_database.json"
REPORT_OUTPUT_PATH = "training_report.txt"


FEATURE_COLS = [
    "calories",
    "protein_g",
    "fat_g",
    "carbs_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
]

TARGET_COL = "health_score"


FOODSTRUCT_COL_MAP = {
    "Calories": "calories",
    "Protein": "protein_g",
    "Fats": "fat_g",
    "Carbs": "carbs_g",
    "Fiber": "fiber_g",
    "Sugar": "sugar_g",
    "Sodium": "sodium_mg",
}


def convert_foodstruct_value(foodstruct_col, target_col, value):
    """
    Convert foodstruct value into the same unit as healthy_foods_database.
    Sodium: g -> mg
    """

    if pd.isna(value):
        return np.nan

    value = float(value)

    if target_col == "sodium_mg":
        return value * 1000

    return value


def train_model():
    df = pd.read_csv(HEALTHY_DB_PATH)

    required_cols = FEATURE_COLS + [TARGET_COL]
    df = df[required_cols].copy()

    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Delete only the missing rows of target.
    # Missing features are handled by SimpleImputer.
    df = df.dropna(subset=[TARGET_COL])

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X,y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    cv_scores = cross_val_score(
        pipeline,
        X,y,
        cv=5,
        scoring="r2",
        n_jobs=-1
    )

    joblib.dump(pipeline, MODEL_OUTPUT_PATH)

    model = pipeline.named_steps["model"]
    importances = dict(zip(FEATURE_COLS, model.feature_importances_))

    with open(REPORT_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("Food Health Score Regression Model Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total records: {len(df)}\n")
        f.write(f"Training records: {len(X_train)}\n")
        f.write(f"Testing records: {len(X_test)}\n\n")

        f.write("Target distribution:\n")
        f.write(y.value_counts().sort_index().to_string())
        f.write("\n\n")

        f.write(f"MAE: {mae:.4f}\n")
        f.write(f"RMSE: {rmse:.4f}\n")
        f.write(f"R2 Score: {r2:.4f}\n")
        f.write(f"5-Fold CV R2: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}\n\n")

        f.write("Feature Importance:\n")
        for col, score in sorted(importances.items(), key=lambda x: -x[1]):
            f.write(f"{col}: {score:.4f}\n")

    print("Model training completed.")
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    print(f"Training report saved to: {REPORT_OUTPUT_PATH}")


def build_food_database():
    df = pd.read_csv(FOODSTRUCT_PATH)

    food_database = {}

    for _, row in df.iterrows():
        food_name = str(row["Food Name"]).strip()
        key = food_name.lower()

        nutrients = {}

        for foodstruct_col, target_col in FOODSTRUCT_COL_MAP.items():
            raw_value = row.get(foodstruct_col, np.nan)

            converted_value = convert_foodstruct_value(
                foodstruct_col,
                target_col,
                raw_value
            )

            if pd.isna(converted_value):
                nutrients[target_col] = None
            else:
                nutrients[target_col] = round(float(converted_value), 4)

        food_database[key] = {
            "original_name": food_name,
            "category": str(row.get("Category Name", "Unknown")).strip(),
            "nutrients": nutrients
        }

    with open(DATABASE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(food_database, f, ensure_ascii=False, indent=2)

    print("Food database completed.")
    print(f"Food database saved to: {DATABASE_OUTPUT_PATH}")


if __name__ == "__main__":
    train_model()
    build_food_database()