import argparse
from pathlib import Path

from sklearn.model_selection import train_test_split

from src.modelling.predicting import evaluate_model
from src.modelling.preprocessing import TARGET_COLUMN, encode_features, fit_encoder, load_data
from src.modelling.training import train_model
from src.modelling.utils import pickle_object

LOCAL_OBJECTS_DIR = Path("src/web_service/local_objects")


def main(trainset_path: Path) -> None:
    """Train a model on the data at the given path and save the model and encoder as pickles."""
    df = load_data(trainset_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    encoder = fit_encoder(train_df)
    X_train = encode_features(train_df, encoder)
    X_test = encode_features(test_df, encoder)

    model = train_model(X_train, train_df[TARGET_COLUMN])
    rmse = evaluate_model(model, X_test, test_df[TARGET_COLUMN])
    print(f"Test RMSE: {rmse:.3f}")

    pickle_object(encoder, LOCAL_OBJECTS_DIR / "encoder.pkl")
    pickle_object(model, LOCAL_OBJECTS_DIR / "model.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model using the data at the given path.")
    parser.add_argument("trainset_path", type=Path, help="Path to the training set")
    args = parser.parse_args()
    main(args.trainset_path)
