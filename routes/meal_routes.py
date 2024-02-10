from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from database import db
from models.meal import Meal
from datetime import datetime

meal_bp = Blueprint('meal_bp', __name__)

@meal_bp.route("/", methods=['POST'])
@login_required
def create_meal():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    date = data.get("date")
    hour = data.get("hour")
    onDiet = data.get("onDiet")

    if title and date and hour:
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            hour = datetime.strptime(hour, "%H:%M").time()
        except ValueError as e:
            print(f"Error parsing date or hour: {e}")
            return jsonify({"message": "Invalid date or hour format"}), 400
        
        if current_user.is_authenticated:
            user_id = current_user.id

            meal = Meal(
                title=title, 
                description=description, 
                date=date, 
                hour=hour, 
                onDiet=onDiet, 
                user_id=user_id,
            )

            db.session.add(meal)
            db.session.commit()

            return jsonify({"message": "Meal has been created successfully"})
    
    return jsonify({"message": "Invalid data"}), 400

@meal_bp.route("/<int:id>", methods=['GET'])
def get_meal(id):
    meal = Meal.query.get(id)

    if meal:
        return {
            "title": meal.title,
            "description": meal.description,
            "date": meal.date,
            "hour": meal.hour,
            "onDiet": meal.onDiet
        }
    
    return jsonify({"message": "Meal not found"}), 404

