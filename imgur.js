const req = require('request');

class imgur {
  constructor(imgur_client_id) {
    this.imgur_client_id = imgur_client_id;
    this.headers = {
      Authorization: `Client-ID ${imgur_client_id}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    };
  }

  /**
   * @name uploadImage
   * @description upload one image and return the link
   * @param {string<binary?base64?>} picture
   */
  uploadImage(picture) {
    return new Promise((resolve, reject) => {
      const form = {
        image: picture
      };
      req.post(
        'https://api.imgur.com/3/image',
        {
          headers: this.headers,
          form: form
        },
        (err, res, body) => {
          if (err) {
            reject(err);
          }
          const parsedBody = JSON.parse(body);
          if (parsedBody.data && parsedBody.data.link) {
            resolve(parsedBody.data.link);
          } else {
            reject(res);
          }
        }
      );
    });
  }

  /**
   * @name uploadImages
   * @description upload one array of images and return their links
   * @param {array<binary?base64?>} pictures
   */
  uploadImages(pictures) {
    return new Promise((resolve, reject) => {
      const uploadPromises = pictures.map((picture) =>
        this.uploadImage(picture)
      );
      Promise.all(uploadPromises)
        .then((result) => resolve(result))
        .catch((err) => reject(err));
    });
  }
}

module.exports = imgur;
