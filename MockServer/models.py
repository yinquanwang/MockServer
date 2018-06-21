from MockServer import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    api = db.relationship('Api', backref='project')


class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False, unique=True)
    body = db.Column(db.TEXT, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
