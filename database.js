const MongoClient = require("mongodb").MongoClient;
const assert = require("assert");

class Database {
  constructor(dbName, url = "mongodb://localhost:27017") {
    // Connection URL
    this.url = url;

    // Database Name
    this.dbName = dbName;
  }

  insertDocument(document, className) {
    return new Promise((resolve, reject) => {
      // Use connect method to connect to the server
      const client = new MongoClient(this.url, { useNewUrlParser: true });
      client.connect(err => {
        assert.equal(null, err);
        const db = client.db(this.dbName);
        const collection = db.collection(className);
        collection.insertOne(document, (err, result) => {
          client.close();
          if (err) {
            reject(err);
          } else {
            if (result.result.n == 1) {
              resolve(result.ops);
            } else {
              reject("Erro ao adicionar");
            }
          }
        });
      });
    });
  }

  findDocuments(className, filter = {}) {
    return new Promise((resolve, reject) => {
      // Use connect method to connect to the server
      const client = new MongoClient(this.url, { useNewUrlParser: true });
      client.connect(err => {
        assert.equal(null, err);
        const db = client.db(this.dbName);
        const collection = db.collection(className);
        Object.keys(filter).forEach(field => {
          // if (typeof filter[field] == typeof []) {
          //   filter[field] = { $in: filter[field] };
          // } else
          if (filter[field] == undefined) {
            delete filter[field];
          }
        });
        collection
          .find(filter)
          .toArray()
          .then(docs => {
            client.close();
            resolve(docs);
          })
          .catch(err => {
            client.close();
            reject(err);
          });
      });
    });
  }

  removeDocument(className, filter) {
    return new Promise((resolve, reject) => {
      // Use connect method to connect to the server
      const client = new MongoClient(this.url, { useNewUrlParser: true });
      client.connect(err => {
        assert.equal(null, err);
        const db = client.db(this.dbName);
        const collection = db.collection(className);
        collection
          .deleteOne(filter)
          .then(result => {
            client.close();
            if (result.result.n == 1) {
              resolve(result.result);
            } else {
              reject("Erro ao deletar");
            }
          })
          .catch(err => {
            client.close();
            reject(err);
          });
      });
    });
  }

  randomDocument(className, amount) {
    return new Promise((resolve, reject) => {
      // Use connect method to connect to the server
      const client = new MongoClient(this.url, { useNewUrlParser: true });
      client.connect(err => {
        assert.equal(null, err);
        const db = client.db(this.dbName);
        const collection = db.collection(className);
        collection
          .aggregate([{ $sample: { size: amount } }])
          .toArray()
          .then(result => resolve(result))
          .catch(err => reject(err));
      });
    });
  }
}

module.exports = Database;
