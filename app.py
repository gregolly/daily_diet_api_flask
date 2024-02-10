from flask import Flask
from database import db
from routes.user_routes import user_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_bp.login'  # Change 'login' to 'user_bp.login'

app.register_blueprint(user_bp, url_prefix='/user')  # This sets a prefix for all routes in user_bp

if __name__ == '__main__':
    app.run(debug=True)