# import Flask
from flask import Flask, render_template
# setup config, to get config object
from config import Config
# setup database object, without inheriting flask app instance
from models import db, create_admin_if_not_exists
# register blue print
from controllers import register_blueprints

from flask import Flask
def create_app():
    # create Flask app
    app= Flask(__name__)
    # apply config to setup database uri
    app.config.from_object(Config)
    # intialise the database on the on flask app
    db.init_app(app)
    # register blueprint
    register_blueprints(app)
    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()
    # define the base route.
    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")
    # return full fledged app. 
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

