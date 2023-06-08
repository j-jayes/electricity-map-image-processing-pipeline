import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load Excel data
df = pd.read_excel('data/intermediate/single_table/combined_data_geocoded_clean_amount_classified_source.xlsx')

# Filter out rows with missing lat/long values
df = df.dropna(subset=['latitude', 'longitude'])

# Create a Map centered around Sweden
m = folium.Map(location=[63.0, 16.0], zoom_start=5)

# Define the color scheme for the different power sources
color_dict = {'water': 'blue', 'NULL': 'gray', 'steam': 'red', 'transmitted': 'green', 'd': 'purple'}

# Initialize MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

# Iterate over rows in dataframe
for index, row in df.iterrows():
    # Check if source_clean exists in color_dict, else default to black
    marker_color = color_dict.get(row['source_clean'], 'black')

    # Create a CircleMarker for each station
    marker = folium.CircleMarker(
        location=(row['latitude'], row['longitude']), 
        radius=row['amount_clean']/1000, # Adjust the divider to change circle size
        color=marker_color,
        fill=True,
        fill_opacity=0.6
    )

    # Create a Popup for each marker
    popup = folium.Popup(
        f"<b>Name:</b> {row['name']}<br>"
        f"<b>Location:</b> {row['location']}<br>"
        f"<b>Amount:</b> {row['amount_clean']}<br>"
        f"<b>Source:</b> {row['source_clean']}<br>"
        f"<b>User:</b> {row['user']}", 
        max_width=250
    )

    # Add popup to marker
    marker.add_child(popup)

    # Add marker to MarkerCluster
    marker_cluster.add_child(marker)

# Save map
m.save('map.html')
