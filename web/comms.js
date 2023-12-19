 'use strict';

var I = Object.create(null);  // module's public interface

var childproc = require('child_process');
var path = require('path');
var fs = require('fs');


var _ENV;
var _NOOP = function() {};

I.init = function(env) {
  _ENV = env;
};


I.wifilist = function() {
  var scriptpath = path.join(__dirname, '..', 'WiFiNetworks.txt');
  var list = fs.readFileSync(scriptpath).toString();
  var arrWifiList = list.split('\n');
  for (var i = arrWifiList.length; i--; ) {
    if (arrWifiList[i].length === 0) arrWifiList.splice(i, 1);
  }
  return arrWifiList;
};


I.btscan = function(cb) {
  _pythScriptExec('bluetooth-list.py', /*args*/[], function(data) {
    var arrData = _btScanParse(data.toString());
    cb(arrData);
  }, function(data) {
    if (_ENV === 'dev') { // MOCK THE DATA FOR NOW in dev where I can't get bluetooth working
      data = "[('5C:3C:88:F4:62:60', 'Super novo chair'), ('00:22:37:51:DD:F6', 'SoundCore Boost')]";
      var arrData = _btScanParse(data);
      setTimeout(function() {cb(arrData)}, 2000);
    } else {
      cb(data.toString());
    }
//    cb(data.toString());
  });
};


I.btconnect = function(mac, cb) {
  if (_ENV !== 'dev') _pythScriptExec('bluetooth-connect.py', [mac]);
};


I.btWrite = function(mac) {
  _fileWrite('chosenBlueTooth.txt', mac);
};


I.profileWrite = function(code) {
  _fileWrite('chair_id.txt', code);
};


I.wifiWrite = function(ssid, pwd) {
  var text = ssid.trim() + '\n' + pwd.trim();
  _fileWrite('chosenNetwork.txt', text);
};


I.reboot = function() {
  if (_ENV !== 'dev') _scriptExec('sudo reboot');
};



function _pythScriptExec(scriptName, args, fnSuccess, fnError) {
  var spawn = childproc.spawn;
  var scriptpath = path.join(__dirname, '..', scriptName);
  var options = [scriptpath].concat(args || []); // spawn likes an array with scriptpath as the first el, followed by all the args you're passing to the actual python script
  var pythonProcess = spawn('python', options);
  if (fnSuccess) pythonProcess.stdout.on('data', fnSuccess);
  if (fnError) pythonProcess.stderr.on('data', fnError);
}


function _fileWrite(filename, text) {
  var scriptpath = path.join(__dirname, '..', filename);
  var options = { "encoding": 'utf8', "flag": 'w' }; // w = 'w': Open file for writing. The file is created (if it does not exist) or truncated (if it exists). https://nodejs.org/api/fs.html#fs_file_system_flags Ie it will overwrite whatever was there before
  fs.writeFile(scriptpath, text, options, _NOOP); // _NOOP as cb because writeFile prints an annoying deprecation warning without it
}

function _scriptExec(command) {
  childproc.exec(command, function (msg) { 
    if (_ENV === 'dev' || _ENV === 'prod') console.log(msg) 
  });
}


// output will be an array of tuples, which in string form looks like 
// [('5C:3C:88:F4:62:60', 'ALIGATOR A680'), ('00:22:37:51:DD:F6', 'SoundCore Boost')]
// so we parse that into this javascript structure
// [{"mac": '5C:3C:88:F4:62:60', "name": 'ALIGATOR A680'}, ...]
function _btScanParse(data) {
  if (data.trim() === '[]') return []; // for the case when no data was returned
  var data = data.replace('[(\'', '').replace('\')]', ''); // remove the start and end rubbish
  var arrData = data.split('\'), (\''); // now we have an array of 5C:3C:88:F4:62:60', 'ALIGATOR A680 pairs
  var arrPair;
  for (var i = 0; i < arrData.length; i++) {
    arrPair = arrData[i].split('\', \'');
    arrData[i] = { "mac": arrPair[0], "name": arrPair[1]};
    arrData[i].isNovo = _ENV === 'test' || 
                  arrData[i].name.toLowerCase().trim().indexOf('super') !== -1;
  }
  return arrData;
}



module.exports = I;
