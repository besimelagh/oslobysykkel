from flask import Flask, jsonify
import requests

app = Flask(__name__)

# API Base URL og Client-Identifier
BASE_URL = "https://gbfs.urbansharing.com/oslobysykkel.no/"
HEADERS = {"Client-Identifier": "origo-sykkelstasjoner"}

def get_feed_urls():
    """
    Henter URL-er for feeds fra gbfs.json.
    """
    try:
        response = requests.get(f"{BASE_URL}gbfs.json", headers=HEADERS)
        response.raise_for_status()
        feeds = response.json()["data"]["nb"]["feeds"]
        feed_urls = {feed["name"]: feed["url"] for feed in feeds}
        return feed_urls
    except Exception as e:
        raise RuntimeError(f"Kunne ikke hente feed-URL-er: {e}")

def fetch_station_data():
    """
    Henter og kombinerer stasjonsinformasjon og sanntidsstatus.
    """
    try:
        # Hent URL-er for feeds
        feeds = get_feed_urls()
        station_info_url = feeds["station_information"]
        station_status_url = feeds["station_status"]

        # Hent data fra feeds
        station_info = requests.get(station_info_url, headers=HEADERS).json()
        station_status = requests.get(station_status_url, headers=HEADERS).json()

        # Valider GBFS-struktur
        if "last_updated" not in station_info or "ttl" not in station_info:
            raise ValueError("Ugyldig respons fra station_information.json")
        if "last_updated" not in station_status or "ttl" not in station_status:
            raise ValueError("Ugyldig respons fra station_status.json")

        # Kombiner data basert på station_id
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
        raise RuntimeError(f"Feil under henting av stasjonsdata: {e}")

@app.route("/stations", methods=["GET"])
def get_stations():
    """
    API-endepunkt for å returnere sykkelstasjonsdata.
    """
    try:
        stations = fetch_station_data()
        return jsonify({"stations": stations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
