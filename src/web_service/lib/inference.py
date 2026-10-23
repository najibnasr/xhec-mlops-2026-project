import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.preprocessing import OneHotEncoder

from src.modelling.predicting import predict
from src.modelling.preprocessing import encode_features
from src.web_service.lib.models import AbaloneInput, PredictionOutput

# Mapping between the API field names and the column names of the training data
COLUMN_NAMES = {
    "sex": "Sex",
    "length": "Length",
    "diameter": "Diameter",
    "height": "Height",
    "whole_weight": "Whole weight",
    "shucked_weight": "Shucked weight",
    "viscera_weight": "Viscera weight",
    "shell_weight": "Shell weight",
}


def run_inference(
    payload: AbaloneInput, model: RegressorMixin, encoder: OneHotEncoder
) -> PredictionOutput:
    """Predict the number of rings (and the age) of one abalone."""
    df = pd.DataFrame([payload.model_dump()]).rename(columns=COLUMN_NAMES)
    X = encode_features.fn(df, encoder)
    rings = float(predict(model, X)[0])
    return PredictionOutput(rings=round(rings, 2), age=round(rings + 1.5, 2))
