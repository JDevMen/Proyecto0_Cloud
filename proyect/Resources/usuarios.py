from Utils.database import db
from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .evento import Evento_Schema
from flask_jwt_extended import jwt_required, get_jwt_identity


class Usuario(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    events = db.relationship("Evento", backref="Usuario", cascade="all,delete-orphan")

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Usuario_Schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Usuario
        sqla_session = db.session
        id = fields.Integer(dump_only=True)
        email = fields.String(required=True)
        password = fields.String(required=True)
        events = fields.Nested(Evento_Schema, many=True)


user_schema = Usuario_Schema()

users_schema = Usuario_Schema(many=True)


class RecursoListarUsuarios(Resource):
    def get(self):
        users = Usuario.query.all()
        return users_schema.dump(users)

    def post(self):
        new_user = Usuario(
            email=request.json['email'],
            password=request.json['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class RecursoUnUsuario(Resource):
    @jwt_required
    def get(self):
        id_usuario = get_jwt_identity()
        user = Usuario.query.get_or_404(id_usuario)
        return user_schema.dump(user)
    @jwt_required
    def put(self):
        id_usuario = get_jwt_identity()
        user = Usuario.query.get_or_404(id_usuario)
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.password = request.json['password']
        db.session.commit()
        return user_schema.dump(user)

    @jwt_required
    def delete(self):
        id_usuario = get_jwt_identity()
        user = Usuario.query.get_or_404(id_usuario)
        db.session.delete(user)
        db.session.commit()
        return '', 204
