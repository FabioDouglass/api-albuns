from . import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100),unique=True, nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Integer)
    critica = db.Column(db.Text, nullable=True)
    collectionId = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'artista': self.artista, 'ano': self.ano, 'nota': self.nota, 'critica': self.critica, 'collectionId': self.collectionId}