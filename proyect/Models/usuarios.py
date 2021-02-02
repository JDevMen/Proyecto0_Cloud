from app import db, ma, api



class Usuario(db.model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Usuario_Schema(ma.Schema):
    class Meta:
        fields = ['id', 'email', 'password']

