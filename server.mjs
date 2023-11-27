// This is a framework to handle server-side content

// You have to do an 'npm install express' to get the package
// Documentation in: https://expressjs.com/en/starter/hello-world.html
import express from 'express';

import * as db from "./db_mysql.mjs";

var app = express();
let port = 3001

db.connect();

// Serve static HTML files in the current directory (called '.')
app.use(express.static('.'))

// For GET requests to "/student?field1=value1&field2=value2"
// providing a function that takes the request of the user,
// goes into the database module (db.qC) & executes a call that will query the db
app.get('/player', function(request, response){
    // If we have fields available
    // console.log(request.query["field1"])

    //let playerId = request.query["name"]
    let name = request.query["name"]

    db.queryPlayerByNameCallback(name, (results) => {
        // also, provide a fn to query callback - whenever you perform query,
        // pass a desscription of what we need to do with these results
        // anonymous fn that takes them & sends them back to the user in json format
        response.json(results);
        // console.log(playerName)
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