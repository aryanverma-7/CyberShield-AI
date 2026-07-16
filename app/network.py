from flask import Blueprint, render_template, jsonify

network_bp = Blueprint('network', __name__, url_prefix='/network')

@network_bp.route('/visualize')
def visualize():
    return render_template('threat_network.html', title="Threat Topology - CyberShield AI")

@network_bp.route('/api/network-data')
def network_data():
    """
    Returns nodes and edges mapping a simulated synergistic fraud ring.
    Groups: 'leader' (Red), 'mule' (Orange), 'comm' (Blue), 'victim' (Green)
    """
    network_matrix = {
        "nodes": [
            {"id": 1, "label": "Mewat Core Gateway [Node-X]", "group": "leader", "size": 25},
            {"id": 2, "label": "Mule Acct: SBI ...8841", "group": "mule", "size": 16},
            {"id": 3, "label": "Mule Acct: HDFC ...9021", "group": "mule", "size": 16},
            {"id": 4, "label": "+91 98765-XXXXX (WhatsApp Vector)", "group": "comm", "size": 14},
            {"id": 5, "label": "+91 81234-XXXXX (VoIP Gateway)", "group": "comm", "size": 14},
            {"id": 6, "label": "Victim Record #2026-A", "group": "victim", "size": 12},
            {"id": 7, "label": "Victim Record #2026-B", "group": "victim", "size": 12}
        ],
        "edges": [
            {"from": 1, "to": 2, "arrows": "to", "label": "Fund Route"},
            {"from": 1, "to": 3, "arrows": "to", "label": "Fund Route"},
            {"from": 1, "to": 4, "arrows": "from", "label": "Command Link"},
            {"from": 1, "to": 5, "arrows": "from", "label": "Command Link"},
            {"from": 4, "to": 6, "arrows": "to", "label": "Phishing Line"},
            {"from": 5, "to": 7, "arrows": "to", "label": "Digital Arrest Call"},
            {"from": 2, "to": 6, "arrows": "from", "label": "Escrow Intercept"}
        ]
    }
    return jsonify(network_matrix)