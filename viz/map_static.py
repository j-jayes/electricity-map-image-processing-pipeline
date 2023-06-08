import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D

# Load the boundaries of Sweden
sweden = gpd.read_file('data/shapefiles/sweden_24_couties.shp')

# Load Excel data
df = pd.read_excel('data/intermediate/single_table/combined_data_geocoded_clean_amount_classified_source.xlsx')

# Filter out rows with missing lat/long values
df = df.dropna(subset=['latitude', 'longitude'])

# Create a GeoDataFrame from the DataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Define the color scheme for the different power sources
color_dict = {'water': 'blue', 'NULL': 'gray', 'steam': 'red', 'transmitted': 'green', 'd': 'purple', None: 'black'}

# Create a new column for color based on 'source_clean'
gdf['color'] = gdf['source_clean'].map(color_dict)

# Handle NaN color values
gdf['color'] = gdf['color'].fillna('black')

# Map color labels to numbers
color_labels = gdf['color'].unique()
color_map = dict(zip(color_labels, range(len(color_labels))))
gdf['color_num'] = gdf['color'].map(color_map)

# Create a colormap
cmap = mcolors.ListedColormap(gdf['color'].unique())

# Plot the map of Sweden
base = sweden.plot(color='white', edgecolor='black')

# Plot the points from the GeoDataFrame
gdf.plot(ax=base, column='color_num', cmap=cmap, markersize=gdf['amount_clean']/1000, alpha=0.6)

# Create legend manually
legend_elements = [Line2D([0], [0], marker='o', color='w', label=key, markerfacecolor=value, markersize=10) 
                   for key, value in color_dict.items() if key is not None]

# Add a legend
base.legend(handles=legend_elements, title='Power Sources')

# Show the plot
# plt.show()

# save the plot
plt.savefig('viz/maps/map_static.png', dpi=300)