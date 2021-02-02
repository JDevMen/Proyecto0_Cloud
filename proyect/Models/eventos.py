from app import db, ma, api


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

