import pathlib
from flask import Flask
from flask_restful import Api, Resource

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object("config.DevConfig")
    else:
        app.config.from_object(test_config)

    # Setup the instance directory structure
    pathlib.Path(app.instance_path).mkdir(exist_ok=True)
    if not pathlib.Path(app.instance_path).is_dir():
        print("Instance directory could not be created! Exiting.")
        exit()

    (pathlib.Path(app.instance_path) / pathlib.Path("fixtures/generated/scripts/")).mkdir(exist_ok=True, parents=True)
    if not (pathlib.Path(app.instance_path) / pathlib.Path("fixtures/generated/scripts/")).is_dir():
        print("Instance fixtures directory could not be created! Exiting.")
        exit()

    from . import db
    db.init_app(app)

    rest_api = Api(app)

    from . import api
    app.register_blueprint(api.auth.bp)
    rest_api.add_resource(api.units.UnitList,               "/api/units/")
    rest_api.add_resource(api.units.Unit,                   "/api/units/<int:unit_id>")
    rest_api.add_resource(api.equipment.EquipmentList,      "/api/equipment/")
    rest_api.add_resource(api.equipment.Equipment,          "/api/equipment/<int:equipment_id>")
    rest_api.add_resource(api.muscles.MuscleList,           "/api/muscles/")
    rest_api.add_resource(api.muscles.Muscle,               "/api/muscles/<int:equipment_id>")

    from . import cli
    app.cli.add_command(cli.db.db_cli)
    app.cli.add_command(cli.fixtures.fixtures_cli)
    app.cli.add_command(cli.units.units_cli)
    app.cli.add_command(cli.auth.auth_cli)
    app.cli.add_command(cli.equipment.equipment_cli)
    app.cli.add_command(cli.muscles.muscles_cli)

    @app.route("/api/apiversion")
    def api_verison():
        return { "apiversion": "0.1" }

    @app.route("/api/version")
    def version():
        return { "version":"0.0.1 alpha" }

    return app
