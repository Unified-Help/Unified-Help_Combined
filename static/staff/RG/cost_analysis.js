//--------------- Camapign Costs Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   cc_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cc_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cc_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cc_seriesData_1 = cc_data.mapAs({x: 0, value: 1});
var cc_seriesData_2 = cc_data.mapAs({x: 0, value: 2});
var cc_seriesData_3 = cc_data.mapAs({x: 0, value: 3});

  // create line chart
cc_chart = anychart.line();

//plotting each series line and setting each series name
var cc_series1 = cc_chart.line(cap_seriesData_1);
  cc_series1.name("Cost 1")
var cc_series2 = cc_chart.line(cap_seriesData_2);
  cc_series2.name("Cost 2")
var cc_series3 = cc_chart.line(cap_seriesData_3);
  cc_series3.name("Cost 3")

// Animation, legend and axis titles
cc_chart.animation(true);
cc_chart.legend(true);
cc_chart.xAxis().title("Month/Year")
cc_chart.yAxis().title("Costs")
//horizontal grid lines
cc_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cc_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cc_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cc_chart.container('CC_container').draw();
});

// load initial data on button click
function cc_thisYear(){
  cc_chart.getSeries(0).data(cc_data);
}

function cc_previousYear() {
  cc_chart.getSeries(0).data(cc_data1);
}

function cc_last5Years(){
  cc_chart.getSeries(0).data(cc_data2);
}

//---------------- Inventory Storage Costs Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   isc_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  isc_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  isc_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var isc_seriesData_1 = isc_data.mapAs({x: 0, value: 1});
var isc_seriesData_2 = isc_data.mapAs({x: 0, value: 2});
var isc_seriesData_3 = isc_data.mapAs({x: 0, value: 3});

  // create line chart
isc_chart = anychart.line();

//plotting each series line and setting each series name
var isc_series1 = isc_chart.line(cap_seriesData_1);
  isc_series1.name("Cost 1")
var isc_series2 = isc_chart.line(cap_seriesData_2);
  isc_series2.name("Cost 2")
var isc_series3 = isc_chart.line(isc_seriesData_3);
  isc_series3.name("Cost 3")

// Animation, legend and axis titles
isc_chart.animation(true);
isc_chart.legend(true);
isc_chart.xAxis().title("Month/Year")
isc_chart.yAxis().title("Costs")
//horizontal grid lines
isc_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
isc_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  isc_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  isc_chart.container('ISC_container').draw();
});

// load initial data on button click
function isc_thisYear(){
  isc_chart.getSeries(0).data(isc_data);
}

function isc_previousYear() {
  isc_chart.getSeries(0).data(isc_data1);
}

function isc_last5Years(){
  isc_chart.getSeries(0).data(isc_data2);
}

//--------------- Charitable activities expenses Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   cap_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cap_seriesData_1 = cap_data.mapAs({x: 0, value: 1});
var cap_seriesData_2 = cap_data.mapAs({x: 0, value: 2});
var cap_seriesData_3 = cap_data.mapAs({x: 0, value: 3});

  // create line chart
cap_chart = anychart.line();

//plotting each series line and setting each series name
var cap_series1 = cap_chart.line(cap_seriesData_1);
  cap_series1.name("Cost 1")
var cap_series2 = cap_chart.line(cap_seriesData_2);
  cap_series2.name("Cost 2")
var cap_series3 = cap_chart.line(cap_seriesData_3);
  cap_series3.name("Cost 3")

// Animation, legend and axis titles
cap_chart.animation(true);
cap_chart.legend(true);
cap_chart.xAxis().title("Month/Year")
cap_chart.yAxis().title("Costs")
//horizontal grid lines
cap_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cap_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cap_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cap_chart.container('CAP_container').draw();
});

// load initial data on button click
function CAP_thisYear(){
  cap_chart.getSeries(0).data(cap_data);
}

function CAP_previousYear() {
  cap_chart.getSeries(0).data(cap_data1);
}

function CAP_last5Years(){
  cap_chart.getSeries(0).data(cap_data2);
}

// Setting the data
anychart.onDocumentReady(function () {
   cap_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cap_seriesData_1 = cap_data.mapAs({x: 0, value: 1});
var cap_seriesData_2 = cap_data.mapAs({x: 0, value: 2});
var cap_seriesData_3 = cap_data.mapAs({x: 0, value: 3});

  // create line chart
cap_chart = anychart.line();

//plotting each series line and setting each series name
var cap_series1 = cap_chart.line(cap_seriesData_1);
  cap_series1.name("Cost 1")
var cap_series2 = cap_chart.line(cap_seriesData_2);
  cap_series2.name("Cost 2")
var cap_series3 = cap_chart.line(cap_seriesData_3);
  cap_series3.name("Cost 3")

// Animation, legend and axis titles
cap_chart.animation(true);
cap_chart.legend(true);
cap_chart.xAxis().title("Month/Year")
cap_chart.yAxis().title("Costs")
//horizontal grid lines
cap_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cap_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cap_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cap_chart.container('CAP_container').draw();
});

// load initial data on button click
function CAP_thisYear(){
  cap_chart.getSeries(0).data(cap_data);
}

function CAP_previousYear() {
  cap_chart.getSeries(0).data(cap_data1);
}

function CAP_last5Years(){
  cap_chart.getSeries(0).data(cap_data2);
}

//--------------- Fund Raising Expenses Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   cap_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cap_seriesData_1 = cap_data.mapAs({x: 0, value: 1});
var cap_seriesData_2 = cap_data.mapAs({x: 0, value: 2});
var cap_seriesData_3 = cap_data.mapAs({x: 0, value: 3});

  // create line chart
cap_chart = anychart.line();

//plotting each series line and setting each series name
var cap_series1 = cap_chart.line(cap_seriesData_1);
  cap_series1.name("Cost 1")
var cap_series2 = cap_chart.line(cap_seriesData_2);
  cap_series2.name("Cost 2")
var cap_series3 = cap_chart.line(cap_seriesData_3);
  cap_series3.name("Cost 3")

// Animation, legend and axis titles
cap_chart.animation(true);
cap_chart.legend(true);
cap_chart.xAxis().title("Month/Year")
cap_chart.yAxis().title("Costs")
//horizontal grid lines
cap_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cap_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cap_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cap_chart.container('CAP_container').draw();
});

// load initial data on button click
function CAP_thisYear(){
  cap_chart.getSeries(0).data(cap_data);
}

function CAP_previousYear() {
  cap_chart.getSeries(0).data(cap_data1);
}

function CAP_last5Years(){
  cap_chart.getSeries(0).data(cap_data2);
}

//--------------- Administration Costs Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   cap_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cap_seriesData_1 = cap_data.mapAs({x: 0, value: 1});
var cap_seriesData_2 = cap_data.mapAs({x: 0, value: 2});
var cap_seriesData_3 = cap_data.mapAs({x: 0, value: 3});

  // create line chart
cap_chart = anychart.line();

//plotting each series line and setting each series name
var cap_series1 = cap_chart.line(cap_seriesData_1);
  cap_series1.name("Cost 1")
var cap_series2 = cap_chart.line(cap_seriesData_2);
  cap_series2.name("Cost 2")
var cap_series3 = cap_chart.line(cap_seriesData_3);
  cap_series3.name("Cost 3")

// Animation, legend and axis titles
cap_chart.animation(true);
cap_chart.legend(true);
cap_chart.xAxis().title("Month/Year")
cap_chart.yAxis().title("Costs")
//horizontal grid lines
cap_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cap_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cap_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cap_chart.container('CAP_container').draw();
});

// load initial data on button click
function CAP_thisYear(){
  cap_chart.getSeries(0).data(cap_data);
}

function CAP_previousYear() {
  cap_chart.getSeries(0).data(cap_data1);
}

function CAP_last5Years(){
  cap_chart.getSeries(0).data(cap_data2);
}

//--------------- Utilities Costs Line Chart ---------------//

// Setting the data
anychart.onDocumentReady(function () {
   cap_data = anychart.data.set([
  ["Jake", 637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data1 = anychart.data.set([
  ["Jake", 1637166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

  cap_data2 = anychart.data.set([
  ["Jake", 837166, 737166, 813000],
  ["John", 721630, 537166, 128013],
  ["Peter", 148662, 188662, 194912],
  ["James", 78662, 178662, 612037],
  ["Mary", 90000, 89000, 375913]
]);

//Mapping each sub category to a line series
var cap_seriesData_1 = cap_data.mapAs({x: 0, value: 1});
var cap_seriesData_2 = cap_data.mapAs({x: 0, value: 2});
var cap_seriesData_3 = cap_data.mapAs({x: 0, value: 3});

  // create line chart
cap_chart = anychart.line();

//plotting each series line and setting each series name
var cap_series1 = cap_chart.line(cap_seriesData_1);
  cap_series1.name("Cost 1")
var cap_series2 = cap_chart.line(cap_seriesData_2);
  cap_series2.name("Cost 2")
var cap_series3 = cap_chart.line(cap_seriesData_3);
  cap_series3.name("Cost 3")

// Animation, legend and axis titles
cap_chart.animation(true);
cap_chart.legend(true);
cap_chart.xAxis().title("Month/Year")
cap_chart.yAxis().title("Costs")
//horizontal grid lines
cap_chart.yGrid().enabled(true);
// y axis uniform scaling
var customScale = anychart.scales.linear();
customScale.minimum(0);
customScale.maximum(2000000);
var customTicks = customScale.ticks();
customTicks.interval(100000);
cap_chart.yScale(customScale);

  {% raw %}
  // configure axis labels
  cap_chart.yAxis().labels().format('${%value}{scale:(1000)(1000)|(k)(m)}');
  {% endraw %}

  // set container id and display chart
  cap_chart.container('CAP_container').draw();
});

// load initial data on button click
function CAP_thisYear(){
  cap_chart.getSeries(0).data(cap_data);
}

function CAP_previousYear() {
  cap_chart.getSeries(0).data(cap_data1);
}

function CAP_last5Years(){
  cap_chart.getSeries(0).data(cap_data2);
}
