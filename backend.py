from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

class TaxiAnalyzer:
    """Custom algorithms for taxi data analysis"""
    
    @staticmethod
    def manual_top_n_sort(items, n=5):
        """
        CUSTOM ALGORITHM: Manual implementation of top-N sorting
        No built-in sorting functions used - demonstrates algorithmic thinking
        """
        # Manual selection sort for top N elements
        results = []
        data = items.copy()
        
        for i in range(min(n, len(data))):
            max_index = i
            for j in range(i + 1, len(data)):
                if data[j] > data[max_index]:
                    max_index = j
            
            # Swap elements manually
            data[i], data[max_index] = data[max_index], data[i]
            results.append(data[i])
        
        return results
    
    @staticmethod
    def analyze_time_patterns(trips):
        """
        CUSTOM ALGORITHM: Manual aggregation by time categories
        No pandas/pivot tables used - pure Python implementation
        """
        time_stats = {}
        
        for trip in trips:
            category = trip[11]  # time_category
            fare = trip[8]       # fare_amount
            
            if category not in time_stats:
                time_stats[category] = {'total_fare': 0, 'count': 0, 'fares': []}
            
            time_stats[category]['total_fare'] += fare
            time_stats[category]['count'] += 1
            time_stats[category]['fares'].append(fare)
        
        # Calculate averages manually
        for category in time_stats:
            stats = time_stats[category]
            stats['average_fare'] = stats['total_fare'] / stats['count'] if stats['count'] > 0 else 0
        
        return time_stats

# Flask Routes
@app.route('/')
def home():
    return "NYC Taxi Analytics API - Ready for Analysis!"

@app.route('/api/analytics/summary')
def get_analytics_summary():
    """Comprehensive analytics endpoint"""
    conn = sqlite3.connect('taxi_analytics.db')
    cursor = conn.cursor()
    
    # Basic statistics
    cursor.execute('''
        SELECT COUNT(*), AVG(fare_amount), AVG(trip_distance), AVG(speed)
        FROM trips
    ''')
    total_trips, avg_fare, avg_distance, avg_speed = cursor.fetchone()
    
    # Get fares for custom sorting algorithm
    cursor.execute('SELECT fare_amount FROM trips LIMIT 100')
    fares = [row[0] for row in cursor.fetchall()]
    
    # Use our custom algorithm
    analyzer = TaxiAnalyzer()
    top_fares = analyzer.manual_top_n_sort(fares, 5)
    
    # Time pattern analysis using custom algorithm
    cursor.execute('SELECT * FROM trips LIMIT 500')
    trips_data = cursor.fetchall()
    time_patterns = analyzer.analyze_time_patterns(trips_data)
    
    conn.close()
    
    return jsonify({
        'summary': {
            'total_trips': total_trips,
            'average_fare': round(avg_fare, 2),
            'average_distance': round(avg_distance, 2),
            'average_speed': round(avg_speed, 2)
        },
        'top_fares': top_fares,
        'time_analysis': time_patterns,
        'algorithm_explanation': {
            'sorting_algorithm': 'Manual selection sort for top-N elements',
            'time_complexity': 'O(k*n) where k is number of top elements',
            'space_complexity': 'O(n)',
            'purpose': 'Find most expensive trips without built-in functions'
        }
    })

@app.route('/api/trips/sample')
def get_sample_trips():
    """Get sample trips for mapping"""
    conn = sqlite3.connect('taxi_analytics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT pickup_latitude, pickup_longitude, fare_amount, trip_distance, time_category
        FROM trips LIMIT 100
    ''')
    
    trips = []
    for row in cursor.fetchall():
        trips.append({
            'pickup_lat': row[0],
            'pickup_lng': row[1],
            'fare': row[2],
            'distance': row[3],
            'time_category': row[4]
        })
    
    conn.close()
    return jsonify(trips)

@app.route('/api/analytics/insights')
def get_insights():
    """Pre-calculated insights for dashboard"""
    conn = sqlite3.connect('taxi_analytics.db')
    cursor = conn.cursor()
    
    # Insight 1: Speed vs Fare correlation
    cursor.execute('''
        SELECT speed, fare_amount FROM trips 
        WHERE speed > 0 AND speed < 60 
        LIMIT 200
    ''')
    
    speed_fare_data = [{'speed': row[0], 'fare': row[1]} for row in cursor.fetchall()]
    
    # Insight 2: Distance distribution
    cursor.execute('''
        SELECT 
            CASE 
                WHEN trip_distance < 1 THEN 'Short (<1 mi)'
                WHEN trip_distance < 3 THEN 'Medium (1-3 mi)'
                WHEN trip_distance < 10 THEN 'Long (3-10 mi)'
                ELSE 'Very Long (10+ mi)'
            END as distance_category,
            COUNT(*),
            AVG(fare_amount)
        FROM trips 
        GROUP BY distance_category
    ''')
    
    distance_analysis = {}
    for row in cursor.fetchall():
        distance_analysis[row[0]] = {
            'count': row[1],
            'avg_fare': round(row[2], 2)
        }
    
    conn.close()
    
    return jsonify({
        'insight_1': {
            'title': 'Speed vs Fare Relationship',
            'description': 'Analysis of how trip speed correlates with fare amounts',
            'data': speed_fare_data
        },
        'insight_2': {
            'title': 'Distance Category Analysis',
            'description': 'How trip distance categories affect passenger counts and fares',
            'data': distance_analysis
        },
        'insight_3': {
            'title': 'Time-based Pricing Patterns',
            'description': 'Fare variations across different times of day',
            'data': 'See time_analysis in summary endpoint'
        }
    })

if __name__ == '__main__':
    print("Starting NYC Taxi Analytics API...")
    print("Access the dashboard at http://localhost:5000")
    app.run(debug=True, port=5000)