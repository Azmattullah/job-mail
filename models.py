from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EmailSendLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_email = db.Column(db.String(120), nullable=False)
    receiver_name = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
