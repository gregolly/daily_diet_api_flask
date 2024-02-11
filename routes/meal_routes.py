from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from database import db
from models.meal import Meal
from models.user import User
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
            hour = datetime.strptime(hour, "%H:%M").strftime("%H:%M")
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

@meal_bp.route("/all/<int:id>", methods=['GET'])
@login_required
def get_meals(id):
    user = User.query.get(id)
    meals = Meal.query.all()

    if user and current_user.is_authenticated:
        meals = Meal.query.filter_by(user_id=id).all()

        meal_list = []
        for meal in meals:
            meal_data = {
                "title": meal.title,
                "description": meal.description,
                "date": meal.date,
                "hour": meal.hour,
                "onDiet": meal.onDiet
            }
            meal_list.append(meal_data)
        return jsonify(meal_list)

    return jsonify({"message": "unauthorized"})

@meal_bp.route("/<int:id>", methods=['PUT'])
@login_required
def update_meal(id):
    data = request.json
    meal = Meal.query.get(id)

    if not current_user.is_authenticated:
        return jsonify({"message": "You cannot change meal of another user"}), 403
    
    if meal and data.get("title"):
        meal.title = data.get("title")
        meal.description = data.get("description")
        meal.date = datetime.strptime(data.get("date"), "%d/%m/%Y") if data.get("date") else meal.date
        meal.hour = datetime.strptime(data.get("hour"), "%H:%M").strftime("%H:%M") if data.get("hour") else meal.hour
        meal.onDiet = data.get("onDiet")
        db.session.commit()
        return jsonify({"message": f"Meal {id} has been updated successful"})
    
    return jsonify({"message": "Meal not found"}), 404 
    
@meal_bp.route("/<int:id>", methods=['DELETE'])
@login_required
def delete_meal(id):
    meal = Meal.query.get(id)
    
    if meal:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": f"Meal {id} has been deleted successful"})
    
    return jsonify({"message": "User not found"}), 404

