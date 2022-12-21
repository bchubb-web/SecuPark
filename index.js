//MODULES
const {exec} = require('child_process');
const bodyParser = require('body-parser');
const express = require("express");
const app = express();
const path = require("path");
const sql = require("mysql");

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.use('/public/styles',express.static(__dirname+'/styles'));

//const pug = require('pug');


app.get('/',(req,res) => {
    res.sendFile(path.join(__dirname)+"\\index.html");
});

app.get('/begin', (req,res) => {
    res.sendFile(path.join(__dirname)+"\\begin.html")
});

app.get('/contact', (req,res) => {
    res.sendFile(path.join(__dirname)+"\\contact.html")
});


app.post('/anpr/:locationID', (req,res) => {
    var LID = req.params.locationID;
    var data = req.body;
    var frame = data.b_64;

    console.log("Site:"+LID+" frame:"+frame);

    res.sendStatus(200);
});

console.log("Starting up...");
app.listen(3000,console.log('Server live'));
