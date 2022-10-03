//MODULES
const {exec} = require('child_process');
//const bodyParser = require('body-parser');
const express = require("express");
const app = express();
const path = require("path");


app.use('/public/styles',express.static(__dirname+'/styles'));

//const pug = require('pug');


app.get('/',(req,res) => {
    res.sendFile(path.join(__dirname)+"\\index.html");
});

app.listen(3000,console.log('site live'));
