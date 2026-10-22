from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL_COLUMNS = ["Sex"]
TARGET_COLUMN = "Rings"


def load_data(path: Path) -> pd.DataFrame:
    """Read the abalone dataset and drop the rows with an impossible height of 0."""
    df = pd.read_csv(path)
    return df[df["Height"] > 0]


def fit_encoder(df: pd.DataFrame) -> OneHotEncoder:
    """Fit a one-hot encoder on the categorical columns."""
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoder.fit(df[CATEGORICAL_COLUMNS])
    return encoder


def encode_features(df: pd.DataFrame, encoder: OneHotEncoder) -> pd.DataFrame:
    """Replace the categorical columns by their one-hot encoding."""
    encoded = pd.DataFrame(
        encoder.transform(df[CATEGORICAL_COLUMNS]),
        columns=encoder.get_feature_names_out(),
        index=df.index,
    )
    numerical = df.drop(columns=CATEGORICAL_COLUMNS + [TARGET_COLUMN], errors="ignore")
    return pd.concat([numerical, encoded], axis=1)
