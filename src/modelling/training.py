import pandas as pd
from prefect import task
from sklearn.linear_model import LinearRegression


@task
def train_model(X: pd.DataFrame, y: pd.Series) -> LinearRegression:
    """Train a linear regression predicting the number of rings."""
    model = LinearRegression()
    model.fit(X, y)
    return model
