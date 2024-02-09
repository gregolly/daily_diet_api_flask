from database import db
from datetime import datetime
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime(), nullable=False)
    hour = db.Column(db.DateTime(), nullable=False)
    onDiet = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="meals")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)