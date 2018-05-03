const express = require('express')
const httpApp = express()
const httpsApp = express()
const http = require('http')
const https = require('https')
const fs = require('fs')
const helmet = require('helmet')

const ONE_YEAR = 31536000000
const bodyParser = require('body-parser')
const fileUpload = require('express-fileupload')
cost mongoClient = require('mongodb').MongoClient;

httpsApp.use(helmet.hsts({
  maxAge: ONE_YEAR,
  includeSubdomains: true,
  force: true
  }))
  
httpsApp.use(bodyParser.json())
httpsApp.use(fileUpload())

var cipher = ['ECDHE-ECDSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-GCM-SHA384',
'ECDHE-RSA-AES256-CBC-SHA384',
'ECDHE-RSA-AES256-GCM-SHA256',
'ECDHE-ECDSA-AES128-GCM-SHA256',
'ECDHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES128-GCM-SHA256',
'DHE-RSA-AES256-GCM-SHA384',
'!aNULL',
'MD5',
'!DSS'].join(':')

httpApp.get("*", function(req, res, next){
  res.redirect('https://' + req.headers.host + req.url);
})

httpsApp.get('/', function(req, res){
  res.send('You are in the right place.');
})

httpsApp.get('/server', function(req, res){
  mongoClient.connect("mongodb://localhost:27017/server", function(err, client){
    if (!err){
      if (req.headers['appkey'] == 'UnicornEncryption'){
        client.db('files').collection('files').findOne({'public_key': req.query['public_key']}, function(err, result){
          if (err) throw err
          res.send(result)
        });
      } else {
        console.log("WARNING: Invalid application has sent a GET")
        res.send("Invalid Application")
      }
    } else {
      res.send("ERROR: Can not connect to server")
    }
  })
})

httpsApp.post('/server', function(req, res){
  mongoClient.connect("mongodb://localhost:27017/server", function(err, client){
    if (!err){
      if (req.headers['appkey'] == 'UnicornEncryption'){
        var myObj = {'private_key': req.body.private_key, 'public_key': req.body.public_key}
        client.db('files').collection('files').insert(myObj, function(err, result){
          if (err) throw err
        })
        res.send("Insert Complete")
      } else {
        console.log("WARNING: Invalid application has sent a GET")
        res.send("Invalid Application")
      }
    } else {
      res.send("Can not connect to server")
    }
  })
})

var options = {
  key: fs.readFileSync('/etc/letsencrypt/live/unicorntheoriest.me/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/unicorntheoriest.me/fullchain.pem'),
  ciphers: cipher
}

http.createServer(httpApp).listen(8080)
https.createServer(options, httpsApp).listen(23245)
