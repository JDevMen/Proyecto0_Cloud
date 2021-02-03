from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.Utils.database import db
from marshmallow_sqlalchemy import ModelSchema

#Recurso para el manejo de los eventos creados por cada usuario.
#Se maneja la autenticación y la autorización para acceder a
#los métodos que modifican la base de datos.

class Evento(db.Model):
    __tablename__ = "Event"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(20))
    lugar = db.Column(db.String(100))
    direccion = db.Column(db.String(150))
    fecha_inicio = db.Column(db.String(50))
    fecha_fin = db.Column(db.String(50))
    virtual = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

#Schema que define el model, la sessión de la base de datos y los campos
class Evento_Schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Evento
        sqla_session = db.session
        fields = ('id', 'nombre', 'categoria', 'lugar', 'direccion', 'fecha_inicio', 'fecha_fin', 'virtual', 'user_id')

#Schema para el manejo de request con respuesta de un solo objeto
event_schema = Evento_Schema()

#Schema para el manejo de request con respuesta de varios objetos (lista).
events_schema = Evento_Schema(many=True)

#Clase del recuso para listar los eventos y crear un evento.
#Se requiere autenticación para acceder y se hace la asociación de user_id
#con respecto a el id obtenido de JWT, es decir, del usuario autenticado.
class RecursoListarEventos(Resource):
    @jwt_required
    def get(self):
        usuario_id = get_jwt_identity()
        eventos = Evento.query.filter_by(user_id=usuario_id)
        return events_schema.dump(eventos)

    @jwt_required
    def post(self):
        usuario_id = get_jwt_identity()
        new_event = Evento(
            nombre=request.json['nombre'],
            categoria=request.json['categoria'],
            lugar=request.json['lugar'],
            direccion=request.json['direccion'],
            fecha_inicio=request.json['fecha_inicio'],
            fecha_fin=request.json['fecha_fin'],
            virtual=request.json['virtual'],
            user_id=usuario_id
        )
        db.session.add(new_event)
        db.session.commit()
        return event_schema.dump(new_event)

#Clase del recurso para los métodos que modifican solo un evento.
#Se requiere de autenticación para acceder. Solo se pueden utilizar los métodos
#en eventos que le pertenezcan al usuario autenticado.
class RecursoUnEvento(Resource):
    @jwt_required
    def get(self, id_evento):
        usuario_id = get_jwt_identity()
        evento = Evento.query.get_or_404(id_evento)
        if str(evento.user_id) == str(usuario_id):
            return event_schema.dump(evento)
        else:
            return 'Forbidden', 403

    @jwt_required
    def put(self, id_evento):
        usuario_id = get_jwt_identity()
        evento = Evento.query.get_or_404(id_evento)
        if str(usuario_id) == str(evento.user_id):
            if 'nombre' in request.json:
                evento.nombre = request.json['nombre']
            if 'categoria' in request.json:
                evento.categoria = request.json['categoria']
            if 'lugar' in request.json:
                evento.lugar = request.json['lugar']
            if 'direccion' in request.json:
                evento.direccion = request.json['direccion']
            if 'fecha_inicio' in request.json:
                evento.fecha_inicio = request.json['fecha_inicio']
            if 'fecha_fin' in request.json:
                evento.fecha_fin = request.json['fecha_inicio']
            if 'virtual' in request.json:
                evento.virtual = request.json['virtual']
            db.session.commit()
            return event_schema.dump(evento)
        else:
            return 'Forbidden', 403

    @jwt_required
    def delete(self, id_evento):
        usuario_id = get_jwt_identity()
        evento = Evento.query.get_or_404(id_evento)
        if str(usuario_id) == str(evento.user_id):
            db.session.delete(evento)
            db.session.commit()
            return '', 204
        else:
            return 'Forbidden', 403
