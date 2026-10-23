from src.modelling.main import train_model_flow

if __name__ == "__main__":
    train_model_flow.serve(
        name="weekly-retraining",
        cron="0 0 * * 1",
        parameters={"trainset_path": "data/abalone.csv"},
    )
