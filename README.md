# MLOps Project: Abalone Age Prediction

Predict the age of abalone (number of rings) from physical measurements, with an automated training pipeline and a prediction API.

## Team

- Najib Nasr ([@najibnasr](https://github.com/najibnasr))

## Project structure

```
├── notebooks/              # EDA and first modelling pass (tracked with MLflow)
├── src/
│   ├── modelling/          # Training pipeline (Prefect flow and tasks)
│   └── web_service/        # FastAPI app, Pydantic models, saved model and encoder
├── bin/run_services.sh     # Starts the Prefect server and the API (used in Docker)
└── Dockerfile.app
```

## Setup

Requirements: Python 3.11, [uv](https://docs.astral.sh/uv/) and Docker.

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

```bash
uv run --with jupyter jupyter lab
```

To compare the MLflow runs, from the `notebooks` folder:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Then open http://127.0.0.1:5000.

## Training

The model is a linear regression on the physical measurements, with `Sex` one-hot encoded. The training script saves the model and its encoder in `src/web_service/local_objects/`:

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

## Prediction API

The API is built with FastAPI and validates the inputs with Pydantic.

### Run it with Docker

```bash
docker build -t abalone-api -f Dockerfile.app .
docker run -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api
```

- API documentation: http://localhost:8000/docs
- Prefect UI: http://localhost:4200

### Run it locally (without Docker)

```bash
uv run uvicorn src.web_service.main:app --port 8001
```

The documentation is then available at http://127.0.0.1:8001/docs.

### Example request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

Response:

```json
{"rings": 9.22, "age": 10.72}
```

`sex` must be `M`, `F` or `I` (infant), and every measurement must be positive. Otherwise the API returns a 422 error.
