# Read var_values.json
import csv
import json
from pprint import pprint

import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import folium
if __name__ == '__main__':
    with open('var_values.json', 'r') as f:
        var_values = json.load(f)

    # Extract facility_id and visualize on map
    with open('data/new_child_care.csv', 'r', encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile)
        child_care_data = {row[0]: row for row in reader}
    zipcode_data_list = []

    for key, value in var_values.items():
        if key.startswith("expansion_percentage_"):
            facility_id = key.split('_')[-1]
            if value > 0 and facility_id in child_care_data:
                row = child_care_data[facility_id]
                zipcode = row[5]

                # Append the necessary data to the list
                zipcode_data_list.append({
                    'ZIP_Code': zipcode,
                    'County_Name': row[6],
                    'Cluster': value
                })

    # Create a DataFrame with the collected data
    zipcode_data = pd.DataFrame(zipcode_data_list)

    with urlopen(
            'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/ny_new_york_zip_codes_geo.min.json') as response:
        zipcodes = json.load(response)
    fig = px.choropleth(zipcode_data,
                        geojson=zipcodes,
                        locations='ZIP_Code',
                        color='Cluster',
                        color_continuous_scale="Viridis",
                        range_color=(1, 5),
                        featureidkey="properties.ZCTA5CE10",
                        scope="usa",
                        labels={'Cluster': 'Cluster_Category'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Save the plot
    fig.write_html("visuals/choropleth_map_expansion.html")

    # Extract location data and visualize on map
    with open('data/new_potential_locations.csv', 'r', encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile)
        potential_locations_data = {index: row for index, row in enumerate(reader, start=1)}
        pprint(potential_locations_data)
    location_data_list = []
    for key, value in var_values.items():
        if key.startswith("location_"):
            location_info = key.split('_')
            location_number = int(location_info[1])  # Convert to integer to use as row number
            facility_type = location_info[2]  # Get the facility type (small, medium, large)

            if value > 0 and location_number in range(1, len(potential_locations_data) + 1):
                row = potential_locations_data.get(location_number, None)
                if row is None:
                    continue
                latitude = float(row[1])
                longitude = float(row[2])

                # Append the necessary data to the list
                location_data_list.append({
                    'Latitude': latitude,
                    'Longitude': longitude,
                    'Cluster': value,
                    'Facility_Type': facility_type
                })
    print(location_data_list)
    # Create a DataFrame with the collected data
    location_data = pd.DataFrame(location_data_list)

    # Create a map with the collected data
    map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    for _, row in location_data.iterrows():
        color = 'blue'
        if row['Facility_Type'] == 'small':
            color = 'green'
        elif row['Facility_Type'] == 'medium':
            color = 'orange'
        elif row['Facility_Type'] == 'large':
            color = 'red'

        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            popup=f"Cluster: {row['Cluster']}, Facility Type: {row['Facility_Type']}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(map)

    # Save the map
    map.save("visuals/map_potential_locations.html")