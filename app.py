from flask import Flask
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///root:admin123@127.0.0.1:3306/new_flask_crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)