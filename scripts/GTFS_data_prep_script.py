#GTFS data preperation script
# NOTE:
# This script processes the full Luxembourg GTFS feed (national scale).
# Results are not limited to Luxembourg City unless spatially filtered.

import pandas as pd
import geopandas as gpd
import os
import numpy as np
import sys



def data_load(base_path):
    GTFS_data = {}
    for file in os.listdir(base_path):
        if file.endswith(".txt"):
            name = file.replace(".txt", "")
            full_path = os.path.join(base_path, file)
            GTFS_data[name] = pd.read_csv(full_path)
    return GTFS_data

def data_validation(stops,stop_times,trips,calendar):
    logic_checks = [
        trips['service_id'].isin(calendar['service_id']).all(),
        stop_times['trip_id'].isin(trips['trip_id']).all(),
        stop_times['stop_id'].isin(stops['stop_id']).all()
        ]

    if not all(logic_checks):
        raise ValueError("GTFS ID relationship check failed")

    #Trip IDs should dupilcate for stop_times and stop_ID should duplicate for trips
    unique_checks = [
        stops['stop_id'].is_unique,
        trips['trip_id'].is_unique
    ]

    if not all(unique_checks):
        raise ValueError("ID unqiueness check failed")

    #Check if stop order is logical
    chrono = stop_times.sort_values(['trip_id', 'stop_sequence'])
    chrono['stop_sequence'] = pd.to_numeric(chrono['stop_sequence'])

    if (
        (chrono.groupby('trip_id')['stop_sequence'].diff() <= 0) |
        (chrono.groupby('trip_id')['departure_time'].diff() < pd.Timedelta(0))
    ).any():
        raise ValueError("Stop order check failed")
    
def data_cleaning(stops,stop_times,trips,calendar):
    stops = stops.dropna(subset=['stop_lat','stop_lon'])
    stops = stops[(stops['stop_lat']!= 0) & (stops['stop_lon']!= 0)]

    #Next, validate ID types
    stops['stop_id'] = stops['stop_id'].astype(str)
    stop_times[['stop_id','trip_id']] = stop_times[['stop_id','trip_id']].astype(str)
    trips[['service_id','trip_id']] = trips[['service_id','trip_id']].astype(str)
    calendar['service_id'] = calendar['service_id'].astype(str)

    #Convert stop times into seconds for normalisation
    stop_times["dep_sec"] = pd.to_timedelta(stop_times["departure_time"]).dt.total_seconds()
    stop_times["arr_sec"] = pd.to_timedelta(stop_times["arrival_time"]).dt.total_seconds()

    #Finally drop duplicates
    stop_times = stop_times.drop_duplicates(subset=["trip_id", "stop_sequence"])
    return stops,stop_times,trips,calendar

def filter_weekday(trips,calendar):
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    weekday_ids = calendar[weekdays].eq(1).all(axis=1)
    weekday_ids = calendar.loc[weekday_ids, "service_id"]
    return trips[trips['service_id'].isin(weekday_ids)]

def filter_hours(stop_times):
    #Peak hours are 7-9 AM. We take morning commute and assume that evening commute is the same.
    peak_start = 3600*7
    peak_end = 3600*9


    peak_times = stop_times[stop_times['dep_sec'].between(peak_start, peak_end)]
    return peak_times

def build_events(peak_times,trips,stops):
    #Now that the data is clean and selected, we want to create a table that links the events together using the IDs: trips -> stop_times -> stops 
    #We use the stop times table for this since it has both trip and stop id, in this case it's the peak_times df

    events = peak_times.merge(trips, on ='trip_id', how = 'inner',validate="many_to_one")
    events = events.merge(stops,on='stop_id',how = 'inner',validate="many_to_one")
    return events

def freqeuncy(events):
    #In this step, we calcualte the number of departures for a stop and the average headway of the stop. 
    #These metrics are used when thinking about how often a commuter can get a bus to commute, more frequent lines are more accessible
    #Thus, we expect stops with a high departure time and low headway to be on lines which lead to business districts.
    #To perform this analysis, we used the stop_id is the key field.

    freq = events.groupby("stop_id")["dep_sec"].count().rename("n_departures").reset_index()

    #For headway calcualtions, we want average minutes per departure per stop.
    time_window = 120

    #We use an average headway calculation here because bus depature times are evenly spaced during peak hours.
    freq["avg_headway"] = time_window / freq["n_departures"]
    return freq

def create_output(stops, freq):
    #When creating the output, we want to use the stops dataset for the geodata so we use it as the main dataframe for merging
    #We only keep the necessary fields: ID, name and coordinates then join it to the freqency table we just made.

    stops = stops[["stop_id", "stop_name", "stop_lat", "stop_lon"]]

    stops_output = stops.merge(freq, on="stop_id", how="left")

    stops_output["n_departures"] = stops_output["n_departures"].fillna(0)
    stops_output['avg_headway'] = stops_output['avg_headway'].fillna(np.inf)

    #Create geodataframe and convert it to LUREF for analysis in meters
    stops_gdf = gpd.GeoDataFrame(stops_output, geometry=gpd.points_from_xy(stops_output.stop_lon, stops_output.stop_lat))
    stops_gdf = stops_gdf.set_crs(epsg=4326).to_crs(epsg=2169)

    return stops_gdf


def main():
    base_path = sys.argv[1]

    data = data_load(base_path)

    required = ["stops", "stop_times", "trips", "calendar"]
    for r in required:
        if r not in data:
            raise ValueError(f"Missing GTFS file: {r}.txt")

    stops = data["stops"]
    stop_times = data["stop_times"]
    trips = data["trips"]
    calendar = data["calendar"]

    stops, stop_times, trips, calendar = data_cleaning(stops, stop_times, trips, calendar)

    data_validation(stops, stop_times, trips, calendar)

    trips = filter_weekday(trips, calendar)
    peak_times = filter_hours(stop_times)
    if peak_times.empty:
        raise ValueError("No data in selected peak window")

    events = build_events(peak_times, trips, stops)

    freq = freqeuncy(events)

    gdf = create_output(stops, freq)

    output_path = os.path.join(base_path, "stops_freq.gpkg")
    gdf.to_file(output_path, driver="GPKG")


if __name__ == "__main__":
    main()