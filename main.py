import streamlit as st

print("hello")
# Import necessary libraries
import ee
import geopy

# Initialize the Earth Engine API
ee.Authenticate()
ee.Initialize(project="1030170391022")

# Function to get the coordinates of a city using Geopy
def get_city_coordinates(city_name):
    geolocator = geopy.Photon(user_agent="pacc-24")
    location = geolocator.geocode(city_name)
    return location.latitude, location.longitude


# Function to get climate data for a given city
def get_climate_data(city_name):
    # Get city coordinates
    lat, lon = get_city_coordinates(city_name)

    # Define the point of interest
    point = ee.Geometry.Point(lon, lat)

    # Load a dataset, for example, the ERA5 Daily Aggregate dataset for temperature
    dataset = ee.ImageCollection('ECMWF/ERA5/DAILY') \
        .filterBounds(point) \
        .filterDate('2023-01-01', '2023-12-31')

    # Select the temperature band (2m air temperature)
    temperature = dataset.select('mean_2m_air_temperature')

    # Calculate the mean temperature for the year
    mean_temp = temperature.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=1000
    )

    # Get the temperature in Celsius
    # temp_celsius = mean_temp.get('mean_2m_air_temperature').getInfo() - 273.15

    return temperature


# Example usage
city_name = 'Los Angeles'
temperature = get_climate_data(city_name)
print(f'The mean temperature for {city_name} in 2023 is {temperature}°C')

st.text("world")
