from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

from predict import predict_health_score


app = FastAPI(
    title="Food Health Score API",
    description="API for predicting food health score from a food name.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://www.healthykids.live",
        "https://healthykids.live",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
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
    return predict_health_score(request.food_name)


handler = Mangum(app)