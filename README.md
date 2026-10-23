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

## Training

Train the model and save it, with its encoder, in `src/web_service/local_objects/`:

```bash
uv run python -m src.modelling.main data/abalone.csv
```

## Orchestration with Prefect

The training pipeline is a Prefect flow (`src/modelling/main.py`), and each step is a Prefect task.

1. Start the Prefect server (UI available at http://127.0.0.1:4200):

```bash
uv run prefect server start
```

2. In another terminal, point the client to this server:

```bash
uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

3. Run the training flow once:

```bash
uv run python -m src.modelling.main data/abalone.csv
```

4. Serve the deployment that retrains the model every Monday at midnight:

```bash
uv run python -m src.modelling.deployment
```

The flow runs and the deployment can then be followed in the Prefect UI.
