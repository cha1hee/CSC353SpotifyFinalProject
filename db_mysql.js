// Documentation in: https://expressjs.com/en/starter/hello-world.html
import express from 'express';

import * as db from "./db_mysql.mjs";

var app = express();
let port = 3000

db.connect();

app.use(express.static('.'))

app.get('/player', function(request, response){
    let name = request.query["name"]

    db.queryPlayerByNameCallback(name, (results) => {
        response.json(results);
    })
});

app.get('/tournament', function(request, response){
    let tournYear = request.query["tourn_date"];
    db.queryTournamentByYearCallback(tournYear, (results) => {
        response.json(results);
    })
});

app.get('/statistics', function(request, response){
    let name = request.query["player_name"];
    let start = request.query["start_date"];
    let end = request.query["end_date"];
    db.queryShowAggregateStatisticsCallback(name, start, end, (results) => {
        response.json(results);
    })
})

app.listen(port, () => console.log('Server is starting on PORT,', port))

process.on('exit', () => {
    db.disconnect()
})