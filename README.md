# MLOps Project: Abalone Age Prediction

Predict the age of abalone (number of rings) from physical measurements, with an automated training pipeline and a prediction API.

## Team

- Najib Nasr ([@najibnasr](https://github.com/najibnasr))

## Setup

Requirements: Python 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
source .venv/bin/activate
uv run pre-commit install
```

## Data

Download `abalone.csv` from [Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) and put it in a `data/` folder at the root of the project:

```
data/abalone.csv
```

The `data/` folder is git-ignored.

## Notebooks

The `notebooks` folder contains the exploratory analysis (`eda.ipynb`) and a first modelling pass (`modelling.ipynb`), with experiments tracked in MLflow.

To run them:

```bash
uv run --with jupyter jupyter lab
```

To compare the MLflow runs, from the `notebooks` folder:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Then open http://127.0.0.1:5000.
