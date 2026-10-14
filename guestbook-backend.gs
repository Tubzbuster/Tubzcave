/**
 * Guestbook backend for Anya's Website (free, runs on Google Apps Script + a Google Sheet).
 *
 * SETUP (about 5 minutes):
 *  1. Go to sheets.new and create a Google Sheet. Name it "Guestbook".
 *  2. In the sheet: Extensions > Apps Script. Delete the sample code and paste ALL of this file in.
 *  3. Click Deploy > New deployment > type "Web app".
 *       Execute as: Me        Who has access: Anyone
 *     Click Deploy and approve the permissions. Copy the "Web app URL" (ends in /exec).
 *  4. In index.html find   var GUESTBOOK_URL = "";   and paste the URL between the quotes. Upload index.html.
 *  5. Test it: open the guestbook on your site, send a message. A new row appears in the sheet.
 *
 * ALREADY DEPLOYED AN OLDER VERSION? Paste this over the old code, then Deploy > Manage deployments > pencil icon >
 * Version: New version > Deploy (the URL stays the same). In your sheet, type "name" in cell E1 of the Messages tab.
 *
 * MODERATION: every message is a row in the sheet. To hide one, type "no" in its "show" column (C).
 * To change this code later: Deploy > Manage deployments > edit > New version (the URL stays the same).
 */

var SHEET_NAME = 'Messages';
var MAX_MESSAGES = 200;   // how many of the newest messages the site loads

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['time', 'message', 'show', 'signature', 'name']);
  }
  return sh;
}

// The website asks for the messages (GET) -> returns them as JSON, newest last.
function doGet() {
  var rows = sheet_().getDataRange().getValues().slice(1);
  var list = rows
    .filter(function (r) { return String(r[2]).toLowerCase() !== 'no' && r[1]; })
    .map(function (r) { return { time: r[0], msg: String(r[1]), sig: String(r[3] || ''), name: String(r[4] || '') }; })
    .slice(-MAX_MESSAGES);
  return ContentService.createTextOutput(JSON.stringify(list)).setMimeType(ContentService.MimeType.JSON);
}

// The website sends a new message (POST) -> adds a row.
function doPost(e) {
  var out = ContentService.createTextOutput('ok');
  try {
    var data = JSON.parse(e.postData.contents);
    var msg = String(data.msg || '').trim().slice(0, 500);
    var sig = String(data.sig || '').trim().slice(0, 200);
    var name = String(data.name || '').trim().slice(0, 30);
    if (!msg) return out;
    // basic spam brake: skip it if the same text was just sent
    var sh = sheet_();
    var last = sh.getLastRow();
    if (last > 1 && sh.getRange(last, 2).getValue() === msg) return out;
    // stop spreadsheet formulas sneaking in ("=...", "+...", "-...", "@...")
    var safe = function (s) { return /^[=+\-@]/.test(s) ? "'" + s : s; };
    sh.appendRow([new Date().toISOString(), safe(msg), 'yes', safe(sig), safe(name)]);
  } catch (err) {}
  return out;
}
