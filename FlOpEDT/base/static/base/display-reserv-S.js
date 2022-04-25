/**********************
*Définition des variables*
**********************/

var date_height = 50
var date_margin_top = 20

var echelle_width = 50
var echelle_x = 100

var echelle_start_time = 8*60+15//495
var echelle_end_time_day = 18*60+45 //1125

var days_width = 150

/* set to 150 for no margin between the schedule and the days */
var horaire_width = 150

var current_room = "414"

var room =[{}]
var date =[{}]
var echelle =[{}]

/**********************
*gestion des variables*
**********************/

/*-- date --*/
function date_width() {
    return days_width*5
}

/*-- days --*/
function days_duration() {
    return (echelle_end_time_day-echelle_start_time)}

function days_x(day) {
    return days_width*(day.num)+horaire_width}

function days_y() {
    return date_height+date_margin_top
}

function days_height() {
    return days_duration()
}

function getday(day) {
    return day["name"]
}

/*-- echelle --*/
function cac_echelle_y() {
    return date_height+date_margin_top
}

function echelle_y() {
    return cac_echelle_y()
}

function echelle_height() {
    return days_duration()
}

function echelle_day_start_hour() {
	return Math.floor(echelle_start_time/60)+1
}

var echelle_current_hour = echelle_day_start_hour()
function echelle_current_hour_incr() {
    var h = echelle_current_hour+1
    echelle_current_hour += 1
    return h
}

function echelle_current_hour_concat() {
    var hhh = echelle_current_hour_incr()+ "h"
    return hhh
}

function echelle_day_start_hour_concat() {
	return echelle_day_start_hour() + "h"
}

function echelle_end_time_day_hour() {
	return Math.floor(echelle_end_time_day/60)
}

function echelle_end_time_day_hour_concat() {
	return echelle_end_time_day_hour + "h"
}

function display_echelle_start_time() {
    return echelle_start_time_hour_concat
}

function display_echelle_end_time_day() {
    return echelle_end_time_day_hour_concat()
}

var each_hour_y = days_y()
function echelle_each_time_soixante() {
    var y = each_hour_y;
    if (y == 70) {
    each_hour_y += ((echelle_start_time+60)-echelle_start_time-echelle_start_time%60);
    return y
    }
    each_hour_y += 60;
    return y;
}

/*-- course --*/
function course_x(day) {
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

function course_y() {
    return date_height+date_margin_top+rooms[i].start-echelle_start_time
}

function course_y_text_module() {
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+10
}

function course_y_text_c_type() {
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+25
}

function course_y_text_tutor() {
    return date_height+date_margin_top+rooms[i].start-echelle_start_time+40
}

/***************
*Select*
 ***************/

/* Select of the template listeReserv.html, add dynamically the rooms stored in dataTest.js */
let select = document.getElementById("selectRoom");
for (var i = 0; i < rooms.length; i++) {
  var textC = rooms[i].name;
  var CreateElem = document.createElement("option");
  CreateElem.textContent = textC;
  CreateElem.value = textC;
  select.appendChild(CreateElem);
}

 /***************
*function display*
 ***************/

/* display the days */
function display_dateS(){
    d3.select(".dateS")
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
        .attr("width",date_width())
        .attr("height",date_height)
}

/* display the grid */
function display_gridS(){
    c_gridall = d3.select(".grilleS")
        .selectAll("rect_grid")
        .data(days)

    c_grid = c_gridall
        .enter()
        .append("g")
        .attr("class",getday)

    /* display the column for the five days */
    c_grid
        .append("rect")
        .attr("class","rect_grid")
        .attr("fill","none")
        .attr("stroke","green")
        .attr("stroke-width",5)
        .attr("x",days_x)
        .attr("y",days_y)
        .attr("width",days_width)
        .attr("height",days_height())
  }

/* display the schedule with the hours */
function display_echelleS(){
    c_echelle = d3.select(".echelleS")
        .selectAll("rect")
        .data(echelle)
        .enter();

    /* display the bar which contain the hour */
    c_echelle
        .append("rect")
        .attr("class","rect_echelle")
        .attr("fill","none")
        .attr("stroke","blue")
        .attr("stroke-width",2)
        .attr("x",echelle_x)
        .attr("y",echelle_y())
        .attr("width",echelle_width)
        .attr("height",echelle_height())

    /* location of the start hour */
    c_echelle
        .append("text")
        .text("")
        .attr("x",110)
        .attr("y", echelle_each_time_soixante)

    /* display the first whole hour after the start hour */
    c_echelle
        .append("text")
        .text(echelle_day_start_hour_concat())
        .attr("x",110)
        .attr("y", echelle_each_time_soixante)

    /* add each hour until the end of the day */
    for (hh = echelle_current_hour+1; hh<echelle_end_time_day_hour()+1; hh++){
        c_echelle
            .append("text")
            .text(echelle_current_hour_concat)
            .attr("x",110)
            .attr("y", echelle_each_time_soixante)
    }

}

/*
function display_reservationS(){
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

/*******
*display*
 ******/

function hideS() {
    console.log("hideS")
}

/* main for displaying all of what is need at once in other file */
function mainS() {
    display_dateS();
    display_gridS();
    display_echelleS();
    //display_reservationS();
}

d3.select("svg")
    .attr("height", 1600)
    .attr("width", 1600)
