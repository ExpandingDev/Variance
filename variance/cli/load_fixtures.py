from datetime import datetime
import click
from flask.cli import AppGroup
from variance import db

lf_cli = AppGroup("load-fixture")

@lf_cli.command("units")
def cli_fixture_load_units():
    click.echo("Adding default units...")
    from variance.fixtures.units import DEFAULT_UNITS
    from variance.models.unit import UnitModel

    # By default all fixture units are not removable. Aka they are not created by a user
    for u in DEFAULT_UNITS:
        m = UnitModel(multiplier=u[0], name=u[1][-1], dimension=u[2], abbreviation=u[1][0], removable=False)
        db.session.add(m)
        db.session.commit()
    click.echo("Default units added.")

@lf_cli.command("equipment")
def cli_fixture_load_equipment():
    click.echo("Adding default equipment...")
    from variance.fixtures.equipment import DEFAULT_EQUIPMENT
    from variance.models.equipment import EquipmentModel

    for e in DEFAULT_EQUIPMENT:
        m = EquipmentModel(name=e[0], description=e[1])
        db.session.add(m)
        db.session.commit()
    click.echo("Default equipment added.")
    
@lf_cli.command("nutrients")
def cli_fixture_load_nutrients():
    click.echo("Adding default nutrients...")
    from variance.fixtures.nutrients import DEFAULT_NUTRIENTS
    from variance.models.nutrition import NutrientInfoModel

    count = 0
    for e in DEFAULT_NUTRIENTS:
        n = NutrientInfoModel(name=e[0],scientific_name=e[1],abbreviation=e[2],description=e[3],is_element=e[4],is_amino_acid=e[5],is_vitamin=e[6],vitamin_family=e[7],vitamin_number=e[8],wikipedia_link=e[9],fdc_nid=e[10],fndds=e[11])
        db.session.add(n)
        db.session.commit()
        count += 1
    click.echo("Default " + str(count) + " nutrient info added.")
    
@lf_cli.command("test_users")
def cli_fixture_load_test_users():
    click.echo("Adding users for testing...")
    from variance.fixtures.users import TESTING_USERS
    from variance.models.user import UserModel

    count = 0
    for i in TESTING_USERS:
        u = UserModel(username=i[0],email=i[1],birthdate=datetime.fromisoformat(i[3]),role=i[4])
        u.set_password(i[2])
        if i[5]:
            if "nopeanuts" in i[5]:
                u.no_peanuts = True
            if "notreenuts" in i[5]:
                u.no_treenuts = True
            if "nodairy" in i[5]:
                u.no_dairy = True
            if "noeggs" in i[5]:
                u.no_eggs = True
            if "nopork" in i[5]:
                u.no_pork = True
            if "nobeef" in i[5]:
                u.no_beef = True
            if "nomeat" in i[5]:
                u.no_meat = True
            if "nofish" in i[5]:
                u.no_fish = True
            if "noshellfish" in i[5]:
                u.no_shellfish = True
            if "nogluten" in i[5]:
                u.no_gluten = True
            if "vegetarian" in i[5]:
                u.is_vegetarian = True
            if "vegan" in i[5]:
                u.is_vegan = True
            if "kosher" in i[5]:
                u.is_kosher = True
        db.session.add(u)
        db.session.commit()
        count += 1
    click.echo("Added " + str(count) + " users for testing.")

@lf_cli.command("default_admin")
def cli_fixture_load_default_admin():
    click.echo("Adding default admin user...")
    from variance.fixtures.users import DEFAULT_USERS
    from variance.models.user import UserModel

    count = 0
    for i in DEFAULT_USERS:
        u = UserModel(username=i[0],email=i[1],birthdate=datetime.fromisoformat(i[3]),role=i[4])
        u.set_password(i[2])
        if i[5]:
            if "nopeanuts" in i[5]:
                u.no_peanuts = True
            if "notreenuts" in i[5]:
                u.no_treenuts = True
            if "nodairy" in i[5]:
                u.no_dairy = True
            if "noeggs" in i[5]:
                u.no_eggs = True
            if "nopork" in i[5]:
                u.no_pork = True
            if "nobeef" in i[5]:
                u.no_beef = True
            if "nomeat" in i[5]:
                u.no_meat = True
            if "nofish" in i[5]:
                u.no_fish = True
            if "noshellfish" in i[5]:
                u.no_shellfish = True
            if "nogluten" in i[5]:
                u.no_gluten = True
            if "vegetarian" in i[5]:
                u.is_vegetarian = True
            if "vegan" in i[5]:
                u.is_vegan = True
            if "kosher" in i[5]:
                u.is_kosher = True
        db.session.add(u)
        db.session.commit()
        count += 1
    click.echo("Added " + str(count) + " users.")

@lf_cli.command("muscles")
def cli_fixture_load_muscles():
    click.echo("Adding default muscles...")
    from variance.fixtures.muscles import DEFAULT_MUSCLES, DEFAULT_MUSCLE_GROUPS
    from variance.models.muscle import MuscleModel, MuscleGroupModel

    for e in DEFAULT_MUSCLE_GROUPS:
        m = MuscleGroupModel(name=e[0], description=e[1])
        db.session.add(m)
        db.session.commit()

    for e in DEFAULT_MUSCLES:
        short_name = e[1]
        if len(short_name) == 0:
            short_name = e[0]
        m = MuscleModel(name=e[0], short_name=short_name, diagram_id=e[3])
        db.session.add(m)
        for g in e[2]:
            m.groups.append(MuscleGroupModel.query.get(g))
        db.session.commit()
    click.echo("Default muscles and muscle groups added.")