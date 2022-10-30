from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_image_alchemy.storages import FileStorage
from flask_migrate import Migrate
from flask import render_template
from flask_login import LoginManager


db = SQLAlchemy()
fs_storage = FileStorage()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db)
    fs_storage.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def home():
        return render_template('index.html', title='Главная страница')

    from .views import auth
    app.register_blueprint(auth)

    return app