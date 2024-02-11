from flask import Flask
from database import db
from models.user import User 
from routes.user_routes import user_bp
from routes.meal_routes import meal_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/new_flask_crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(meal_bp, url_prefix='/meal')

if __name__ == '__main__':
    app.run(debug=True)