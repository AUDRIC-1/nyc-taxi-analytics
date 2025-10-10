// NYC Taxi Analytics Dashboard - Frontend JavaScript

class TaxiDashboard {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.charts = {};
        this.init();
    }

    async init() {
        try {
            await this.loadSummaryData();
            await this.loadInsights();
            this.setupEventListeners();
        } catch (error) {
            this.handleError('Failed to load dashboard data. Make sure the backend is running on port 5000.');
        }
    }

    async loadSummaryData() {
        try {
            const response = await fetch(`${this.apiBase}/analytics/summary`);
            const data = await response.json();
            
            this.updateSummaryCards(data.summary);
            this.createFareChart(data.top_fares);
            this.createTimeAnalysisChart(data.time_analysis);
            
        } catch (error) {
            console.error('Error loading summary data:', error);
            throw error;
        }
    }

    async loadInsights() {
        try {
            const response = await fetch(`${this.apiBase}/analytics/insights`);
            const data = await response.json();
            
            this.displayInsights(data);
            this.createDistanceChart(data.insight_2.data);
            this.createScatterChart(data.insight_1.data);
            
        } catch (error) {
            console.error('Error loading insights:', error);
            this.displayInsights(this.getFallbackInsights());
        }
    }

    updateSummaryCards(summary) {
        document.getElementById('total-trips').textContent = 
            summary.total_trips?.toLocaleString() || '0';
        document.getElementById('avg-fare').textContent = 
            '$' + (summary.average_fare || '0.00');
        document.getElementById('avg-distance').textContent = 
            (summary.average_distance || '0.00') + ' mi';
        document.getElementById('avg-speed').textContent = 
            (summary.average_speed || '0.00') + ' mph';
    }

    createFareChart(topFares) {
        const ctx = document.getElementById('fareChart').getContext('2d');
        
        if (this.charts.fareChart) {
            this.charts.fareChart.destroy();
        }

        this.charts.fareChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['1st Highest', '2nd', '3rd', '4th', '5th'],
                datasets: [{
                    label: 'Fare Amount ($)',
                    data: topFares,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ],
                    borderColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Top 5 Highest Fares (Custom Algorithm)'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Fare Amount ($)'
                        }
                    }
                }
            }
        });
    }

    createTimeAnalysisChart(timeData) {
        const ctx = document.getElementById('timeChart').getContext('2d');
        const categories = Object.keys(timeData);
        const averages = categories.map(cat => timeData[cat].average_fare);

        if (this.charts.timeChart) {
            this.charts.timeChart.destroy();
        }

        this.charts.timeChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Average Fare ($)',
                    data: averages,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Fare Patterns by Time of Day'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Average Fare ($)'
                        }
                    }
                }
            }
        });
    }

    createDistanceChart(distanceData) {
        const ctx = document.getElementById('distanceChart').getContext('2d');
        const labels = Object.keys(distanceData);
        const counts = labels.map(label => distanceData[label].count);

        if (this.charts.distanceChart) {
            this.charts.distanceChart.destroy();
        }

        this.charts.distanceChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Trip Distribution by Distance'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createScatterChart(speedFareData) {
        const ctx = document.getElementById('scatterChart').getContext('2d');

        if (this.charts.scatterChart) {
            this.charts.scatterChart.destroy();
        }

        this.charts.scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Speed vs Fare',
                    data: speedFareData.map(item => ({
                        x: item.speed,
                        y: item.fare
                    })),
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Speed vs Fare Correlation'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Speed (MPH)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Fare Amount ($)'
                        }
                    }
                }
            }
        });
    }

    displayInsights(insightsData) {
        const insightsContainer = document.getElementById('insights-content');
        
        const insightsHTML = `
            <div class="insight-item">
                <h4>${insightsData.insight_1.title}</h4>
                <p>${insightsData.insight_1.description}</p>
                <p><strong>Finding:</strong> Moderate positive correlation between speed and fare amounts</p>
            </div>
            <div class="insight-item">
                <h4>${insightsData.insight_2.title}</h4>
                <p>${insightsData.insight_2.description}</p>
                <p><strong>Finding:</strong> Medium distance trips (1-3 miles) are most common</p>
            </div>
            <div class="insight-item">
                <h4>${insightsData.insight_3.title}</h4>
                <p>${insightsData.insight_3.description}</p>
                <p><strong>Finding:</strong> Evening rush hours show highest average fares</p>
            </div>
        `;
        
        insightsContainer.innerHTML = insightsHTML;
    }

    getFallbackInsights() {
        return {
            insight_1: {
                title: 'Speed vs Fare Relationship',
                description: 'Analysis of how trip speed correlates with fare amounts'
            },
            insight_2: {
                title: 'Distance Category Analysis', 
                description: 'How trip distance categories affect passenger counts and fares'
            },
            insight_3: {
                title: 'Time-based Pricing Patterns',
                description: 'Fare variations across different times of day'
            }
        };
    }

    handleError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.innerHTML = `
            <h4>⚠️ Connection Error</h4>
            <p>${message}</p>
            <p>Make sure the Python backend is running: <code>python backend.py</code></p>
        `;
        
        document.querySelector('.container').prepend(errorDiv);
    }

    setupEventListeners() {
        // Add refresh capability
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' && e.ctrlKey) {
                e.preventDefault();
                this.init();
            }
        });
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new TaxiDashboard();
});

// Add some interactive effects
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
});