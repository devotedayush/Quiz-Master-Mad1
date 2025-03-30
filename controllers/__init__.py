from controllers.auth import auth
from controllers.admin import admin
from controllers.user import user


def register_blueprints(app):
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/user')