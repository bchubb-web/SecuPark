import bodyParser from 'body-parser';
import express from 'express';
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
//currently working on 
app.get('/detect/:b64image', (req, res) => {
    //var decoded = new Image();
    //decoded.src = `data:image/png;base64,${decodeURIComponent(req.params.b64image)}`;
    Buffer.from(req.params.b64image, "base64");
    res.sendStatus(200);
});
app.post('/anpr/:locationID', (req, res) => {
    var LID = req.params.locationID;
    var data = req.body;
    var frame = data.b_64;
    console.log("Site:" + LID + " frame:" + frame);
    res.sendStatus(200);
});
app.post('/plate/:plate', (req, res) => {
    console.log(req.params.plate);
    res.sendStatus(200);
});
app.listen(3000, () => console.log('Server live'));
//# sourceMappingURL=index.js.map