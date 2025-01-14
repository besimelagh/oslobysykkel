from flask import Flask, render_template
import requests

app = Flask(__name__)

# Backend API URL
API_URL = "http://localhost:8000/stations"

@app.route("/")
def index():
    """
    Ruten for å vise kart med sykkelstasjoner.
    """
    try:
        response = requests.get(API_URL)
        stations = response.json().get("stations", [])
        return render_template("index.html", stations=stations)
    except Exception as e:
        return f"Error fetching station data: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
