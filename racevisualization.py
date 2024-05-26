import os
import fastf1 as ff1
from fastf1 import plotting
import folium
from folium.plugins import MarkerCluster
import numpy as np
from matplotlib import pyplot as plt

# Define cache directory
cache_dir = 'cache'

# Create cache directory if it doesn't exist
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Setup plotting
plotting.setup_mpl()
# Enable the cache
ff1.Cache.enable_cache(cache_dir)

# Load the session data
race = ff1.get_session(2021, 'Zandvoort', 'R')

# Load the session to access the data
race.load()

# Collect all race laps
laps = race.laps

# Get laps of the drivers (BOT and HAM)
laps_bot = laps.pick_driver('BOT')
laps_ham = laps.pick_driver('HAM')

# Extract the fastest laps
fastest_bot = laps_bot.pick_fastest()
fastest_ham = laps_ham.pick_fastest()

# Get telemetry from fastest laps
telemetry_bot = fastest_bot.get_car_data().add_distance()
telemetry_ham = fastest_ham.get_car_data().add_distance()

# Create a Folium map centered around Circuit Zandvoort
map_zandvoort = folium.Map(location=[52.389, 4.541], zoom_start=15)

# Plot car positions on the map
marker_cluster_bot = MarkerCluster(name='BOT Car Positions').add_to(map_zandvoort)
marker_cluster_ham = MarkerCluster(name='HAM Car Positions').add_to(map_zandvoort)

# Add car positions for BOT
for idx, row in telemetry_bot.iterrows():
    folium.Marker(location=[row['Distance'], 0], popup=f'BOT - Distance: {row["Distance"]:.2f} m', icon=folium.Icon(color='red')).add_to(marker_cluster_bot)

# Add car positions for HAM
for idx, row in telemetry_ham.iterrows():
    folium.Marker(location=[row['Distance'], 0], popup=f'HAM - Distance: {row["Distance"]:.2f} m', icon=folium.Icon(color='green')).add_to(marker_cluster_ham)

# Plot the data
fig, ax = plt.subplots(3, sharex=True)
fig.suptitle("Fastest Race Lap Telemetry Comparison")

# Plot speed
ax[0].plot(telemetry_bot['Distance'], telemetry_bot['Speed'], label='BOT')
ax[0].plot(telemetry_ham['Distance'], telemetry_ham['Speed'], label='HAM')
ax[0].set(ylabel='Speed')
ax[0].legend(loc="lower right")

# Plot throttle
ax[1].plot(telemetry_bot['Distance'], telemetry_bot['Throttle'], label='BOT')
ax[1].plot(telemetry_ham['Distance'], telemetry_ham['Throttle'], label='HAM')
ax[1].set(ylabel='Throttle')

# Plot brakes
ax[2].plot(telemetry_bot['Distance'], telemetry_bot['Brake'], label='BOT')
ax[2].plot(telemetry_ham['Distance'], telemetry_ham['Brake'], label='HAM')
ax[2].set(ylabel='Brakes')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()

plt.xlabel('Distance')
plt.show()

# Display the map
map_zandvoort











