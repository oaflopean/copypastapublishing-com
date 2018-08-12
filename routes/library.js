exports.library = function(req, res){
	var pg = require('pg');
	pg.connect(conString, function (err, client, done) {
	    if (err) {
	      // pass the error to the express error handler
	      return next(err)
	    }
	    client.query('SELECT * FROM fiction;', [], function (err, result) {
	      done()

	      if (err) {
	        // pass the error to the express error handler
	        return next(err)
	      }

	      res.render('pitch', { title: 'Copypasta Publishing' }, {results:result});
	    })})};