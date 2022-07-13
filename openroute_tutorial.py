import folium
import openrouteservice as ors

# import PYTHON_API_KEYS


# enter your openrouteservice api key here as string
ors_key = '5b3ce3597851110001cf62486d6ad0e922c94437ad054d71396dc725'

# performs requests to the ORS API services
# client will be used in all examples
client = ors.Client(key=ors_key)

# coordinates from Nashville, TN (-86.781247, 36.163532) to Miami, FL (-80.191850, 25.771645)
# order for coordinates is [lon, lat]
coordinates = [[-86.781247, 36.163532], [-80.191850, 25.771645]]

# directions
route = client.directions(coordinates=coordinates,
                          profile='driving-car',
                          format='geojson')

# map
map_directions = folium.Map(location=[33.77, -84.37], zoom_start=5)

# add geojson to map
folium.GeoJson(route, name='route').add_to(map_directions)

# add layer control to map (allows layer to be turned on or off)
folium.LayerControl().add_to(map_directions)

# display map
map_directions.save("foliummap1.html")

# distance and duration
print(route['features'][0]['properties']['segments'][0]['distance'] * 0.000621371, 'miles')
print(route['features'][0]['properties']['segments'][0]['duration'] * 0.000277778, 'hours\n')

# distances are in meters
# timings are in seconds
print('directions')
for index, i in enumerate(route['features'][0]['properties']['segments'][0]['steps']):
    print(index + 1, i, '\n')

# coordinates
coordinates = [[-80.127995, 25.784097]]

# isochrone
isochrone = client.isochrones(locations=coordinates,
                              range_type='time',
                              # 900 seconds, 15 minutes
                              range=[900],
                              attributes=['total_pop'])

# map
map_isochrone = folium.Map(location=[25.784097, -80.127995], tiles='cartodbpositron', zoom_start=12)

# add geojson to map with population
population = isochrone['features'][0]['properties']['total_pop']
folium.GeoJson(isochrone, name='isochrone', tooltip=f'population: {population:,.0f}').add_to(map_isochrone)

# add marker to map
minutes = isochrone['features'][0]['properties']['value'] / 60
popup_message = f'outline shows areas reachable within {minutes} minutes'
folium.Marker([25.784097, -80.127995], popup=popup_message, tooltip='click').add_to(map_isochrone)

# add layer control to map (allows layer to be turned on or off)
folium.LayerControl().add_to(map_isochrone)

# display map
map_isochrone.save("isochrone_map.html")

# map
map_geocode = folium.Map(location=[31.7755, -106.4664], tiles='cartodbpositron', zoom_start=13)

# address
address = '4001 E Paisano Dr, El Paso, TX, 79905'

# geocode
geocode = client.pelias_search(text=address, focus_point=list(reversed(map_geocode.location)))

# add marker to map (El Paso Zoo)
for result in geocode['features']:
    folium.Marker(location=list(reversed(result['geometry']['coordinates'])),
                  icon=folium.Icon(icon='building', color='green', prefix='fa'),
                  popup=folium.Popup(result['properties']['name'])).add_to(map_geocode)

# display map
map_geocode.save("geocode_map.html")

# coordinates
geojson = {"type": "point", "coordinates": [-106.435073, 31.774464]}
coordinates = [31.774464, -106.435073]

# places of interest
pois = client.places(request='pois',
                     geojson=geojson,
                     # buffer searches (in meters) around specified point
                     buffer=2000,
                     # hospital: 206, restaurant: 570
                     filter_category_ids=[206, 570])

# map
map_pois = folium.Map(location=coordinates, tiles='cartodbpositron', zoom_start=14)

# add center point
folium.Marker(coordinates, icon=folium.Icon(color='red')).add_to(map_pois)

# add search area circle
folium.Circle(radius=2000, location=coordinates, color='green').add_to(map_pois)

# add markers to map
for poi in pois['features']:
    folium.Marker(location=list(reversed(poi['geometry']['coordinates'])),
                  icon=folium.Icon(color='blue'),
                  popup=folium.Popup(poi['properties']['osm_tags']['name'])).add_to(map_pois)

# display map
map_pois.save("POI_map.html")
