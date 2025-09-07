# Backend Acervo Musical

Projeto de MVP da sprint de Desenvolvimento Backend Avançado.
Baseado no meu projeto de Fullstack básico, este projeto consiste em uma estrutura de acervo de músicas, onde é possível registrar, listar, apagar e editar críticas de álbuns, os quais as informações são consultadas em uma api externa do itunes.

# Funcionalidades

Buscar álbuns musicais por título ou cantor;
Registrar uma crítica para um álbum;
Listar álbuns criticados;
Editar uma crítica;
Excluir uma crítica;

## Baixar o projeto

```bash
git clone https://github.com/FabioDouglass/api-albuns
cd api-albuns
```

## Rodar o Projeto

**1 - Construir a imagem Docker do projeto**

```
docker build -t flask-app .

```

**2 - Iniciar o projeto**

```
docker run -p 5001:5001 -v $(pwd)/db:/app/db flask-app

```

## Acessar Documentação

Acesse [http://127.0.0.1:5001/docs](http://127.0.0.1:5001/docs) no navegador

API Externa: [https://performance-partners.apple.com/search-api](https://performance-partners.apple.com/search-api)  
Para o requisito consumo de api externa, foi utilizada a API gratuita do iTunes. Conforme demonstrado na documentação do link acima, o acesso é realizado apenas através da montagem da URL indicada, sem a necessidade de tokens de autenticação.
Para este projeto, foi utilizado o term={titulo_ou_cantor}&entity=album para a consulta dos álbuns.
E também a lookup?id={collectionId}&entity=song para buscar as especificações de um determinado álbum, como a lista de músicas.

## URl para requisições

http://127.0.0.1:5001/album  
http://127.0.0.1:5001/albuns

- **Listar todos os ábluns avaliados:**

  ```http
  GET /albuns
  ```

- **Buscar um álbum por ID**

  ```http
  GET /album?collectionId={collectionId}

  ```

- **Editar a crítica de um álbum:**

  ```http
  PUT /album/{collectionId}
  Body:
  {
    "nota": int,
    "critica": str
  }
  ```

  - **Deletar um álbum:**

  ```http
  DELETE /album/{collectionId}
  ```

- **Cadastrar um album:**

  ```http
  POST /api/album
  Body:
  {
  "nome": str,
  "artista": str,
  "ano": int,
  "collectionId": str
  "nota": int,
  "critica": str
  }
  ```

## Apis Externas

- **Buscar álbuns por título ou cantor**

  ```http
  GET https://itunes.apple.com/search?term={titulo_ou_cantor}&entity=album

  ```

- **Buscar detalhes de um álbum pelo id retornado na api anterior**

  ```http
  GET https://itunes.apple.com/lookup?id={collectionId}&entity=song

  ```

## Fluxograma da Arquitetura da serviço

---

![alt text](Fluxograma.png)
