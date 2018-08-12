var pg = require('pg');
pg.connect(process.env.DATABASE_URL, function(err, client, done) {
  if(err) {
    return console.error('Client error.', err);
  }
  
  client.query('SELECT * FROM fiction', function(err, result) {
	    done();

	    if(err) {
	      return console.error('Query error.', err);
	    }

exports.library = function(req, res){
res.render('library', { title: 'Copypasta Publishing' }, {results:result});
};