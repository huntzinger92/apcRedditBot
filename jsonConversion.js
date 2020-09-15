const eventLibrary = require('./eventLibrary.js');

var fs = require('fs');
var jsonLibrary = JSON.stringify(eventLibrary.eventLibrary);

fs.writeFile('txtLibrary.txt', jsonLibrary, function (err) {
  if (err)
    console.log(err);
  else
    console.log('Write operation complete.');
});
