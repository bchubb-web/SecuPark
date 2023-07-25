import bodyParser from 'body-parser';
import express from 'express';
const app = express();

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

// currently working on 
// posts base64 image to google cloud api,
//
// returns decoded plate
app.get('/detect/:b64image', async (req, res) => {
    const decoded = await fetch("https://vision.googleapis.com/v1/images:annotate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "Bearer ",
            "x-goog-user-project": "secupark-393921"
        },
        body: JSON.stringify({
            "requests": [{
                "image": { "content": req.params.b64image },
                "features": [
                    { "type": "TEXT_DETECTION" }
                ]
            }]
        })
    });
    const ocrText = await decoded.json();
    //Buffer.from(req.params.b64image, "base64");
    res.send(JSON.stringify(ocrText));
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

app.listen(3000, ()=>console.log('Server live'));
