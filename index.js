//MODULES
const {exec} = require('child_process');
//const bodyParser = require('body-parser');
const express = require("express");
const app = express();
const path = require("path");
const sql = require("mysql");


app.use('/public/styles',express.static(__dirname+'/styles'));

//const pug = require('pug');


app.get('/',(req,res) => {
    res.sendFile(path.join(__dirname)+"\\index.html");
});

app.get('/begin', (req,res) => {
    res.sendFile(path.join(__dirname)+"\\begin.html")
});



app.post('/check/:locationID', (req,res) => {
    var LID = req.params.locationID;
    var frame = req.body.frame;
    console.log(LID);
    console.log(frame);
    

    res.send(200);
});

app.listen(3000,console.log('site live'));
