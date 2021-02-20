from variance import db

# Association table. Associates MuscleGroups with their Muscles and vice-versa
class MuscleGroupAssociationTable(db.Model):
    __tablename__ = "MuscleGroupAssociation"
    group_id = db.Column(db.Integer, db.ForeignKey("MuscleGroupIndex.id"), primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey("MuscleIndex.id"), primary_key=True)

# Association table. Associates exercises with the PRIMARY muscles they work
class PrimaryExerciseMuscleAssociationTable(db.Model):
    __tablename__ = "PrimaryExerciseMuscleAssociation"

    exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey("MuscleIndex.id"), primary_key=True)

# Association table. Associates exercises with the SECONDARY muscles they work
class SecondaryExerciseMuscleAssociationTable(db.Model):
    __tablename__ = "SecondaryExerciseMuscleAssociation"

    exercise_id = db.Column(db.Integer, db.ForeignKey("ExerciseIndex.id"), primary_key=True)
    muscle_id = db.Column(db.Integer, db.ForeignKey("MuscleIndex.id"), primary_key=True)   

class MuscleGroupModel(db.Model):
    __tablename__ = "MuscleGroupIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Name of this muscle group
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # List of muscles in this muscle group
    muscles = db.relationship("MuscleModel", secondary="MuscleGroupAssociation", back_populates="groups")

    @staticmethod
    def has_owner():
        return False

class MuscleModel(db.Model):
    __tablename__ = "MuscleIndex"

    id = db.Column(db.Integer, primary_key=True)

    # Optional: ID of this muscle used to locate on the anatomy chart
    diagram_id = db.Column(db.Integer, nullable=True)

    # Long, anatomical name for this muscle
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Shortened name for this muscle. Used for display.
    short_name = db.Column(db.String(50), nullable=True)

    # List of groups this muscle belongs to
    groups = db.relationship("MuscleGroupModel", secondary="MuscleGroupAssociation", back_populates="muscles")

    # List of exercises that this muscle is used in as a primary muscle
    primary_exercises = db.relationship("ExerciseModel", secondary="PrimaryExerciseMuscleAssociation", back_populates="primary_muscles")

    # List of exercises that this muscle is used in as a secondary muscle
    secondary_exercises = db.relationship("ExerciseModel", secondary="SecondaryExerciseMuscleAssociation", back_populates="secondary_muscles")
    
    @staticmethod
    def has_owner():
        return False