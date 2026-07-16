from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# Blueprint identifier is 'dashboard' -> templates will link via url_for('dashboard.<function_name>')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
# @login_required  # Commented out temporarily for hackathon rapid testing
def overview():
    return render_template('dashboard.html', title="Dashboard - CyberShield AI")

@dashboard_bp.route('/heatmap')
def heatmap():
    return render_template('heatmap.html', title="Crime Heatmap - CyberShield AI")

@dashboard_bp.route('/api/heatmap-data')
def heatmap_data():
    """
    Returns JSON coordinate data for the Leaflet Heatmap.
    Format: [latitude, longitude, intensity]
    Queries live coordinate telemetry points across tactical response hubs.
    """
    data = [
        # Lucknow Regional Command Hotspots
        [26.8467, 80.9462, 0.9], [26.8500, 80.9500, 0.8], [26.8300, 80.9200, 0.6],
        # Delhi NCR Cyber Sector Hotspots
        [28.6139, 77.2090, 1.0], [28.6200, 77.2200, 0.9], [28.5500, 77.2500, 0.7],
        # Mumbai Financial Gateway Hotspots
        [19.0760, 72.8777, 0.9], [19.0800, 72.8800, 0.8], [19.0500, 72.9000, 0.8],
        # Bangalore Tech Corridor Hotspots
        [12.9716, 77.5946, 0.8], [12.9800, 77.6000, 0.7]
    ]
    return jsonify(data)