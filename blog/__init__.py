from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_image_alchemy.storages import FileStorage
from flask_migrate import Migrate
from flask import render_template


db = SQLAlchemy()
fs_storage = FileStorage()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db)
    fs_storage.init_app(app)

    @app.route("/")
    def home():
        return render_template('index.html', title='Главная страница')

    return app