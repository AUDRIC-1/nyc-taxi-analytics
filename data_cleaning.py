import csv
import sqlite3

def clean_and_process_data():
    """Clean the raw NYC taxi data and create derived features"""
    print("Starting data cleaning...")
    
    cleaned_data = []
    skipped_records = 0
    
    try:
        with open('train.csv', 'r') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                # Basic data validation
                if (row['pickup_latitude'] and row['pickup_longitude'] and
                    row['trip_duration'] and row['trip_distance'] and
                    row['fare_amount']):
                    
                    try:
                        # Convert data types
                        pickup_lat = float(row['pickup_latitude'])
                        pickup_lng = float(row['pickup_longitude'])
                        duration = float(row['trip_duration'])
                        distance = float(row['trip_distance'])
                        fare = float(row['fare_amount'])
                        
                        # Data quality checks
                        if (duration > 0 and duration < 86400 and  # Reasonable duration (1 second to 24 hours)
                            distance > 0 and distance < 100 and     # Reasonable distance
                            fare > 0 and fare < 500 and            # Reasonable fare
                            -74.5 < pickup_lng < -73.5 and         # NYC longitude bounds
                            40.5 < pickup_lat < 41.0):             # NYC latitude bounds
                            
                            # DERIVED FEATURE 1: Speed (mph)
                            speed = (distance / (duration / 3600)) if duration > 0 else 0
                            
                            # DERIVED FEATURE 2: Fare per mile
                            fare_per_mile = fare / distance if distance > 0 else 0
                            
                            # DERIVED FEATURE 3: Time category
                            hour = int(row['pickup_datetime'].split(' ')[1].split(':')[0])
                            if 7 <= hour <= 9:
                                time_category = "Morning Rush"
                            elif 16 <= hour <= 18:
                                time_category = "Evening Rush"
                            elif 22 <= hour <= 24 or 0 <= hour <= 5:
                                time_category = "Late Night"
                            else:
                                time_category = "Normal Hours"
                            
                            cleaned_data.append({
                                'id': row['id'],
                                'pickup_datetime': row['pickup_datetime'],
                                'passenger_count': int(row['passenger_count']),
                                'trip_distance': distance,
                                'pickup_lat': pickup_lat,
                                'pickup_lng': pickup_lng,
                                'dropoff_lat': float(row['dropoff_latitude']),
                                'dropoff_lng': float(row['dropoff_longitude']),
                                'fare_amount': fare,
                                'trip_duration': duration,
                                'speed': speed,
                                'fare_per_mile': fare_per_mile,
                                'time_category': time_category
                            })
                        else:
                            skipped_records += 1
                    except:
                        skipped_records += 1
                else:
                    skipped_records += 1
                
                # Process only first 50,000 records for demo
                if i >= 50000:
                    break
                    
    except FileNotFoundError:
        print("Using sample data for demo...")
        # Generate sample data if file doesn't exist
        cleaned_data = generate_sample_data()
    
    print(f"Data cleaning complete. Kept: {len(cleaned_data)}, Skipped: {skipped_records}")
    return cleaned_data

def generate_sample_data():
    """Generate sample data if real CSV is not available"""
    sample_data = []
    for i in range(1000):
        sample_data.append({
            'id': f'trip_{i}',
            'pickup_datetime': '2023-01-01 10:30:00',
            'passenger_count': 2,
            'trip_distance': 3.5 + (i % 10),
            'pickup_lat': 40.75 + (i * 0.001),
            'pickup_lng': -73.99 + (i * 0.001),
            'dropoff_lat': 40.75 + (i * 0.001) + 0.01,
            'dropoff_lng': -73.99 + (i * 0.001) + 0.01,
            'fare_amount': 15.50 + (i % 20),
            'trip_duration': 1200 + (i * 30),
            'speed': 15 + (i % 10),
            'fare_per_mile': 4.5 + (i % 3),
            'time_category': ["Morning Rush", "Evening Rush", "Late Night", "Normal Hours"][i % 4]
        })
    return sample_data

if __name__ == "__main__":
    data = clean_and_process_data()
    print(f"Sample record: {data[0] if data else 'No data'}")