import json
import folium
import requests
from flask import Flask


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

@app.route('/')
def index():

    locations = []
    center = []
    lat, long = [], []

    response_json = download()
    start_coords = (6.524400, 3.379199)

    for devname in response_json["rows"]:
        lat.append(float(devname["latitude_deg"]))
        long.append(float(devname["longitude_deg"]))
    center = [mean(lat), mean(long)]

    #Adding markers to the map
    m=folium.Map(location=start_coords, tiles='cartodbpositron',zoom_start=3)
    for la, lo in zip(lat, long):
        folium.Marker(location=[la, lo], popup=f"{la},{lo}",tooltip='Click here to see Popup').add_to(m)


    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
