import requests, csv, os
from datetime import datetime, timezone, timedelta

TOKEN = os.environ["MAPBOX_TOKEN"]
# lon,lat;lon,lat  (UB-ийн гол замууд, ойролцоо координат)
ROUTES = {
    "Enkhtaivan_W_E":   "106.8500,47.9170;106.9000,47.9180",
    "Enkhtaivan_E_W":   "106.9000,47.9180;106.8500,47.9170",
    "Enkhtaivan_C_E":   "106.9000,47.9180;106.9500,47.9150",
    "Enkhtaivan_E_C":   "106.9500,47.9150;106.9000,47.9180",
    "Chinggis_N_S":     "106.9170,47.9150;106.9150,47.8900",
    "Chinggis_S_N":     "106.9150,47.8900;106.9170,47.9150",
    "Narnii_W_E":       "106.8900,47.9050;106.9500,47.9050",
    "Narnii_E_W":       "106.9500,47.9050;106.8900,47.9050",
    "Baruun4_Zuun4":    "106.8850,47.9180;106.9400,47.9180",
    "Zaisan_Center":    "106.9150,47.8800;106.9170,47.9200",
}
URL = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{}"
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ub_mapbox.csv")
UB = timezone(timedelta(hours=8))

now = datetime.now(UB).isoformat(timespec="seconds")
new = not os.path.exists(FILE)
with open(FILE, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["time_ub","route","segment","speed_mps","congestion",
                    "seg_duration_s","seg_distance_m","route_duration_s","route_typical_s"])
    for name, coords in ROUTES.items():
        try:
            r = requests.get(URL.format(coords), params={
                "annotations": "congestion,speed,duration,distance",
                "overview": "full", "access_token": TOKEN}, timeout=30)
            d = r.json()
            route = d["routes"][0]
            a = route["legs"][0]["annotation"]
            for i in range(len(a["congestion"])):
                w.writerow([now, name, i, a["speed"][i], a["congestion"][i],
                            a["duration"][i], a["distance"][i],
                            route["duration"], route.get("duration_typical")])
        except Exception as e:
            print(name, "ERROR", e, str(d)[:200] if 'd' in dir() else "")
print("OK", now)
