alert("please");
var date_height = 50
var date_margin_top = 20

var echelle_width = 50
var echelle_y = cac_echelle_y()
var echelle_x = 100
var echelle_start_time = 8*60+15//495
var echelle_day_start_hour = Math.floor(echelle_start_time/60)+1
var echelle_day_start_hour_concat = echelle_day_start_hour + "h"
var echelle_end_time_day = 18*60+45 //1125
var echelle_end_time_day_hour = Math.floor(echelle_end_time_day/60)
var echelle_end_time_day_hour_concat = echelle_end_time_day_hour+ "h"
var echelle_current_hour = echelle_day_start_hour

var echelle_height = days_duration()

var days_width = 150
var days_height = days_duration()

var horaire_width = 150

var date_width = days_width*5

var each_hour_y = days_y()
var each_hour_yy = days_y()

var current_room = "414"
var another_each_case_y = another_decal_y()


var room =[{}]

var date =[{}]

var echelle =[{}]

var another = [{}]

var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;

/*
var each_reserv = [
{ "day" : "m", "room" : "Amphi1", "start": 480, "end" : 540, "name" : "PSE" },
{ "day" : "m", "room" : "Amphi2", "start": 840, "end" : 960, "name" : "PSE" },
{ "day" : "tu", "room" : "B115", "start": 480, "end" : 1080, "name" : "ALE" },
{ "day" : "w", "room" : "B007", "start": 600, "end" : 840, "name" : "MCV" },
{ "day" : "w", "room" : "B007", "start": 480, "end" : 600, "name" : "MCV" },
{ "day" : "th", "room" : "B111", "start": 480, "end" : 540, "name" : "OT" },
{ "day" : "th", "room" : "B112", "start": 480, "end" : 540, "name" : "LN" }
]
*/

/*
let courses = [
  {
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "m",
    "start": 495,
    "duration": 85,
    "room": "B102",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },
  {
    "id_course": 137456,
    "department": 'INFO',
    "mod": "IE",
    "c_type": "Projet",
    "day": "tu",
    "start": 800,
    "duration": 100,
    "room": "B102",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#FFFFFF",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },
  {
    "id_course": 137456,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "w",
    "start": 800,
    "duration": 100,
    "room": "B102",
    "room_type": "M",
    "display": false,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },
  {
    "id_course": 137457,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "th",
    "start": 585,
    "duration": 85,
    "room": "B103",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  }]
  */

let rooms = [
  {"name": "414", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[{
    "id_course": 137457,
    "department": 'INFO',
    "mod": "ExploJAVA",
    "c_type": "Projet",
    "day": "w",
    "start": 585,
    "duration": 85,
    "room": "414",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },{
    "id_course": 137458,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "w",
    "start": 700,
    "duration": 85,
    "room": "414",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd7",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },], 'th':[],'f':[]}},
  {"name": "G21", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "G26", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E209", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B111", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B002", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B203", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}}
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

function echelle_current_hour_incr() {
    var h = echelle_current_hour+1
    echelle_current_hour += 1
    return h
}

function echelle_current_hour_concat(){
    var hhh = echelle_current_hour_incr()+ "h"
    return hhh
}


function display_echelle_start_time(){
    return echelle_start_time_hour_concat
}

function display_echelle_end_time_day(){
    return echelle_end_time_day_hour_concat
}

function echelle_each_time_soixante(){
    //console.log((echelle_start_time+60)-echelle_start_time-echelle_start_time%60)
    var y = each_hour_y;
    if (y == 70) {
    //console.log("if "+each_hour_y)
    each_hour_y += ((echelle_start_time+60)-echelle_start_time-echelle_start_time%60);
    //console.log("if "+each_hour_y)
    return y    }
    each_hour_y += 60;
    //console.log(each_hour_y+" else")
    return y;
}

function course_x(day){
    for (day of days){
    console.log(day.day)
    if (day[day.ref] == "w") {
    console.log("if w")
    return days_width*(2)+horaire_width
    }

    //console.log(rooms[i].courses["w"])
    /*if (rooms[i].courses["m"] == "m"){
        return days_width*(0)+horaire_width
        }
    if (rooms[i].courses["tu"] == "tu"){
        return days_width*(1)+horaire_width
        }
    if (rooms[i].courses["w"] == "w"){
        return days_width*(2)+horaire_width
        }
    if (rooms[i].courses["th"] == "th"){
        return days_width*(3)+horaire_width
        }
    if (rooms[i].courses["f"] == "f"){
        return days_width*(4)+horaire_width
        }*/

    /*
        if (day.ref == course[day.ref]){
        console.log(2)
        console.log(days_width*element["num"]+room_width)
            return days_width*element["num"]+room_width
        }
    */
    }
}

function course_y(){
//console.log("course_y")
//console.log(/*date_height+date_margin_top-echelle_start_time+*/rooms[0].courses)
    return date_height+date_margin_top+rooms[i].start-echelle_start_time
}

function course_y_text_module(){
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+10
}

function course_y_text_c_type(){
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+25
}

function course_y_text_tutor(){
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+40
}

function another_decal_x(){
    return (days_width*(5)+horaire_width) + echelle_x
}

function another_decal_y(){
    return date_height+date_margin_top
}

function another_decal_height(){
    return (another_case_height()*rooms.length) + (another_case_height()*2)
}

function another_decal_width(){
    return 500
}


function another_case_x(){
    return another_decal_x()
}

function another_case_y(){
    var ac = another_each_case_y;
    another_each_case_y += another_case_height()
    return ac
}

function another_case_height(){
    return 70
}

function another_case_width(){
    return another_decal_width()
}

function another_case_text_x(){

}

function another_case_text_y(){

}

function another_case_text(){

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
  .attr("stroke-width",2)
  .attr("x",echelle_x)
  .attr("y",echelle_y)
  .attr("width",echelle_width)
  .attr("height",echelle_height)

  c_echelle
  .append("text")
  .text("")
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

  c_echelle
  .append("text")
  .text(echelle_day_start_hour_concat)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)


  for (hh = echelle_current_hour+1; hh<echelle_end_time_day_hour; hh++){
  c_echelle
  .append("text")
  .text(echelle_current_hour_concat)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)
}

  c_echelle
  .append("text")
  .text(echelle_end_time_day_hour_concat)
  .attr("x",110)
  .attr("y", echelle_each_time_soixante)

}

/*
function display_reservation(){
    c_reservations = d3.select(".reservations")
    .selectAll("rect")
    .data(rooms)
    .enter();

    //console.log(rooms.length)
    //for (i=0; i<rooms.length;i++){
    //    if (rooms[i].display == true) {
    //        //console.log(rooms[i].name)
    //        if (current_room == rooms[i].name) {
    //           for day in days:
    //                x = course_x(day)
    //                days_courses = room_object.courses[day.ref]
    //                for course in days_courses:
    //                   y =

    //console.log(rooms.length)
    for (i=0; i<rooms.length;i++) {
        if (current_room == room[i].name) {
            if (rooms[i].display == true){
                for (day of days) {
                    console.log(rooms[i].name)
                    c_reservations
                        .append("rect")
                        .attr("class", "rect_grid")
                        .attr("fill","none") //rooms[i].color_bg
                        .attr("stroke", "black")
                        .attr("x", course_x(day))
                        days_courses = .courses[day.ref]
                            for (course of days_courses) {
                                .attr("y", course_y)
                                .attr("width", days_width)
                                .attr("height", rooms[i].duration)
                            }
                }
            }
        }
    }

                //console.log(rooms[i].name)
                c_reservations
                    .append("rect")
                    .attr("class", "rect_grid")
                    .attr("fill",rooms[i].color_bg)
                    .attr("stroke", "black")
                    .attr("x", course_x(rooms[i].courses))
                    .attr("y", course_y)
                    .attr("width", days_width)
                    .attr("height", rooms[i].duration)

                c_reservations
                    .append("text")
                    .text(rooms[i].mod)
                    .attr("x", course_x(rooms[i].day)+50)
                    .attr("y", course_y_text_module)
                    //.attr("style_color", rooms[i].color_txt)

                c_reservations
                    .append("text")
                    .text(rooms[i].c_type)
                    .attr("x", course_x(rooms[i].day)+50)
                    .attr("y", course_y_text_c_type)
                    //.attr("style.color", rooms[i].color_txt)

                c_reservations
                    .append("text")
                    .text(rooms[i].tutor)
                    .attr("x", course_x(rooms[i].day)+50)
                    .attr("y", course_y_text_tutor)
                    //.attr("text_color", rooms[i].color_txt)
            }
*/

function display_another(){
  c_another = d3.select(".anothers")
  .selectAll("rect")
  .data(another)
  .enter();

  c_another
  .append("rect")
  .attr("class","rect_another")
  .attr("fill","none")
  .attr("stroke","red")
  .attr("stroke-width",2)
  .attr("x",another_decal_x)
  .attr("y",another_decal_y)
  .attr("width",another_decal_width)
  .attr("height",another_decal_height)

  c_another
  .append("rect")
  .attr("class","rect_another")
  .attr("fill","none")
  .attr("stroke","grey")
  .attr("stroke-width",2)
  .attr("x",another_case_x)
  .attr("y",another_case_y)
  .attr("width",another_case_width)
  .attr("height",another_case_height)

  c_another
  .append("rect")
  .attr("class","rect_another")
  .attr("fill","none")
  .attr("stroke","grey")
  .attr("stroke-width",2)
  .attr("x",another_case_x)
  .attr("y",another_case_y)
  .attr("width",another_case_width)
  .attr("height",another_case_height)

  for (ia = 0; ia < rooms.length; ia++){
      c_another
      .append("rect")
      .attr("class","rect_another")
      .attr("fill","none")
      .attr("stroke","blue")
      .attr("stroke-width",2)
      .attr("x",another_case_x)
      .attr("y",another_case_y)
      .attr("width",another_case_width)
      .attr("height",another_case_height)
  }

}

/*******
*display*
 ******/

 function main() {
    display_date();
    display_grid();
    display_echelle();
    //display_reservation();
    display_another();
    alert("please");
 }


d3.select("svg")
        .attr("height", 1600)
        .attr("width", 1600) ;
