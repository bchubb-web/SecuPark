"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var body_parser_1 = require("body-parser");
var express_1 = require("express");
var app = (0, express_1.default)();
app.use(body_parser_1.default.urlencoded({ extended: true }));
app.use(body_parser_1.default.json());
//currently working on 
app.get('/detect/:b64image', function (req, res) {
    var decoded = new Image();
    decoded.src = "data:image/png;base64,".concat(req.params.b64image);
    res.send(decoded);
});
app.post('/anpr/:locationID', function (req, res) {
    var LID = req.params.locationID;
    var data = req.body;
    var frame = data.b_64;
    console.log("Site:" + LID + " frame:" + frame);
    res.sendStatus(200);
});
app.post('/plate/:plate', function (req, res) {
    console.log(req.params.plate);
    res.sendStatus(200);
});
app.listen(3000, function () { return console.log('Server live'); });
