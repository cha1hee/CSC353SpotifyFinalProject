// You have to do an 'npm install mysql2' to get the package
// Documentation in: https://www.npmjs.com/package/mysql2

import { createConnection } from 'mysql2';

var connection = createConnection({
	host: 'localhost', // domains.davidson.edu
	user: 'root',
	// password: '123456',
	database: 'tennishw3'
});

function connect() {
	connection.connect();
}

// copy & paste this to make one for each kind of query we want to support!!
function queryCallback(parameters, callback) {
	connection.query("SELECT * FROM player WHERE id = ?", [parameters], (error, results, fields) => {
		if (error) throw error;

		console.log(results)
		callback(results);
		// this function, provided by the user, just sends the data back to the client
	});

	// With parameters:
	// "... WHERE name = ?", ['Fernanda'], (error ...)
}

function queryPlayerByNameCallback(parameters, callback) {
	connection.query("SELECT * FROM player WHERE name = ?", [parameters], (error, results, fields) => {
		if (error) throw error;
		
		callback(results);
		// this function, provided by the user, just sends the data back to the client
	});

	// With parameters:
	// "... WHERE name = ?", ['Fernanda'], (error ...)
}

// use reg ex to get all tournaments in a certain year (since we have them stored as dates in db)
function queryTournamentByYearCallback(parameters, callback) {

	connection.query("SELECT * FROM tournament WHERE YEAR(tourn_date) = ?", [parameters], (error, results, fields) => {
		if (error) throw error;
		
		callback(results);
		// this function, provided by the user, just sends the data back to the client
	});

	// With parameters:
	// "... WHERE name = ?", ['Fernanda'], (error ...)
}

function queryShowAggregateStatisticsCallback(param1, param2, param3, callback){
	connection.query("call showAggregateStatistics(?, ?, ?)", [param1, param2, param3], (error, results) => {
		if (error) throw error;
		
		callback(results);
	
	});
}

function disconnect() {
	connection.end();
}

// Setup exports to include the external variables/functions
export {
	connection,
	connect,
	queryCallback,
	queryPlayerByNameCallback,
	queryTournamentByYearCallback,
	queryShowAggregateStatisticsCallback,
	disconnect
}

// For testing:
// connect()
// queryCallback(r => console.log(r))
// disconnect()