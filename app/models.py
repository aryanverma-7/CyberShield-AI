from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='citizen') # 'admin', 'police', 'citizen'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    complaints = db.relationship('Complaint', backref='author', lazy='dynamic')

class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Investigating') # 'Resolved', 'High Risk'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location_state = db.Column(db.String(50))
    location_district = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    evidence = db.relationship('Evidence', backref='complaint', lazy='dynamic')
    threat_report = db.relationship('ThreatReport', backref='complaint', uselist=False)

class Evidence(db.Model):
    __tablename__ = 'evidence'
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))
    file_type = db.Column(db.String(20)) # 'image', 'audio', 'pdf', 'text'
    file_path = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text) # OCR/Whisper output
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class ThreatReport(db.Model):
    __tablename__ = 'threat_reports'
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'))
    scam_category = db.Column(db.String(50)) # 'Digital Arrest', 'UPI Fraud', etc.
    threat_score = db.Column(db.Float) # 0.0 to 100.0
    confidence_score = db.Column(db.Float)
    analysis_summary = db.Column(db.Text)
    recommended_action = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class GraphNode(db.Model):
    __tablename__ = 'graph_nodes'
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50)) # 'Phone', 'UPI', 'IP'
    entity_value = db.Column(db.String(150), unique=True, index=True)
    risk_level = db.Column(db.String(20)) # 'Safe', 'Suspicious', 'Malicious'
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)