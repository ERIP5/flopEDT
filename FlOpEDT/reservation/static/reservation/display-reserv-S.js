/**********************
*Définition des variables*
**********************/
var largeurWindowS = window.innerWidth -40;

var date_heightS = 50
var date_margin_topS = 20

var scale_width_Total = largeurWindowS - (days_width_T*5)
var scale_width = (largeurWindowS - (days_width_T*5))*0.6
var scale_margin = (largeurWindowS - (days_width_T*5))*0.4

var scale_x = 100

var scale_start_time = 8*60+15//480
var scale_end_time_day = 18*60+45 //1125

var days_widthS = (largeurWindow*0.9)/5



var roomS =[{}]
var dateS =[{}]
var scaleS =[{}]

/**********************
*gestion des variables*
**********************/

/*-- date --*/
function date_widthS() {
    return days_widthS*5
}

/*-- days --*/
function days_durationS() {
    return (scale_end_time_day-scale_start_time)
}

function days_xS(day) {
    return days_widthS*(day.num)+scale_width_Total}

function days_yS() {
    return date_heightS+date_margin_topS
}

function days_heightS() {
    return days_durationS()
}

function getdayS(day) {
    return day["name"]
}

/*-- scale --*/
function cac_scale_y() {
    return date_heightS+date_margin_topS
}

function scale_y() {
    return cac_scale_y()
}

function scale_height() {
    return days_durationS()
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

each_hour_yS = days_yS()
function scale_each_time_soixante() {
    var y = each_hour_yS;
    if (y == 70) {
        each_hour_yS += ((scale_start_time+60)-scale_start_time-scale_start_time%60);
        return y
    }
    each_hour_yS += 60;
    return y;
}

/*-- course --*/
function course_xS(course){
    for (element of days){
        if (element["ref"] ==  course["day"]){
            return days_widthS*element["num"]+ scale_width_Total
        }
    }
}

    //console.log(rooms[i].courses["w"])
    /*if (rooms[i].courses["m"] == "m"){
        return days_widthS*(0)+scale_Margin_width
        }
    if (rooms[i].courses["tu"] == "tu"){
        return days_widthS*(1)+scale_Margin_width
        }
    if (rooms[i].courses["w"] == "w"){
        return days_widthS*(2)+scale_Margin_width
        }
    if (rooms[i].courses["th"] == "th"){
        return days_widthS*(3)+scale_Margin_width
        }
    if (rooms[i].courses["f"] == "f"){
        return days_widthS*(4)+scale_Margin_width
        }*/

    /*
        if (day.ref == course[day.ref]){
        console.log(2)
        console.log(days_widthS*element["num"]+room_widthS)
            return days_widthS*element["num"]+room_widthS
        }
    */


function course_yS(course) {
   return course.start+date_margin_topS+date_heightS-scale_start_time
}

function course_heightS(course) {
   return course.duration
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

function getCourseName_S(course)
{
    return course.mod
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
    c_gridallS
        .selectAll("rect_grid")
        .data(days)
        .remove()

    c_gridS
        .remove()
}

function rmv_dateS() {
    c_dateS
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
    c_dateS = d3.select(".dateS")
        .selectAll("rect")
        .data(dateS)
        .enter()
        .append("rect")
        .attr("class","rect_date")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",scale_width_Total)
        .attr("y",date_margin_topS)
        .attr("width",date_widthS())
        .attr("height",date_heightS)
}

/* display the grid */
function display_gridS(){
    c_gridallS = d3.select(".grilleS")
        .selectAll("rect_grid")
        .data(days)

    c_gridS = c_gridallS
        .enter()
        .append("g")
        .attr("class",getdayS)

    /* display the column for the five days */
    c_gridS
        .append("rect")
        .attr("class","rect_grid")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",days_xS)
        .attr("y",days_yS)
        .attr("width",days_widthS)
        .attr("height",days_heightS())
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
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",scale_margin)
        .attr("y",scale_y())
        .attr("width",scale_width)
        .attr("height",scale_height())

    each_hour_yS_safe = each_hour_yS
    scale_current_hour_safe = scale_current_hour
    /* location of the start hour */
    c_scale
        .append("text")
        .text("")
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
    each_hour_yS = each_hour_yS_safe
    scale_current_hour = scale_current_hour_safe
}


function display_reservationS(){

    c_courses_day = d3.select(".grilleS");
    for(room of rooms){
        if(room.name == current_room)
            {
                for (day of days){
                    c_course = c_courses_day
                        .select("."+day.name)
                        .selectAll("course")
                        .data(room.courses[day.ref])
                        .enter()
                        .append("g")
                        .attr("class",getCourseName_S)

                    c_course
                        .append("rect")
                        .attr("class","course")
                        .attr("stroke","black")
                        .attr("stroke-width",2)
                        .attr("x",course_xS)
                        .attr("y",course_yS)
                        .attr("width",days_widthS)
                        .attr("height",course_heightS)
                        .attr("fill",color_courses)
                }
            }

    }

}


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
    display_reservationS();
}

d3.select("svg")
    .attr("height", 1600)
    .attr("width", 1600)
