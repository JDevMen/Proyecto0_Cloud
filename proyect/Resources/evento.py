from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Utils.database import db
from marshmallow_sqlalchemy import ModelSchema


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


class Evento_Schema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Evento
        sqla_session = db.session
        fields = ('id', 'nombre', 'categoria', 'lugar', 'direccion', 'fecha_inicio', 'fecha_fin', 'virtual', 'user_id')


event_schema = Evento_Schema()

events_schema = Evento_Schema(many=True)


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
