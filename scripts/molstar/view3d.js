
function makeAtlas(data,id) {
var txt = "";
var txt1="";

//extract table from json
if (data.response.numFound == 0)
{txt += "<div class='alert alert-info' role='alert'><p>No entry found for PDBDEV_" + id + "</p></div>";
$('#results').append(txt); return;}

var jdata = data.response.docs[0];



txt += "<div class='card-header' style='padding-bottom: 6px; padding-top: 12px; background-color: #003366; color: white; border-radius: 0; border: none; margin-bottom: 0px;'>";
txt += "<div class='row'><div class='col-sm-10'><h4 class='card-title'>PDBDEV_" + id + "</h4></div>";
//txt += "<div class='col-sm-2'><div class='float-right'><button type='button'class='btn' data-toggle='tooltip' style='background-color: #669966; height: 34px;'><a  href='/solrseach.html' target = '_blank'><span style='color: #FFF;margin-bottom: 16px;'>Start New Search</span></a></button></div></div>";

txt += "<div class='col-sm-2'><div class='float-right'><a  href='/solrsearch.html' target = '_blank'><button type='button' class='button' data-toggle='tooltip' style='background-color: #669966; color: #FFF; margin-right:13px; height: 34px; width: 11em; border-radius: 12px;cursor: pointer; font-size:0.9em;'>Start New Search</button></a></div></div>";

txt += "</div></div>";

$('#results').append(txt);

txt1 +="<div>";
txt1 += "<p>" + jdata['struct.title']  + "</p>";
txt1 +="</div>";
$('#results1').append(txt1);

} //end makeAtlas

function getPDBentry() {
$('#results').empty();
var query = $('#query').val().toString();



document.title = "PDBDEV_" + query;

//???
//var hosturl='http://localhost:8983/solr/ihmnew/select';
//var hosturl='http://pdb-dev.wwpdb.org:8983/solr/ihmnew/select';
var hosturl='/node/solr/ihmnew/select';
var jsonData;
var queryid = "entry.id:PDBDEV_" + query;



$.ajax({
traditional: true,
url: hosturl,
data: { 'q' : queryid },
success : function(data) { makeAtlas(data,query) },
error: function() {
  $('#results').prepend('<div class="alert alert-warning" role="alert"><b>'
   + 'Query or server problem</b></div>');},
//complete: function(jqXHR,textStatus) {
//  $('#results').prepend('<div class="alert alert-primary" role="alert"><b>'
//   + textStatus  + ' : ' + this.url + '</b></div>'); },
dataType: "jsonp",
jsonp : 'json.wrf'
}) ;
}


function on_ready() {

getPDBentry();
$('body').keypress(function(e) { if (e.keyCode == '13') {
var element = document.getElementById("opentab");
element.value = "sum";
getPDBentry() }
});
}


