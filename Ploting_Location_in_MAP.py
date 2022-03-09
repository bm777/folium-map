import json
import folium
import requests
from flask import Flask
from datetime import date
from datetime import datetime


app = Flask(__name__)

def download():
    url = "https://kandaweather-mainnet.ddns.net/v1/chain/get_table_rows"
    HEADER = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    DATA = "{\"code\":\"dclimateiot4\",\"table\":\"weather\",\"scope\":\"dclimateiot4\",\"index_position\":\"first\",\"json\":\"true\"}"
    res = requests.post(url, headers = HEADER, data = DATA)
    response_json = json.loads(res.text)
    return response_json

def mean(l):
    return sum(l)/len(l)

def difference_days(t=1646780874):
    from datetime import datetime

    timestamp = t
    dt = datetime.fromtimestamp(timestamp)
    dt = str(dt)
    d = dt.split()[0].split("-")

    return d

@app.route('/')
def index():

    locations = []
    center = []
    lat, long = [], []
    unix_time_s = []

    response_json = download()
    start_coords = (6.524400, 3.379199)

    for devname in response_json["rows"]:

        lat.append(float(devname["latitude_deg"]))
        long.append(float(devname["longitude_deg"]))
        unix_time_s.append(devname["unix_time_s"])
    center = [mean(lat), mean(long)]

    #Adding markers to the map
    m=folium.Map(location=start_coords, tiles='cartodbpositron',zoom_start=3)
    for la, lo, unix_time in zip(lat, long, unix_time_s):
        d = difference_days(unix_time)

        now = datetime.now().strftime(format="%Y-%m-%d")
        now = str(now)
        n = now.split("-")

        dif = date(int(n[0]), int(n[1]), int(n[2])) - date(int(d[0]), int(d[1]), int(d[2]))
        inter = dif.days
        if inter < 7:
            color = "green"
        elif inter >= 7 and inter < 28:
            color = "yellow"
        elif inter >= 28:
            color = "red"

        folium.Marker(location=[la, lo], popup=f"{la},{lo}",tooltip='Click here to see location',icon=folium.Icon(color=color,icon='off')).add_to(m)


    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
