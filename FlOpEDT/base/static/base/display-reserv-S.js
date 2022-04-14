var days_width = 150
var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;


var room_width = 100

var date_width = days_width*5
var date_height = 50
var date_margtop = 20

var each_room_y = days_y()
var each_room_height = 120

var each_text_y = days_y() + 60

var res_posy = days_y()
var res_height = 75


var room =[{}]
var each_room = [
{ "day" : "m", "room" : "Amphi1", "start": 8, "end" : 9, "name" : "PSE" },
{ "day" : "m", "room" : "Amphi2", "start": 14, "end" : 16, "name" : "PSE" },
{ "day" : "tu", "room" : "B115", "start": 8, "end" : 18, "name" : "ALE" },
{ "day" : "w", "room" : "B007", "start": 10, "end" : 14, "name" : "MCV" },
{ "day" : "w", "room" : "B007", "start": 8, "end" : 10, "name" : "MCV" },
{ "day" : "th", "room" : "B111", "start": 8, "end" : 9, "name" : "OT" },
{ "day" : "th", "room" : "B112", "start": 8, "end" : 9, "name" : "LN" }
]
var date =[{}]
/**********************
*gestion des variables*
**********************/

function days_x(day){

    return days_width*(day.num)+room_width}

function days_y(){
    return date_height+date_margtop
}


function days_height(){
    return (each_room_y - days_y())
}

function each_room_posy(){
    var y = each_room_y;
    each_room_y += each_room_height;
    return y;
}

function display_text(res){
    return res["room"]
}

function each_text_posy(){
    var y = each_text_y;
    each_text_y += each_room_height;
    return y;
}
function res_x(res){
    for (element of days){
        if (element["ref"] ==  res["day"]){
            return days_width*element["num"]+room_width
        }
    }
}

function res_y(){
var y = res_posy;
    res_posy += each_room_height;
    return y;
}

function text_heure_res(res){
    return (res["start"] + " - " + res["end"]);
}

function getday(day){
    return day["name"]
}

function getsalle(res)
{
    return res["room"]
}

/**********
*affichage*
**********/

function display_date(){
d3.select(".dates")
  .selectAll("rect")
  .data(date)
  .enter()
  .append("rect")
  .attr("class","rect_date")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",room_width)
  .attr("y",date_margtop)
  .attr("width",date_width)
  .attr("height",date_height)
}

function display_room(){
d3.select("svg")
  .select(".salles")
  .selectAll("rect_room")
  .data(room)
  .enter()
  .append("rect")
  .attr("class","rect_room")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",0)
  .attr("y",days_y)
  .attr("width",room_width)
  .attr("height",days_height())
  }

function display_each_room(){

c_room = d3.select(".salles")
  .selectAll("rect_each_room")
  .data(each_room);

c_room
  .enter()
  .append("rect")
  .attr("class","rect_each_room")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",0)
  .attr("y", each_room_posy)
  .attr("width",room_width)
  .attr("height",each_room_height);

c_room
  .enter()
  .append("text")
  .text(display_text)
  .attr("x",25)
  .attr("y", each_text_posy)

  }


function display_grid(){
c_gridall = d3.select(".grille")
  .selectAll(".rect_grid")
  .data(days)

c_grid = c_gridall
    .enter()
    .append("g")
    .attr("class",getday)


  .append("rect")
  .attr("class","rect_grid")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",days_x)
  .attr("y",days_y)
  .attr("width",days_width)
  .attr("height",days_height())
  }

function display_res(){
c_resall= d3.select(".reservation")
          .selectAll("cadre_reservation")
          .data(each_room);

c_res = c_resall
    .enter()
    .append("g")
    .attr("class",getsalle)

c_res
    .append("rect")
    .attr("class","cadre_reservation")
    .attr("fill","none")
    .attr("stroke","black")
    .attr("stroke-width",5)
    .attr("x", res_x)
    .attr("y", res_y)
    .attr("width", days_width)
    .attr("height", res_height)
/*
c_res
    .enter()
    .append("text")
    .text(text_heure_res)
    .attr("x",)
    .attr("y", )*/
}


display_date();
display_res();
display_each_room();
display_room();
display_grid();

d3.select("svg")
        .attr("height", 1000)
        .attr("width", 1000) ;


