from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abc.db'

db = SQLAlchemy(app)

ma = Marshmallow(app)

api = Api(app)


class Evento(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(20))
    lugar = db.Column(db.String(100))
    direccion = db.Column(db.String(150))
    fecha_inicio = db.Column(db.String(50))
    fecha_fin = db.Column(db.String(50))
    virtual = db.Column(db.Boolean(), default=True)


class Evento_Schema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'categoria', 'lugar', 'direccion', 'fecha_inicio', 'fecha_fin', 'virtual')


event_schema = Evento_Schema()

events_schema = Evento_Schema(many=True)


class RecursoListarEventos(Resource):
    def get(self):
        eventos = Evento.query.all()
        return events_schema.dump(eventos)

    def post(self):
        new_event = Evento(
            nombre=request.json['nombre'],
            categoria=request.json['categoria'],
            lugar=request.json['lugar'],
            direccion=request.json['direccion'],
            fecha_inicio=request.json['fecha_inicio'],
            fecha_fin=request.json['fecha_fin'],
            virtual=request.json['virtual']
        )
        db.session.add(new_event)
        db.session.commit()
        return event_schema.dump(new_event)


class RecursoUnEvento(Resource):
    def get(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        return event_schema.dump(evento)

    def put(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
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

    def delete(self, id_evento):
        evento = Evento.query.get_or_404(id_evento)
        db.session.delete(evento)
        db.session.commit()
        return '', 204


api.add_resource(RecursoListarEventos, '/eventos')
api.add_resource(RecursoUnEvento, '/eventos/<int:id_evento>')
if __name__ == '__main__':
    app.run(debug=True)
