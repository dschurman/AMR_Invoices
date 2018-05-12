function doGet(e) {
  // params - "name" describes name of sheet (should be tenant name)
  var sheetName = "";
  
  // check for "name" parameter
  if(e.parameters.hasOwnProperty("name")) {
    sheetName = e.parameters["name"][0]
    // log most recent data to sheet 
    logSheet(sheetName)
  } else {
    ContentService.createTextOutput("Missing parameters: name");
  }
  
  // if "query" is true, return last entry in given tenant's sheet
  if(e.parameters.hasOwnProperty("query")) {
    if(e.parameters["query"][0].equals("true")) {
      return querySheet(sheetName)
    }
  }
  return ContentService.createTextOutput("Success");
}

function logSheet(sheetName) {
  // each tenant's monthly rent rate
  TENANT_RATES = {"Jack_Roswell":3400.00, "Alex_Zhuk":56321.99, "Rashid_Zia":1931.26, "Elizabeth_Austin":12.00}
  // cost per kilowatt-hour
  POWER_MULTIPLIER = 0.12
  // get file with specified name from Drive
  var fileIterator = DriveApp.getFilesByName("Tenant Invoice History");
  // get spreadsheet
  var spreadsheetID = fileIterator.next().getId();
  var spreadsheet = SpreadsheetApp.openById(spreadsheetID);
  // load sheet, create new if not found 
  var thisSheet = spreadsheet.getSheetByName(sheetName);
  if(thisSheet == null) {
    thisSheet = spreadsheet.insertSheet(sheetName);
    // at creation, append relevant field headers
    thisSheet.appendRow(["Date Issued", "Total Amount", "Power Consumption This Month (kWh)", "Total Power Consumption (kWh)", "Power Rate ($/kWh)", "Monthly Rent ($)"]);
  }
  
  // get updated usage from database
  var url = "http://dschurma.pythonanywhere.com/query_by_tenant?name=" + sheetName; 
  var resp = JSON.parse(UrlFetchApp.fetch(url));
  // parse data fields from response
  var currentTotalUsage = parseInt(resp["current_month"]);
  var change = parseInt(resp["change"]);
  var rent = TENANT_RATES[sheetName];
  
  // append to new row of sheet
  var lastRow = thisSheet.getLastRow();
  var lastCol = thisSheet.getLastColumn();
  
  var newRange = thisSheet.getRange(lastRow + 1, 1, 1, lastCol);
  // fields: ["Date Issued", "Total Amount", "Power Consumption This Month (kWh)", "Total Power Consumption (kWh)", "Power Rate ($/kWh)", "Monthly Rent ($)"]
  var newVals = [[Utilities.formatDate(new Date(), "EST", "yyyy-MM-dd"), change * POWER_MULTIPLIER + rent, change, currentTotalUsage, POWER_MULTIPLIER, rent]];
  newRange.setValues(newVals);
}

function querySheet(name) {
  // get files with specified name from Drive
  var fileIterator = DriveApp.getFilesByName("Tenant Invoice History");
  // get spreadsheet and sheet
  var spreadsheetID = fileIterator.next().getId();
  var spreadsheet = SpreadsheetApp.openById(spreadsheetID);
  var thisSheet = spreadsheet.getSheetByName(name);
  
  // get last row of values
  var lastRow = thisSheet.getLastRow();
  var lastCol = thisSheet.getLastColumn();
  var vals = thisSheet.getSheetValues(lastRow, 1, 1, lastCol)[0]
  
  // return json object containing all data values
  return ContentService.createTextOutput(JSON.stringify({"date":vals[0], "amt":vals[1], "month_cons":vals[2], "tot_cons":vals[3], "pow_rate":vals[4], "rent":vals[5]})).setMimeType(ContentService.MimeType.JSON);
}

