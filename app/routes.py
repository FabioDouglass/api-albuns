from flask import Blueprint, request, jsonify
from .models import Album
from . import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime

main = Blueprint('main', __name__)

# Listar todos os álbuns
@main.route('/albuns', methods=['GET'])
def obter_albuns():
    """
    Retorna a lista de álbuns
    ---
    tags:
      - Álbums
    operationId: obter_albuns
    responses:
      200:
        description: Lista de álbuns avaliados
        schema:
          type: array
          items:
            type: object
            properties:
              nome:
                type: string
              artista:
                type: string
              ano:
                type: integer
              nota:
                type: integer
              critica:
                type: string
              collectionId:
                type: string
    """
    albuns = db.session.query(Album.nome, Album.artista, Album.ano, Album.nota, Album.critica, Album.collectionId).all()
    return jsonify([{'nome': nome, 'artista': artista, 'ano': ano, 'nota': nota, 'critica': critica, 'collectionId': collectionId} for nome, artista, ano, nota, critica, collectionId in albuns])

# Registrar um álbum
@main.route('/album', methods=['POST'])
def adicionar_album():
    """
    Adicionar álbum
    ---
    tags:
      - Álbums
    operationId: adicionar_album
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required:
            - nome
            - artista
            - ano
          properties:
            nome:
              type: string
              example: "Abbey Road"
            artista:
              type: string
              example: "The Beatles"
            ano:
              type: integer
              example: 1969
            nota:
              type: integer
              example: 5
            critica:
              type: string
              example: "Otimo disco"
            collectionId:
              type: string
              example: 123456
              
    responses:
      201:
        description: Álbum adicionado com sucesso
      400:
        description: Dados inválidos
      409:
        description: Álbum já cadastrado
    """
    dados = request.get_json()

    # Campos obrigatórios
    campos_obrigatorios = ['nome', 'artista', 'ano', 'collectionId']
    for campo in campos_obrigatorios:
      if campo not in dados or not str(dados[campo]).strip():
        return jsonify({'erro': f'Campo "{campo}" é obrigatório'}), 400

    # Validação do ano
    ano = dados.get('ano')
    if ano is not None:
      if not isinstance(ano, int):
        return jsonify({'erro': 'Campo "ano" deve ser um número inteiro'}), 400
      ano_atual = datetime.now().year
      if ano < 1800 or ano > ano_atual:
        return jsonify({'erro': f'Campo "ano" inválido'}), 400

    # Validação da nota
    nota = dados.get('nota')
    if nota is not None:
      if not isinstance(nota, int):
        return jsonify({'erro': 'Campo "nota" deve ser um número inteiro'}), 400
      if nota < 0 or nota > 5:
        return jsonify({'erro': 'Campo "nota" deve estar entre 0 e 5'}), 400

    # Criar o álbum
    novo_album = Album(
    nome=dados['nome'],
    artista=dados['artista'],
    ano=dados['ano'],
    nota=nota,
    critica=dados.get('critica', None),
    collectionId=dados['collectionId'] 
)

    try:
      db.session.add(novo_album)
      db.session.commit()
      return jsonify({'mensagem': 'Álbum adicionado com sucesso!'}), 201

    except IntegrityError:
      db.session.rollback()
      return jsonify({'mensagem': 'Álbum já cadastrado!'}), 409
# Deletar um álbum
@main.route('/album/<string:collectionId>', methods=['DELETE'])
def deletar_album(collectionId):
    """
    Deletar álbum pelo collectionId
    ---
    tags:
      - Álbums
    operationId: deletar_album
    parameters:
      - name: collectionId
        in: path
        type: string
        required: true
    responses:
      200:
        description: Álbum deletado com sucesso
      404:
        description: Álbum não encontrado
    """
    album = db.session.query(Album).filter(Album.collectionId == collectionId).first()

    if not album:
        return jsonify({'erro': 'Álbum não encontrado'}), 404

    db.session.delete(album)
    db.session.commit()
    return jsonify({'mensagem': f'{album.nome} foi removido com sucesso.'})

#Buscar Album
@main.route('/album', methods=['GET'])
def obter_album():
    """
    Retorna álbum pelo collectionId
    ---
    tags:
      - Álbums
    operationId: obter_album
    parameters:
      - name: collectionId
        in: query
        type: string
        required: true
    responses:
      200:
        description: Álbum encontrado
        schema:
          type: array
          items:
            type: object
            properties:
              nome:
                type: string
              artista:
                type: string
              ano:
                type: integer
              nota:
                type: integer
               critica:
                type: string
              collectionId:
                type: string
    """
    collectionId = request.args.get("collectionId")

    if not collectionId:
        return jsonify({"erro": "Informe ao menos um parâmetro: collectionId."}), 400

    albuns = db.session.query(Album).filter(Album.collectionId == collectionId).all()

    resultado = [
        {
            "nome": album.nome,
            "artista": album.artista,
            "ano": album.ano,
            "nota": album.nota,
            "critica": album.critica,
            "collectionId": album.collectionId
        } for album in albuns
    ]

    return jsonify(resultado), 200


# Atualizar um álbum
@main.route('/album/<string:collectionId>', methods=['PUT'])
def atualizar_album(collectionId):
    """
    Atualizar álbum pelo collectionId 
    ---
    tags:
      - Álbums
    operationId: atualizar_album
    parameters:
      - name: collectionId
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nota:
              type: integer
            critica:
              type: string
    responses:
      200:
        description: Álbum atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Álbum não encontrado
    """
    album = db.session.query(Album).filter(Album.collectionId == collectionId).first()

    if not album:
        return jsonify({'erro': 'Álbum não encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Corpo da requisição obrigatório'}), 400

    if 'nota' in data:
        try:
            nota = int(data['nota'])
            if nota < 0 or nota > 5:
                return jsonify({'erro': 'Campo "nota" deve estar entre 0 e 5'}), 400
            album.nota = nota
        except ValueError:
            return jsonify({'erro': 'Campo "nota" deve ser um número inteiro'}), 400

    if 'critica' in data and data['critica'] is not None:
        critica = data['critica']
        if not isinstance(critica, str):
            return jsonify({'erro': 'Campo "critica" deve ser uma string'}), 400
        album.critica = critica

    db.session.commit()

    return jsonify({'mensagem': f'Álbum {album.nome} atualizado com sucesso.'})
