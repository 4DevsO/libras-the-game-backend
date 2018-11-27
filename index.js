const Database = require("./database");
const mlab_url = require("./config/keys").mlab_url;
const mongoDB = new Database("libras_o_jogo");
const express = require("express");
const bodyParser = require("body-parser");
const Utils = require("./utils");

const app = express();

app.use(bodyParser.json());

const port = process.env.PORT || 5000;
const server = app.listen(port, server => {
  console.log(`listening on ${port}`);
});

app.post("/configuracoes/add", (req, res) => {
  if (req.body && req.body.configuracao) {
    const configuracao = req.body.configuracao;
    if (configuracao.nome && configuracao.imagem) {
      mongoDB
        .insertDocument(configuracao, "configuracoes")
        .then(result => res.send(result))
        .catch(err => res.status(500).send(err));
    } else {
      res.sendStatus(400);
    }
  } else {
    res.sendStatus(400);
  }
});

app.post("/configuracoes/delete", (req, res) => {
  if (req.body && req.body.nome) {
    mongoDB
      .removeDocument("configuracoes", { nome: req.body.nome })
      .then(result => res.send(result))
      .catch(err => res.status(500).send(err));
  } else {
    res.sendStatus(400);
  }
});

app.get("/configuracoes/", (req, res) => {
  if (req.query) {
    const filter =
      req.query.nome == undefined && req.query.id == undefined
        ? {}
        : {
            nome: req.query.nome,
            id: req.query.id
          };
    mongoDB
      .findDocuments("configuracoes", filter)
      .then(result => res.send(result))
      .catch(err => res.status(500).send(err));
  } else {
    res.sendStatus(400);
  }
});

app.post("/palavras/add", async (req, res) => {
  if (req.body && req.body.palavra) {
    const palavra = req.body.palavra;
    if (palavra.nome && palavra.configuracoes) {
      const configuracoes_objs = [];
      Promise.all(
        palavra.configuracoes.map(configuracao => {
          return new Promise((resolve, reject) => {
            mongoDB
              .findDocuments("configuracoes", {
                nome: configuracao
              })
              .then(configuracao_obj => {
                if (configuracao_obj[0]) {
                  configuracoes_objs.push(configuracao_obj[0]);
                  resolve();
                } else {
                  reject();
                }
              })
              .catch(err => reject(err));
          });
        })
      )
        .then(result => {
          palavra.configuracoes = configuracoes_objs;
          if (palavra.configuracoes.length > 0) {
            mongoDB
              .insertDocument(palavra, "palavras")
              .then(result => res.send(result))
              .catch(err => res.status(500).send(err));
          } else {
            res
              .status(400)
              .send("Erro ao adicionar palavra, configuracao não existe");
          }
        })
        .catch(err =>
          res
            .status(400)
            .send("Erro ao adicionar palavra, configuracao não existe")
        );
    } else {
      res.sendStatus(400);
    }
  } else {
    res.sendStatus(400);
  }
});

app.post("/palavras/delete", (req, res) => {
  if (req.body && req.body.nome) {
    mongoDB
      .removeDocument("palavras", { nome: req.body.nome })
      .then(result => res.send(result))
      .catch(err => res.status(500).send(err));
  } else {
    res.sendStatus(400);
  }
});

app.get("/palavras/", (req, res) => {
  if (req.query) {
    const filter =
      req.query.nome == undefined && req.query.id == undefined
        ? {}
        : {
            nome: req.query.nome,
            id: req.query.id
          };
    mongoDB
      .findDocuments("palavras", filter)
      .then(result => res.send(result))
      .catch(err => res.status(500).send(err));
  } else {
    res.sendStatus(400);
  }
});

app.get("/game", async (req, res) => {
  let palavras_nin = [];
  let resposta = {};
  let configuracao = {};
  do {
    resposta = (await mongoDB.randomDocument("palavras", 1))[0];
    configuracao =
      resposta.configuracoes[
        Math.floor(Math.random() * resposta.configuracoes.length)
      ];
    palavras_nin = await mongoDB.findDocuments("palavras", {
      "configuracoes.nome": { $nin: [configuracao.nome] }
    });
  } while (palavras_nin.length < 4);

  const alternativas = Utils.getRandom(palavras_nin, 3);
  const palavras = Utils.shuffle([...alternativas, resposta]);
  const ojogo = {
    palavras: palavras,
    configuracao: configuracao,
    resposta: resposta
  };
  res.send(ojogo);
});
