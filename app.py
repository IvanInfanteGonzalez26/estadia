from flask import Flask
from config import Config
from models.db_config import db
from models.user_model import User
from models.post_model import Post
from controllers.auth_controller import auth
from controllers.blog_controller import blog

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(blog)
    app.add_url_rule('/', endpoint='index')
    
    with app.app_context():
        db.create_all() 

    return app
