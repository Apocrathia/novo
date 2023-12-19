'use strict';

// ------------------------------------------------------------------------------------
// Dependencies

var http         = require('http');
var express      = require('express');
var bodyParser   = require('body-parser'); // parse out html requests with stuff in the body like JSON
var hbs          = require('handlebars');
var winston      = require('winston');
var fs           = require('fs');
var path         = require('path');

var comms        = require('./comms');

var app = express();



// ------------------------------------------------------------------------------------
// Config

var _ENV = 'prod';
var _LISTENPORT = _ENV === 'dev' ? '3333' : '9999';



// ------------------------------------------------------------------------------------
// Init libs 

comms.init(_ENV.toLowerCase());


    
// ------------------------------------------------------------------------------------
// Final outputs of the novo setup process

var _userAddressChosen; // mac address of the novo chair
var _userProfileCode; // the user account profile code which links this wifi bridge device to the user's voice commands from their Alexa
var _wifiSSID; // the user's wifi router SSID
var _wifiPwd; // ...and password



// ------------------------------------------------------------------------------------
// Site structure

// NOTE: each page in _pages may later receive the property
// tplExec: the pre-compiled handlebars template which can be executed 
// with the tokens to create the final page
var _pages = {
    "landing":    { "tpl": 'landing.tpl.html' }
  , "bluetooth":  { "tpl": 'bluetooth.tpl.html' }
  , "profile":    { "tpl": 'profile.tpl.html' }
  , "wifichoose": { "tpl": 'wifichoose.tpl.html' }
  , "wifipwd":    { "tpl": 'wifipwd.tpl.html' }
  , "confirm":    { "tpl": 'confirm.tpl.html' }
  , "final":      { "tpl": 'final.tpl.html' }
  , "edit":       { "tpl": 'edit.tpl.html' }
};


function _pagesInit() {
  var arrPages = Object.keys(_pages);
  var page;
  var pathToFile;
  var tpl;
  for (var i = 0; i < arrPages.length; i++) {
    page = _pages[arrPages[i]];
    pathToFile = path.join(__dirname, 'tpl', page.tpl);
    tpl = fs.readFileSync(pathToFile, 'utf-8');
    page.tplExec = hbs.compile(tpl);
  }
}


_pagesInit();



// ------------------------------------------------------------------------------------
// Page rendering

var _arrWifiList; // temporarily store the list of wifi router SSIDs

function _landing(req, res, next) {
  var page = _pages.landing.tplExec();
  res.send(page);
  if (!_arrWifiList) _arrWifiList = comms.wifilist();
}


var _arrBTAddresses; // temporarily store the list of nearby bluetooth devices
var _scanningNow;

function _bluetooth(req, res, next) {
  if (!_arrBTAddresses) { // First bluetooth page, "Scanning"
    var tokens = { "BTSTATESCANNING": true };
    _bluetoothRender(tokens, res);
    if (!_scanningNow) {
      _scanningNow = true;
      comms.btscan(function(data) {
        if (_ENV === 'dev' || _ENV === 'test') console.log(data);
        _scanningNow = false;
        _arrBTAddresses = data;
      });
    }
  } else { // Second bluetooth page, "Choose"
    var tokens = { 
        "BTSTATECHOOSE": true
      , "DEVICES": _arrBTAddresses
      , "HAVEDEVICES": _arrBTAddresses.length 
    };
    _bluetoothRender(tokens, res);
  }
}


function _bluetoothRender(tokens, res) {
  var page = _pages.bluetooth.tplExec(tokens);
  res.send(page);
}


function _bluetoothAction(req, res, next) {
  if (req.body.mac) { // Third bluetooth page, "Connecting to novo"
    _userAddressChosen = req.body.mac;
    if (_ENV === 'dev' || _ENV === 'test') console.log(_userAddressChosen, 'chosen');
    _bluetoothRender({}, res);
    if (_ENV !== 'dev') comms.btconnect(_userAddressChosen);
  } else if (req.body.rescan) { // Returning from anywhere to First bluetooth page
    _arrBTAddresses = null;
    _scanningNow = false;
    _userAddressChosen = null;
    _bluetooth(req, res, next);
  }
}


function _btcheck(req, res, next) {
  var msg = _arrBTAddresses ? 'ready' : '';
  res.send(msg);
}


function _profile(req, res, next) {
  var page = _pages.profile.tplExec();
  res.send(page);
}


function _wifichoose(req, res, next) {
  if (req.body.profilecode) _userProfileCode = req.body.profilecode; // the if (req.body.profilecode) is a hack to ensure this isn't removed if the user navigates to /profile from the /edit screen
  var tokens = { "WIFILIST": _arrWifiList };
  var page = _pages.wifichoose.tplExec(tokens);
  res.send(page);
}


function _wifipwd(req, res, next) {
  _wifiSSID = req.body.ssid;
  var tokens = { "WIFICHOSEN": _wifiSSID };
  var page = _pages.wifipwd.tplExec(tokens);
  res.send(page);
}


function _confirm(req, res, next) {
  if (req.body.wifipwd) _wifiPwd = req.body.wifipwd;  // the if (req.body.wifipwd) is a hack to ensure this isn't removed if the user navigates to /profile from the /edit screen
  var tokens = {
      "PROFILECODE": _userProfileCode
    , "WIFICHOSEN": _wifiSSID
    , "WIFIPWD": _wifiPwd
  };
  var page = _pages.confirm.tplExec(tokens);
  res.send(page);
}


// Write all the details for the user at this final page after user has 
// "confirmed" them all. This serves as a kind of "transaction" which makes
// sure that the whole setup process either succeeds entirely or fails 
// entirely. In the latter case, the user can start the process again without 
// fear of any weird "half configured" behaviour upon reboots, etc.
// After writing the server is rebooted and then will come up with no 
// hotspot, but with the wifi and bluetooth connections working instead
// which is the desired result of the setup process.
function _final(req, res, next) {
  var page = _pages.final.tplExec();
  res.send(page);
  comms.btWrite(_userAddressChosen.trim()); // write to file chosenBlueTooth.txt
  comms.profileWrite(_userProfileCode.trim()); // write to file chair_id.txt
  comms.wifiWrite(_wifiSSID, _wifiPwd.trim()); // write to file chosenNetwork.txt
  setTimeout(comms.reboot, 15000);
}

function _edit(req, res, next) {
  var page = _pages.edit.tplExec();
  res.send(page);
}



// ------------------------------------------------------------------------------------
// Web server setup

// 1. set up middleware

app.use(bodyParser.urlencoded({ extended: true }));
  

// 2. set up app routes

app.get('/', _landing); 
app.get('/bluetooth', _bluetooth);  // handles the first two "Bluetooth" screens, which are HTTP Gets
app.post('/bluetooth', _bluetoothAction);  // handles the final screen and the action to return back to the start of the Bluetooth process (RE-SCAN)
app.get('/btcheck', _btcheck); // async XHR to make the bluetooth polling process smooth - ie without whole page postbacks which can make the page otherwise appear to "blip"
app.get('/profile', _profile);
app.post('/wifichoose', _wifichoose);
app.post('/wifipwd', _wifipwd);
app.post('/confirm', _confirm);
app.get('/final', _final);
app.get('/edit', _edit);



// 3. static files web server (long cached)
// Other routes take precedence, so make sure static .use comes 
// after those routes

function _cacheStatic(res) {
  var cacheIf = _ENV.toLowerCase() === 'dev' || _ENV.toLowerCase() === 'test';
  var cacheSecs = cacheIf ? '0' : '3600'; // cache for an hour in production
  res.setHeader('cache-control', 'public, max-age=' + cacheSecs);
}

var staticOptions = { "setHeaders": _cacheStatic };  // cache static files for a day: http://evanhahn.com/express-dot-static-deep-dive/
var staticFilePath = path.join(__dirname, 'static');
app.use(express.static(staticFilePath, staticOptions));



// ------------------------------------------------------------------------------------
// Create and start HTTP server (not HTTPS)

function _initWebServer() { 
  http.createServer(app).listen(_LISTENPORT);
  if (_ENV === 'dev' || _ENV === 'test') {
    winston.log('info', 'Server listening on port ' + _LISTENPORT );
  }
}


_initWebServer();