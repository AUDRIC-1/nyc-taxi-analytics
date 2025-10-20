import csv
import math
from datetime import datetime

INPUT = "train.csv"
CLEAN_OUT = "cleaned_taxi.csv"
LOG = "invalid_records.log"

# Column names
PICKUP = "pickup_datetime"
DROPOFF = "dropoff_datetime"
PLAT = "pickup_latitude"
PLON = "pickup_longitude"
DLAT = "dropoff_latitude"
DLON = "dropoff_longitude"
DURATION = "trip_duration"

# Bounding box for NYC (approx)
MIN_LAT, MAX_LAT = 40.4774, 40.9176
MIN_LON, MAX_LON = -74.2591, -73.7004

def haversine(lat1, lon1, lat2, lon2):
    """Return distance (km) between two lat/lon points."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def parse_dt(s):
    """Try to parse pickup/dropoff datetime."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None

with open(INPUT, newline='', encoding='utf-8') as infile, \
     open(CLEAN_OUT, 'w', newline='', encoding='utf-8') as cleanfile, \
     open(LOG, 'w', newline='', encoding='utf-8') as logfile:

    reader = csv.DictReader(infile)
    out_fields = reader.fieldnames + ["distance_km", "trip_speed_kmh", "rush_hour"]
    writer = csv.DictWriter(cleanfile, fieldnames=out_fields)
    writer.writeheader()

    log_fields = reader.fieldnames + ["reason"]
    log_writer = csv.DictWriter(logfile, fieldnames=log_fields)
    log_writer.writeheader()

    for row in reader:
        try:
            plat = float(row[PLAT])
            plon = float(row[PLON])
            dlat = float(row[DLAT])
            dlon = float(row[DLON])
        except:
            row["reason"] = "bad_coords"
            log_writer.writerow(row)
            continue

        # Check coordinate bounds
        if not (MIN_LAT <= plat <= MAX_LAT and MIN_LON <= plon <= MAX_LON and
                MIN_LAT <= dlat <= MAX_LAT and MIN_LON <= dlon <= MAX_LON):
            row["reason"] = "out_of_bbox"
            log_writer.writerow(row)
            continue

        # Parse times
        ptime = parse_dt(row[PICKUP])
        dtime = parse_dt(row[DROPOFF])
        if not ptime or not dtime or dtime <= ptime:
            row["reason"] = "bad_datetime"
            log_writer.writerow(row)
            continue

        # Trip duration (if not empty)
        try:
            duration_s = float(row[DURATION])
        except:
            row["reason"] = "bad_duration"
            log_writer.writerow(row)
            continue
        if duration_s <= 0:
            row["reason"] = "nonpositive_duration"
            log_writer.writerow(row)
            continue

        # Compute distance (km)
        distance_km = haversine(plat, plon, dlat, dlon)
        if distance_km <= 0:
            row["reason"] = "zero_distance"
            log_writer.writerow(row)
            continue

        # Compute speed
        hours = duration_s / 3600
        trip_speed_kmh = distance_km / hours
        if trip_speed_kmh <= 0 or trip_speed_kmh > 200:
            row["reason"] = "invalid_speed"
            log_writer.writerow(row)
            continue

        # Rush hour (7–9 or 17–19)
        hour = ptime.hour
        rush_hour = 1 if hour in [7, 8, 17, 18] else 0

        # Add new fields
        row["distance_km"] = round(distance_km, 2)
        row["trip_speed_kmh"] = round(trip_speed_kmh, 2)
        row["rush_hour"] = rush_hour

        writer.writerow(row)
