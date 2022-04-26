/**********************
*Définition des variables*
**********************/

var date_height = 50
var date_margin_top = 20

var scale_width = 50
var scale_x = 100

var scale_start_time = 8*60+15//495
var scale_end_time_day = 18*60+45 //1125

var days_width = 150

/* set to 150 for no margin between the schedule and the days */
var scale_Margin_width = 150

var current_room = "414"

var roomS =[{}]
var dateS =[{}]
var scaleS =[{}]

/**********************
*gestion des variables*
**********************/

/*-- date --*/
function date_width() {
    return days_width*5
}

/*-- days --*/
function days_duration() {
    return (scale_end_time_day-scale_start_time)
}

function days_x(day) {
    return days_width*(day.num)+scale_Margin_width}

function days_y() {
    return date_height+date_margin_top
}

function days_height() {
    return days_duration()
}

function getday(day) {
    return day["name"]
}

/*-- scale --*/
function cac_scale_y() {
    return date_height+date_margin_top
}

function scale_y() {
    return cac_scale_y()
}

function scale_height() {
    return days_duration()
}

function scale_day_start_hour() {
	return Math.floor(scale_start_time/60)+1
}

var scale_current_hour = scale_day_start_hour()
function scale_current_hour_incr() {
    var h = scale_current_hour+1
    scale_current_hour += 1
    return h
}

function scale_current_hour_concat() {
    var hhh = scale_current_hour_incr()+ "h"
    return hhh
}

function scale_day_start_hour_concat() {
	return scale_day_start_hour() + "h"
}

function scale_end_time_day_hour() {
	return Math.floor(scale_end_time_day/60)
}

function scale_end_time_day_hour_concat() {
	return scale_end_time_day_hour + "h"
}

function display_scale_start_time() {
    return scale_start_time_hour_concat
}

function display_scale_end_time_day() {
    return scale_end_time_day_hour_concat()
}

each_hour_y = days_y()
function scale_each_time_soixante() {
    var y = each_hour_y;
    if (y == 70) {
        each_hour_y += ((scale_start_time+60)-scale_start_time-scale_start_time%60);
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
            return days_width*(2)+scale_Margin_width
    }

    //console.log(rooms[i].courses["w"])
    /*if (rooms[i].courses["m"] == "m"){
        return days_width*(0)+scale_Margin_width
        }
    if (rooms[i].courses["tu"] == "tu"){
        return days_width*(1)+scale_Margin_width
        }
    if (rooms[i].courses["w"] == "w"){
        return days_width*(2)+scale_Margin_width
        }
    if (rooms[i].courses["th"] == "th"){
        return days_width*(3)+scale_Margin_width
        }
    if (rooms[i].courses["f"] == "f"){
        return days_width*(4)+scale_Margin_width
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
    return date_height+date_margin_top+rooms[i].start-scale_start_time
}

function course_y_text_module() {
    return date_height+date_margin_top+rooms[i].start-scale_start_time+10
}

function course_y_text_c_type() {
    return date_height+date_margin_top+rooms[i].start-scale_start_time+25
}

function course_y_text_tutor() {
    return date_height+date_margin_top+rooms[i].start-scale_start_time+40
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
*function remove*
 ***************/

function rmv_scaleS() {
    c_scale
        .selectAll("rect")
        .data(scaleS)
        .remove()

    c_scale
        .selectAll("text")
        .remove()
}

function rmv_grileS() {
    c_gridall
        .selectAll("rect_grid")
        .data(days)
        .remove()

    c_grid
        .remove()
}

function rmv_dateS() {
    c_date
        .data(dateS)
        .remove()
}


function rmv_reservS() {
    rmv_scaleS()
    rmv_dateS()
    rmv_grileS()
}

 /***************
*function display*
 ***************/



/* display the days */
function display_dateS(){
    c_date = d3.select(".dateS")
        .selectAll("rect")
        .data(dateS)
        .enter()
        .append("rect")
        .attr("class","rect_date")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",5)
        .attr("x",scale_Margin_width)
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
function display_scaleS(){
    c_scale = d3.select(".scaleS")
        .selectAll("rect")
        .data(scaleS)
        .enter()

    /* display the bar which contain the hour */
    c_scale
        .append("rect")
        .attr("class","rect_scale")
        .attr("fill","none")
        .attr("stroke","blue")
        .attr("stroke-width",2)
        .attr("x",scale_x)
        .attr("y",scale_y())
        .attr("width",scale_width)
        .attr("height",scale_height())

    each_hour_y_safe = each_hour_y
    /* location of the start hour */
    c_scale
        .append("text")
        .text("test")
        .attr("x",110)
        .attr("y", scale_each_time_soixante())

    /* display the first whole hour after the start hour */
    c_scale
        .append("text")
        .text(scale_day_start_hour_concat())
        .attr("class","display_hour_first")
        .attr("x",110)
        .attr("y", scale_each_time_soixante())

    /* add each hour until the end of the day */
    for (hh = scale_current_hour+1; hh<scale_end_time_day_hour()+1; hh++){
        c_scale
            .append("text")
            .text(scale_current_hour_concat)
            .attr("class","display_hour")
            .attr("x",110)
            .attr("y", scale_each_time_soixante())
    }
    each_hour_y = each_hour_y_safe
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


/* main for displaying all of what is need at once in other file */
function mainS() {
    /* display the days */
    display_dateS()
    /* display the grid */
    display_gridS()
    /* display the schedule with the hours */
    display_scaleS()
    //display_reservationS();
}

d3.select("svg")
    .attr("height", 1600)
    .attr("width", 1600)

/*
c_scale = d3.select(".scaleS")
        .selectAll("rect")
        .data(scale)
        .remove()
        //exit()
        */
