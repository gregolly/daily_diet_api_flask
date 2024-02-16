from flask import Flask
from database import db
from models.user import User 
from routes.user_routes import user_bp
from routes.meal_routes import meal_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3306/daily_diet_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_bp.login'

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None and user_id.isdigit():
        return User.query.get(int(user_id))
    return None

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(meal_bp, url_prefix='/meal')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database tables
    app.run(debug=True)