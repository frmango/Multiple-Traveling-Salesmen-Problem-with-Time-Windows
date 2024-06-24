import googlemaps
from datetime import datetime
import pandas as pd

def get_travel_time(api_key, start_address, end_address, mode='driving'):
    """
    Fetches the travel time between two addresses using the Google Maps Directions API.

    Args:
    api_key (str): Google Maps API key
    start_address (str): Starting address
    end_address (str): Destination address
    mode (str): Mode of transportation

    Returns:
    int: Travel time in minutes
    """
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    directions_result = gmaps.directions(start_address, end_address, mode=mode, departure_time=now)
    duration = directions_result[0]['legs'][0]['duration']['value']  # Travel time in seconds
    travel_time_minutes = duration // 60
    return travel_time_minutes

def calculate_brand_travel_time_matrix(data, api_key):
    """
    Calculates the travel time matrix for a list of brands and their addresses.

    Args:
    data (DataFrame): DataFrame containing 'Marque' and 'Adresse' columns
    api_key (str): Google Maps API key

    Returns:
    DataFrame: Travel time matrix
    """
    gmaps = googlemaps.Client(key=api_key)
    brand_to_address = data.set_index('Marque')['Adresse'].to_dict()
    unique_brands = data['Marque'].unique()
    travel_times = pd.DataFrame(index=unique_brands, columns=unique_brands, dtype=int)
    cache = {}  # Cache to store previously computed travel times

    for origin_brand in unique_brands:
        for destination_brand in unique_brands:
            if origin_brand != destination_brand:
                origin_address = brand_to_address[origin_brand]
                destination_address = brand_to_address[destination_brand]
                address_pair = tuple(sorted([origin_address, destination_address]))
                if address_pair not in cache:
                    travel_time = get_travel_time(api_key, origin_address, destination_address)
                    cache[address_pair] = travel_time
                else:
                    travel_time = cache[address_pair]
                travel_times.loc[origin_brand, destination_brand] = travel_time

    return travel_times
