from flask import Flask

import folium

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    #fig=Figure(width=550,height=350)
    folium_map =folium.Map(location=[28.644800, 77.216721],tiles='cartodbpositron',zoom_start=11)
    #fig.add_child(folium_map)

    #Adding markers to the map
    folium.Marker(location=[28.695800, 77.244721],popup='Default popup Marker1',tooltip='Click here to see Popup').add_to(folium_map)
    folium.Marker(location=[28.645800, 77.214721],popup='<strong>Marker3</strong>',tooltip='<strong>Click here to see Popup</strong>').add_to(folium_map)
    folium.Marker(location=[28.655800, 77.274721],popup='<h3 style="color:green;">Marker2</h3>',tooltip='<strong>Click here to see Popup</strong>').add_to(folium_map)


    return folium_map._repr_html_()
    
if __name__ == '__main__':
    app.run(debug=True)
