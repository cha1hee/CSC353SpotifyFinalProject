import { createConnection } from 'mysql2';

var connection = createConnection({
	host: 'localhost',
	user: 'root',
	database: 'tennishw3'
});

function connect() {
	connection.connect();
}

function queryCallback(parameters, callback) {
	connection.query("SELECT * FROM player WHERE id = ?", [parameters], (error, results, fields) => {
		if (error) throw error;
		callback(results);
	});
}

function queryPlayerByNameCallback(parameters, callback) {
	connection.query("SELECT * FROM player WHERE name = ?", [parameters], (error, results, fields) => {
		if (error) throw error;
		callback(results);
	});
}

function queryTournamentByYearCallback(parameters, callback) {
	connection.query("SELECT * FROM tournament WHERE YEAR(tourn_date) = ?", [parameters], (error, results, fields) => {
		if (error) throw error;
		callback(results);
	});
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