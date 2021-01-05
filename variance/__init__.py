import pathlib
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object("variance.config.DevConfig")
    else:
        app.config.from_object(test_config)

    # Setup the instance directory structure
    pathlib.Path(app.instance_path).mkdir(exist_ok=True)
    if not pathlib.Path(app.instance_path).is_dir():
        print("Instance directory could not be created! Exiting.")
        exit()

    rest_api = Api(app)

    from variance.models import user

    from variance import cli
    app.cli.add_command(cli.db.db_cli)
    app.cli.add_command(cli.user.user_cli)
    """
    app.cli.add_command(cli.fixtures.fixtures_cli)
    app.cli.add_command(cli.units.units_cli)
    
    app.cli.add_command(cli.equipment.equipment_cli)
    app.cli.add_command(cli.muscles.muscles_cli)
    """
    
    db.init_app(app)
    @app.route("/api/apiversion")
    def api_verison():
        return { "apiversion": "0.1" }

    @app.route("/api/version")
    def version():
        return { "version":"0.0.1 alpha" }

    return app


