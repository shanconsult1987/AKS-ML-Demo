from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

data = joblib.load("model/model.pkl")
model = data["model"]
target_names = data["target_names"]

@app.route("/")
def home():
    return {
        "application": "AKS Machine Learning API",
        "model": "Random Forest Iris Classifier",
        "pod": os.getenv("HOSTNAME", "unknown")
    }

@app.route("/health")
def health():
    return {"status": "healthy", "pod": os.getenv("HOSTNAME", "unknown")}

@app.route("/predict", methods=["POST"])
def predict():
    features = request.get_json()["features"]
    prediction = int(model.predict([features])[0])
    probability = float(model.predict_proba([features])[0][prediction])
    return jsonify({
        "prediction": prediction,
        "class": target_names[prediction],
        "probability": probability,
        "pod": os.getenv("HOSTNAME", "unknown")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
