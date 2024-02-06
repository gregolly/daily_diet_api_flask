from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'
# Session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "You have been logged in!"})

    return jsonify({"message": "Username or password are incorrect!"}), 400

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been logged out"})

@app.route("/user", methods=['POST'])
# @login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered with successful"})

    return jsonify({"message": "Invalid data"}), 400

@app.route("/user/<int:id>", methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get(id)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:id>", methods=['PUT'])
@login_required
def update_user(id):
    data = request.json
    user = User.query.get(id)

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"User {id} has been updated successful"})
    
    return jsonify({"message": "User not found"}), 404 

@app.route("/user/<int:id>", methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.get(id)

    if id == current_user.id:
        return jsonify({"message": "You cannot delete user logged in"})
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {id} has been deleted successful"})
    
    return jsonify({"message": "User not found"}), 404 

if __name__ == '__main__':
    app.run(debug=True)