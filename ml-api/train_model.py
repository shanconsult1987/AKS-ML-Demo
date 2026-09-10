from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

iris = load_iris()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(iris.data, iris.target)

os.makedirs("model", exist_ok=True)
joblib.dump({
    "model": model,
    "target_names": iris.target_names.tolist()
}, "model/model.pkl")

print("Model trained successfully.")
