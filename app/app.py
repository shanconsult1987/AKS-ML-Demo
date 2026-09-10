from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "application": "AKS Demo",
        "pod": os.getenv("HOSTNAME", "unknown"),
        "time": str(datetime.utcnow())
    }

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
