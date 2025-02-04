from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# Load the trained model
try:
    model = joblib.load("fraud_model.joblib")
except FileNotFoundError:
    model = None

feature_names = [f'feature_{i}' for i in range(20)]

class Transaction(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(transaction: Transaction):
    if model is None:
        return {"error": "Model not loaded"}
    features = np.array(transaction.features).reshape(1, -1)
    features_df = pd.DataFrame(features, columns=feature_names)
    prediction = model.predict(features_df)
    probability = model.predict_proba(features_df).max()
    return {"prediction": int(prediction[0]), "probability": probability}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
