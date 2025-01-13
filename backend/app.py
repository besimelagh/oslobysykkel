from fastapi import FastAPI
import requests

app = FastAPI()

BASE_URL = "https://gbfs.urbansharing.com/oslobysykkel.no/"
HEADERS = {"Client-Identifier": "besim-sykkelstasjoner"}

@app.get("/stations")
def get_stations():
    # Hent stasjonsinformasjon
    station_info = requests.get(BASE_URL + "station_information.json", headers=HEADERS).json()
    station_status = requests.get(BASE_URL + "station_status.json", headers=HEADERS).json()

    # Kombiner dataene
    station_data = []
    info_dict = {station["station_id"]: station for station in station_info["data"]["stations"]}
    for status in station_status["data"]["stations"]:
        station_id = status["station_id"]
        if station_id in info_dict:
            station = info_dict[station_id]
            station_data.append({
                "id": station_id,
                "name": station["name"],
                "address": station["address"],
                "lat": station["lat"],
                "lon": station["lon"],
                "capacity": station["capacity"],
                "num_bikes_available": status["num_bikes_available"],
                "num_docks_available": status["num_docks_available"],
            })

    return {"stations": station_data}

