var date_height = 50
var date_margin_top = 20

var echelle_width = 50
var echelle_y = cac_echelle_y()
var echelle_x = 100
var echelle_start_time = 8*60+15 //495
var echelle_end_time_day = 18*60+45 //1005
var echelle_day_start_hour = ~~(echelle_start_time/60)
var echelle_day_start_min = echelle_start_time%60
var echelle_day_start_concat = echelle_day_start_hour + "h" + echelle_day_start_min
var echelle_end_time_day_hour = ~~(echelle_end_time_day/60)
var echelle_end_time_day_min = echelle_end_time_day%60
var echelle_end_time_day_concat = echelle_end_time_day_hour + "h" + echelle_end_time_day_min
var echelle_height = days_duration()

var days_width = 150
var days_height = days_duration()

var horaire_width = 150

var date_width = days_width*5


var each_hour_y = days_y()
var each_hour_yy = days_y()

var each_time_text = 9


/*
// a changer
var each_case_y = days_y()
var each_case_height = 120 //(each_reserv.end-each_reserv.start)*2
*/

/*
// a changer
var res_posy = days_y()
var res_height = 110 // each_case_height
*/


var room =[{}]

var date =[{}]

var echelle =[{}]

var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;

var each_reserv = [
{ "day" : "m", "room" : "Amphi1", "start": 480, "end" : 540, "name" : "PSE" },
{ "day" : "m", "room" : "Amphi2", "start": 840, "end" : 960, "name" : "PSE" },
{ "day" : "tu", "room" : "B115", "start": 480, "end" : 1080, "name" : "ALE" },
{ "day" : "w", "room" : "B007", "start": 600, "end" : 840, "name" : "MCV" },
{ "day" : "w", "room" : "B007", "start": 480, "end" : 600, "name" : "MCV" },
{ "day" : "th", "room" : "B111", "start": 480, "end" : 540, "name" : "OT" },
{ "day" : "th", "room" : "B112", "start": 480, "end" : 540, "name" : "LN" }
]



/**********************
*gestion des variables*
**********************/

function days_duration(){
    return (echelle_end_time_day-echelle_start_time)}

function days_x(day){
    return days_width*(day.num)+horaire_width}

function days_y(){
    return date_height+date_margin_top
}

function getday(day){
    return day["name"]
}

function cac_echelle_y(){
    return date_height+date_margin_top
}

function display_echelle_start_time(){
    return echelle_start_time
}

function display_echelle_end_time_day(){
    return echelle_end_time_day
}

function echelle_each_time_quaranteCinq(){
    var y = each_hour_y;
    each_hour_y += 45;
    return y;
}

function echelle_each_time_quaranteCinq_h(){
    var yy = each_hour_yy;
    each_hour_yy += 45;
    return yy;
}

function echelle_each_time_soixante(){
    var y = each_hour_y;
    each_hour_y += 60;
    return y;
}

function echelle_each_time_soixante_h(){
    var yy = each_hour_yy;
    each_hour_yy += 60;
    //console.log(yy)
    return yy;
}

function echelle_each_time_text(){
    var yyy = each_time_text;
    each_time_text += 1;
    console.log(yyy);
    return yyy;
}

 /***************
*function display*
 ***************/

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
  .attr("x",horaire_width)
  .attr("y",date_margin_top)
  .attr("width",date_width)
  .attr("height",date_height)
}


function display_grid(){
c_gridall = d3.select(".grille")
  .selectAll("rect_grid")
  .data(days)

c_grid = c_gridall
    .enter()
    .append("g")
    .attr("class",getday)

  .append("rect")
  .attr("class","rect_grid")
  .attr("fill","none")
  .attr("stroke","green")
  .attr("stroke-width",5)
  .attr("x",days_x)
  .attr("y",days_y)
  .attr("width",days_width)
  .attr("height",days_height)
  }


function display_echelle(){
c_echelle = d3.select(".echelles")
  .selectAll("rect")
  .data(echelle)
  .enter();

  c_echelle
  .append("rect")
  .attr("class","rect_echelle")
  .attr("fill","none")
  .attr("stroke","blue")
  .attr("stroke-width",5)
  .attr("x",echelle_x)
  .attr("y",echelle_y)
  .attr("width",echelle_width)
  .attr("height",echelle_height)

  c_echelle
  .append("text")
  .text(echelle_day_start_concat)
  .attr("x",110)
  .attr("y", echelle_each_time_quaranteCinq)

  c_echelle
  .append("text")
  .text("")
  .attr("x",130)
  .attr("y", echelle_each_time_quaranteCinq_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_soixante_h)

  c_echelle
  .append("text")
  .text(echelle_each_time_text)
  .attr("x",110)
  .attr("y", echelle_each_time_quaranteCinq)

  c_echelle
  .append("text")
  .text("h")
  .attr("x",130)
  .attr("y", echelle_each_time_quaranteCinq_h)

  c_echelle
  .append("text")
  .text(echelle_end_time_day_concat)
  .attr("x",105)
  .attr("y", echelle_each_time_quaranteCinq)

    c_echelle
  .append("text")
  .text("")
  .attr("x",130)
  .attr("y", echelle_each_time_quaranteCinq_h)

}

/*******
*display*
 ******/
display_date();
display_grid();
display_echelle();

d3.select("svg")
        .attr("height", 1600)
        .attr("width", 1600) ;

/* 60min*12h(8h->19h) = 720min *2= 1440pix
 12h = 1400pix
 1h = 60min = 120pix
 1min = 2pix */

/*  let start_time = 8*60+15
    let end_time_day = 18*60+45 */

