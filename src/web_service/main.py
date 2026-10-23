from pathlib import Path

from fastapi import FastAPI

from src.web_service.lib.inference import run_inference
from src.web_service.lib.models import AbaloneInput, PredictionOutput
from src.web_service.utils import load_object

LOCAL_OBJECTS_DIR = Path(__file__).parent / "local_objects"

app = FastAPI(
    title="Abalone age prediction",
    description="Predict the age of an abalone from its physical measurements.",
)

model = load_object(LOCAL_OBJECTS_DIR / "model.pkl")
encoder = load_object(LOCAL_OBJECTS_DIR / "encoder.pkl")


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOutput, status_code=201)
def predict(payload: AbaloneInput) -> PredictionOutput:
    """Return the predicted number of rings and age of the abalone."""
    return run_inference(payload, model, encoder)
