from database import db
from datetime import datetime
class Meal(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime(), nullable=False)
    hour = db.Column(db.DateTime(), nullable=False)
    onDiet = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="meals")
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False) 
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)