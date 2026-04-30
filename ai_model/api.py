from fastapi import FastAPI
from pydantic import BaseModel
from predict import predict_health_score


app = FastAPI(
    title="Food Health Score API",
    description="API for predicting food health score from a food name.",
    version="1.0.0"
)


class FoodRequest(BaseModel):
    food_name: str


@app.get("/")
def root():
    return {
        "message": "Food Health Score API is running."
    }


@app.post("/predict")
def predict_food_health(request: FoodRequest):
    result = predict_health_score(request.food_name)
    return result