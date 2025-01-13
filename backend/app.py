from flask import Flask, jsonify
import requests

app = Flask(__name__)

# API-konfigurasjon
BASE_URL = "https://gbfs.urbansharing.com/oslobysykkel.no/"
HEADERS = {"Client-Identifier": "origo-sykkelstasjoner"}

def fetch_station_data():
    """
    Henter og kombinerer stasjonsinformasjon og sanntidsstatus.
    """
    try:
        # Hent stasjonsinformasjon
        station_info = requests.get(f"{BASE_URL}station_information.json", headers=HEADERS).json()
        station_status = requests.get(f"{BASE_URL}station_status.json", headers=HEADERS).json()

        # Kombiner data
        stations = []
        info_dict = {station["station_id"]: station for station in station_info["data"]["stations"]}

        for status in station_status["data"]["stations"]:
            station_id = status["station_id"]
            if station_id in info_dict:
                station = info_dict[station_id]
                stations.append({
                    "id": station_id,
                    "name": station["name"],
                    "address": station["address"],
                    "lat": station["lat"],
                    "lon": station["lon"],
                    "capacity": station["capacity"],
                    "num_bikes_available": status["num_bikes_available"],
                    "num_docks_available": status["num_docks_available"],
                })

        return stations
    except Exception as e:
        return {"error": str(e)}

@app.route("/stations", methods=["GET"])
def get_stations():
    """
    API-endepunkt for å hente stasjonsdata.
    """
    data = fetch_station_data()
    if "error" in data:
        return jsonify(data), 500
    return jsonify({"stations": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
