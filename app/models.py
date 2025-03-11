from app.database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    timezone = db.Column(db.String(20), nullable=False)
    replied = db.Column(db.Boolean(), default=False)

    def __init__(self, name, email, mobile, timezone, replied=False):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.timezone = timezone
        self.replied = replied