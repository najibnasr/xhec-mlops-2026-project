import numpy as np
import pandas as pd
from prefect import task
from sklearn.base import RegressorMixin
from sklearn.metrics import root_mean_squared_error


def predict(model: RegressorMixin, X: pd.DataFrame) -> np.ndarray:
    """Predict the number of rings for each row of X."""
    return model.predict(X)


@task
def evaluate_model(model: RegressorMixin, X: pd.DataFrame, y: pd.Series) -> float:
    """Return the RMSE of the model on the given data."""
    return root_mean_squared_error(y, predict(model, X))
