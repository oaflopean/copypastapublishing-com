exports.pitch = function(req, res){
res.render('pitch', { title: 'Copypasta Publishing: Magenta Madness and Prismatic Displays' });
};
exports.invitation = function(req, res){
res.render('invite.html', { title: 'Huge Impossible Word Search' });
};
