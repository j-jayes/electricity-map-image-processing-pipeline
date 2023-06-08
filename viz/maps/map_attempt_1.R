# Map based on the data that we have created

library(tidyverse)
library(here)

df <- readxl::read_excel((here("data", "intermediate", "single_table", "combined_data_manual_edits_source_amount.xlsx")))

colnames(df)

df %>%
  ggplot(aes(x = longitude, y = latitude, color = source_final)) +
  geom_point() +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Map of the data that we have created",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

df %>%
  ggplot(aes(x = longitude, y = latitude, color = source_final)) +
  geom_point() +
  theme_bw() +
  theme(legend.position = "right") +
  facet_wrap(~source_final) +
  coord_map() +
  labs(title = "Map of the data that we have created",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

# Load necessary libraries
library(sf)
library(histmaps)

map_county <- get_boundaries(1925, "county")

map_county <- map_county %>% 
  st_transform(4326) %>%
  rename(name_county = name)

map_county %>% ggplot() + geom_sf()



# 1. Convert the power stations dataframe to an sf object
df_sf <- df %>% 
  st_as_sf(coords = c("longitude", "latitude"), crs = 4326)

sf_use_s2(FALSE)
# 2. Spatial join - associate each power station to a county
df_join <- st_join(df_sf, map_county)
sf_use_s2(TRUE)

# 3. Group by county and power station type, and count the number of power stations
power_station_counts_by_county <- df_join %>%
  group_by(name_county, source_final) %>%
  summarise(n = n(), .groups = "drop")

# 4. make a column plot with number of power stations by county on the x-axis and county codes on the y-axis
power_station_counts_by_county %>%
  ggplot(aes(x = n, y = name_county, fill = source_final)) +
  geom_col(position = "dodge") +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Number of power stations by county",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")


# 4. make a column plot with number of power stations by county on the x-axis and county codes on the y-axis
power_station_counts_by_county %>%
  ggplot(aes(x = n, y = name_county, fill = source_final)) +
  geom_col(position = "stack") +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Number of power stations by county",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

# 5. make a facet map where the share of each power station type is shown for each county
power_station_share_by_county <- power_station_counts_by_county %>%
  group_by(name_county) %>%
  mutate(share = n / sum(n)) 


power_station_share_by_county %>%
  ggplot(aes(x = share, y = name_county, fill = source_final)) +
  geom_col(position = "fill") 

# 6. make a map where the share of 'transmitted' power stations is shown for each county
power_station_share_by_county %>%
  filter(source_final == "transmitted") %>%
  ggplot() +
  geom_sf(aes(colour = share)) +
  scale_colour_viridis_c() +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Share of 'transmitted' power stations by county",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

# 7. import the shapefile with the power lines

power_lines <- read_rds(here("data", "shapefiles", "1926_grid.rds"))


power_lines %>%
  ggplot() +
  geom_sf() +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Power lines",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")


## New section
# 1. A map at the parish level that shows share of power from "transmitted" power stations
map_parish <- get_boundaries(1925, "parish")

map_parish <- map_parish %>% 
  st_transform(4326) %>%
  rename(name_parish = name)

map_parish %>% ggplot() + geom_sf()


# 1. Convert the power stations dataframe to an sf object
df_sf <- df %>% 
  st_as_sf(coords = c("longitude", "latitude"), crs = 4326)

sf_use_s2(FALSE)
# 2. Spatial join - associate each power station to a county
df_join <- st_join(map_parish, df_sf)

# 3. Group by county and power station type, and count the number of power stations
power_station_counts_by_parish <- df_join %>%
  group_by(name_parish, source_final) %>%
  summarise(n = n(), .groups = "drop")

power_station_share_by_parish <- power_station_counts_by_parish %>%
  group_by(name_parish) %>%
  mutate(share = n / sum(n)) 

power_station_share_by_parish %>%
  filter(source_final == "transmitted") %>%
  ggplot(aes(fill = share)) +
  scale_fill_viridis_c() +
  geom_sf() +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Share of 'transmitted' power stations by parish",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

power_station_share_by_parish %>%
  filter(source_final == "water") %>%
  ggplot(aes(fill = share)) +
  scale_fill_viridis_c() +
  geom_sf() +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = "Share of 'water' power stations by parish",
       subtitle = "The data is based on the data that we have created",
       caption = "Source:")

df_join %>% 
  mutate()

## Regression

electrified_parishes <- read_rds(here("data", "shapefiles", "electrified_parishes_1930.rds"))
