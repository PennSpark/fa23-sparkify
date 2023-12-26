// server.js
const express = require('express');
const AWS = require('aws-sdk');
const cors = require('cors');



const app = express();
app.use(cors());
app.use(express.json());


//objKey = "https://fa23-sparkify-bucket.s3.us-east-1.amazonaws.com/homeress.png"

AWS.config.update({
  accessKeyId: 'AKIA4FGSHVMSEXPOF6VA',
  secretAccessKey: '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',
  region: 'us-east-1',
});

const bucketName = 'fa23-sparkify-bucket';



app.post('/getS3Image', (req, res) => {
  const s3 = new AWS.S3();
  //console.log(req.body);
  const params = {
    Bucket: bucketName,
    Key: req.body.imgPath,
    Expires: 3600 
  };

  s3.getSignedUrl('getObject', params, (err, url) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else {
      const sendObj = {
        imgUrl: url
      }
      res.send(sendObj);
    }
  });
});

app.listen(3001, () => {
  console.log('Server is running on port 3001');

  /* const s3 = new AWS.S3();
  const params = {
    Bucket: 'fa23-sparkify-bucket',
    Key: objKey,
  };

  s3.getObject(params, (err, data) => {
    if (err) {
      console.error(err);
      //res.status(500).send('Internal Server Error');
    } else {
        console.log(data);
      //res.send(data.Body);
    }
  }); */
});
