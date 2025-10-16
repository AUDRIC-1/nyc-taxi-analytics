from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend JS to fetch data

@app.route('/api/analytics/summary')
def summary():
    return jsonify({
        "summary": {
            "total_trips": 10000,
            "average_fare": 15.25,
            "average_distance": 2.8,
            "average_speed": 18.4
        },
        "top_fares": [52.5, 47.2, 45.1, 43.9, 41.7],
        "time_analysis": {
            "Morning": {"average_fare": 12.3},
            "Afternoon": {"average_fare": 14.5},
            "Evening": {"average_fare": 18.2},
            "Night": {"average_fare": 16.9}
        }
    })

@app.route('/api/analytics/insights')
def insights():
    return jsonify({
        "insight_1": {
            "title": "Speed vs Fare Correlation",
            "description": "Trips with higher average speed tend to have slightly higher fares.",
            "data": [{"speed": 10, "fare": 8}, {"speed": 20, "fare": 14}, {"speed": 30, "fare": 20}]
        },
        "insight_2": {
            "title": "Distance Distribution",
            "description": "Trips of 1-3 miles are the most common distance range.",
            "data": {"Short": {"count": 300}, "Medium": {"count": 550}, "Long": {"count": 150}}
        },
        "insight_3": {
            "title": "Time of Day Pricing",
            "description": "Evening hours show higher average fares."
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
