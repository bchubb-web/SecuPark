const bodyParser = require('body-parser');
const express = require("express");
const app = express();
const { MongoClient, ServerApiVersion } = require('mongodb');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

//currently working on 
app.get('/detect/:b64image', (req, res) => {
    const encoded = req.params.b64image;
    var decoded = new Image();
    decoded.src = `data:image/png;base64,${encoded}`;
    res.send(decoded);
});







app.post('/anpr/:locationID', (req,res) => {
    var LID = req.params.locationID;
    var data = req.body;
    var frame = data.b_64;

    console.log("Site:"+LID+" frame:"+frame);

    res.sendStatus(200);
});



app.post('/plate/:plate', (req, res) => {
    console.log(req.params.plate);
    res.sendStatus(200)
});

console.log("Starting up...");
app.listen(3000,console.log('Server live'));
