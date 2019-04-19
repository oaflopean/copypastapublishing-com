
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , http = require('http')
   favicon = require('express-favicon')
  , path = require('path');

var app = express();
app.use(favicon(__dirname + '/public/favicon.ico'));
// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));
app.use(favicon(__dirname + '/public/favicon.ico'));
// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

var pg = require('pg');

var blog = require('./routes/blog');
var pitch = require('./routes/pitch');
var library = require('./routes/library')


app.get('/', routes.index);
app.get('/users', user.list);
app.get('/blog', blog.blog);
app.get('/ten-minute-pitch', pitch.pitch);
app.get('/library', library.library);


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
