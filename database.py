import sqlite3
from data_cleaning import clean_and_process_data

def setup_database():
    """Create and setup the database with normalized schema"""
    conn = sqlite3.connect('taxi_analytics.db')
    cursor = conn.cursor()
    
    # Create tables with normalized schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id TEXT PRIMARY KEY,
            pickup_datetime TEXT,
            passenger_count INTEGER,
            trip_distance REAL,
            pickup_latitude REAL,
            pickup_longitude REAL,
            dropoff_latitude REAL,
            dropoff_longitude REAL,
            fare_amount REAL,
            trip_duration REAL,
            speed REAL,
            fare_per_mile REAL,
            time_category TEXT
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fare ON trips(fare_amount)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_distance ON trips(trip_distance)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_time ON trips(pickup_datetime)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_speed ON trips(speed)')
    
    conn.commit()
    return conn

def insert_data(conn, trips):
    """Insert cleaned data into database"""
    cursor = conn.cursor()
    
    for trip in trips:
        cursor.execute('''
            INSERT OR REPLACE INTO trips 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trip['id'], trip['pickup_datetime'], trip['passenger_count'],
            trip['trip_distance'], trip['pickup_lat'], trip['pickup_lng'],
            trip['dropoff_lat'], trip['dropoff_lng'], trip['fare_amount'],
            trip['trip_duration'], trip['speed'], trip['fare_per_mile'],
            trip['time_category']
        ))
    
    conn.commit()
    print(f"Inserted {len(trips)} trips into database")

def get_database_stats(conn):
    """Get basic database statistics"""
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*), AVG(fare_amount), AVG(trip_distance) FROM trips')
    count, avg_fare, avg_distance = cursor.fetchone()
    
    print(f"Database Stats: {count} trips, Average Fare: ${avg_fare:.2f}, Average Distance: {avg_distance:.2f} miles")

if __name__ == "__main__":
    print("Setting up database...")
    conn = setup_database()
    
    print("Processing data...")
    trips = clean_and_process_data()
    
    print("Inserting data...")
    insert_data(conn, trips)
    
    get_database_stats(conn)
    conn.close()
    print("Database setup complete!")