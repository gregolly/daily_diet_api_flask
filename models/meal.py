from database import db
from datetime import datetime
class Meal(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime(), nullable=False)
    hour = db.Column(db.DateTime(), default=db.func.now() nullable=False)
    onDiet = db.Column(db.Boolean, nullable=False)
    user_id = db.relationship("User", back_populates="meals", foreign_keys="[User.id]")
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False) 
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.utcnow(), onupdate=db.func.utcnow(), nullable=False)