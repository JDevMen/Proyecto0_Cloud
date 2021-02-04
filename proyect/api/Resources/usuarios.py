from api.Utils.database import db
from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .evento import Evento_Schema
from flask_jwt_extended import jwt_required, get_jwt_identity

#Recurso para el manejo de usuarios. Se maneja la autenticación y la autorización para acceder a
#los métodos que modifican la base de datos.

#Definición de Usuario, incluyendo sus atributos
class Usuario(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    events = db.relationship("Evento", backref="Usuario", cascade="all,delete-orphan")

    #Método para encriptar la clave del usuario
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    #Método para revisar que una clave dada corresponda a la clave guardada en la base de datos
    def check_password(self, password):
        return check_password_hash(self.password, password)


#Schema de usuario, define el modelo, la base de datos a utilizar y características de los atributos en la base de datos.
class Usuario_Schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Usuario
        sqla_session = db.session
        id = fields.Integer(dump_only=True)
        email = fields.String(required=True)
        password = fields.String(required=True)
        events = fields.Nested(Evento_Schema, many=True)

#Schema para el manejo de peticiones con respuesta de un objeto.
user_schema = Usuario_Schema()

#Schema para el manejo de peticiones con respuesta de varios objetos.
#varios de los métodos se usan para la verificación de los servicios a través de postman
#y no deben ser llamadados desde el front end
users_schema = Usuario_Schema(many=True)

#Schema para listar los usuarios y crear un usuario sin recurrir a la autenticación.
#Solo se utiliza para hacer revisiones desde POSTman
class RecursoListarUsuarios(Resource):
    def get(self):
        users = Usuario.query.all()
        return users_schema.dump(users)

    def post(self):
        new_user = Usuario(
            email=request.json['email'],
            password=request.json['password']
        )
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

#Recurso para requests sobre un solo usuario
#Todos los métodos requieren de autenticación.
#La forma de acceder a los distintos métodos es por medio del token JWT
#esto garantiza que un usuario solo puede acceder, modificar y eliminar su propio usuario
#después de haber hecho login.
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
        user.hash_password()
        db.session.commit()
        return user_schema.dump(user)

    @jwt_required
    def delete(self):
        id_usuario = get_jwt_identity()

        user = Usuario.query.get_or_404(id_usuario)
        db.session.delete(user)
        db.session.commit()
        return '', 204
