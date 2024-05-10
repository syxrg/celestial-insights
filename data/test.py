import pandas as pd
import numpy as np

data = pd.read_csv('cleaned_data.csv')
print(data['apparent_magnitude'].min())
print(data['apparent_magnitude'].max())

print(data['absolute_magnitude'].min())
print(data['absolute_magnitude'].max())

data['right_ascension'] = pd.to_numeric(
    data['right_ascension'], errors='coerce')
data['declination'] = pd.to_numeric(data['declination'], errors='coerce')
data['apparent_magnitude'] = pd.to_numeric(
    data['apparent_magnitude'], errors='coerce')
data['absolute_magnitude'] = pd.to_numeric(
    data['absolute_magnitude'], errors='coerce')
data['distance_light_year'] = pd.to_numeric(
    data['distance_light_year'], errors='coerce')


ra_range = [6.0, 16.0]  # Example values for Right Ascension range
dec_range = [-90, 90.0]  # Example values for Declination range
appmag_range = [-1.46, 2.0]  # Example values for Apparent Magnitude range
absmag_range = [-6.5, -2.8]  # Example values for Absolute Magnitude range
dist_range = [2500.0, 4500.0]  # Example values for Distance range

# Applying filters to check how many records match the given criteria
filtered_data = data[
    (data['right_ascension'].between(*ra_range)) &
    (data['declination'].between(*dec_range)) &
    (data['apparent_magnitude'].between(*appmag_range))
]

# Print the size of filtered data and some example rows to verify
print(f"Filtered data size: {len(filtered_data)} records")
if not filtered_data.empty:
    print("Sample of filtered data:")
    print(filtered_data.head())
