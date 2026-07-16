from flask import Blueprint, render_template, send_file, jsonify
from app.services.report_generator import CaseReportGenerator

police_bp = Blueprint('police', __name__, url_prefix='/police')

@police_bp.route('/dashboard')
def dashboard():
    # Simulation dashboard feed containing system state data
    active_cases = [
        {"id": "CS-2026-8841", "type": "Digital Arrest Scam", "score": 94, "status": "Critical Impact", "city": "Lucknow"},
        {"id": "CS-2026-7739", "type": "UPI Mirror Fraud", "score": 78, "status": "Under Evaluation", "city": "Delhi"},
        {"id": "CS-2026-3120", "type": "Instant Loan Extortion", "score": 88, "status": "Active Wiretap", "city": "Mumbai"},
        {"id": "CS-2026-1102", "type": "FedEx Package Trap", "score": 42, "status": "Deferred", "city": "Bangalore"}
    ]
    return render_template('police_dashboard.html', title="Precinct Commander Control Center", cases=active_cases)

@police_bp.route('/api/telemetry')
def analytics_telemetry():
    """Provides Chart.js mapping data aggregates representing weekly fraud footprints."""
    return jsonify({
        "categories": ["Digital Arrest", "UPI Fraud", "Loan Traps", "Fake KYC", "FedEx Scams"],
        "category_counts": [142, 389, 94, 210, 65],
        "timeline_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "timeline_data": [45, 62, 55, 84, 98, 110, 135],
        "risk_distribution": [35, 45, 20] # High, Medium, Low percentages
    })

@police_bp.route('/report/download/<case_id>')
def download_case_dossier(case_id):
    """Generates and pipes dynamic structural PDF evidence files down to request target."""
    
    # In production, queries the structural ORM database models built in Phase 1
    mock_case_payload = {
        "case_id": case_id,
        "classification": "RESTRICTED LAW ENFORCEMENT FORENSICS",
        "scam_type": "Digital Arrest Syndicate / Fake CBI Extortion",
        "threat_score": 94,
        "location": "Uttar Pradesh Cyber Crime Cell HQ",
        "status": "Active Operational Interdiction",
        "summary": "Target citizen was placed under unauthorized coercive confinement by adversaries posing as federal CBI officers via digital video applications. The target was forced into transferring structural liquidity positions under duress.",
        "analysis": "LLM signature detection identifies specific linguistic frameworks mapping closely to cross-border operations. Core operations indicate routing through complex multi-layered VPN nodes coupled with instant outward clearing mule accounts.",
        "entities": [
            {"value": "+91-9876543210", "type": "Inbound Mobile Route", "risk": "CRITICAL RISK MATCH"},
            {"value": "police.secure@ybl", "type": "Financial Layer 1 (Mule UPI)", "risk": "HIGH SUSPICION RATING"},
            {"value": "103.15.22.45", "type": "Egress Gateway Proxy IP", "risk": "VERIFIED EXPLOIT SOURCE"}
        ],
        "recommendation": "Initiate automated freezing directives to central banking clearinghouses. Dispatched trace indicators to mobile carriage providers to identify base station location sequences."
    }
    
    pdf_buffer = CaseReportGenerator.generate_pdf(mock_case_payload)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"CyberShield_Forensic_Dossier_{case_id}.pdf",
        mimetype="application/pdf"
    )