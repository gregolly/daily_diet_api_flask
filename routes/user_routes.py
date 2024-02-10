from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from flask_login import login_user, current_user, logout_user, login_required
from bcrypt import hashpw, gensalt, checkpw

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and checkpw(str.encode(password), user.password):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "You have been logged in!"})

    return jsonify({"message": "Username or password are incorrect!"}), 400

@user_bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been logged out"})

@user_bp.route("/user", methods=['POST'])
# @login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = hashpw(str.encode(password), gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered with successful"})

    return jsonify({"message": "Invalid data"}), 400

@user_bp.route("/user/<int:id>", methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get(id)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/user/<int:id>", methods=['PUT'])
@login_required
def update_user(id):
    data = request.json
    user = User.query.get(id)

    if id != current_user.id and current_user.role == "user":
        return jsonify({"message": "You cannot change password of another user"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        # user.role = data.get("role")
        db.session.commit()
        return jsonify({"message": f"User {id} has been updated successful"})
    
    return jsonify({"message": "User not found"}), 404 

@user_bp.route("/user/<int:id>", methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)

    if current_user.role != "admin":
        return jsonify({"message": "You cannot delete another user"}), 403
    
    if id == current_user.id:
        return jsonify({"message": "You cannot delete a logged in user"})
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {id} has been deleted successful"})
    
    return jsonify({"message": "User not found"}), 404 