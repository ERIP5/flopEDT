/**********************
*Définition des variables*
**********************/
var largeurWindowS = window.innerWidth -40;

var days_widthS = (largeurWindow*0.9)/5

var date_heightS = 50
var date_margin_topS = 20

var scale_width_Total = largeurWindowS - (days_width_T*5)
var scale_width = (largeurWindowS - (days_width_T*5))*0.6
var scale_margin = (largeurWindowS - (days_width_T*5))*0.4
var scale_x = 100

var scale_start_time = 8*60+15//480
var scale_end_time_day = 18*60+45 //1125

var addS_val = 80


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
    return days_widthS*(day.num)+scale_width_Total
}

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

function scale_textx_S()
{
    return scale_margin+ (scale_width/2)
}

/*-- course --*/
function course_xS(course){
    for (element of days){
        if (element["ref"] ==  course["day"]){
            return days_widthS*element["num"]+ scale_width_Total
        }
    }
}


function course_yS(course) {
   return course.start+date_margin_topS+date_heightS-scale_start_time
}

function course_heightS(course) {
   return course.duration
}

/*-- add --*/
function addS_x(day) {
    return days_widthS*(day.num)+scale_width_Total
}

function addS_y() {
    return days_yS() + days_heightS()
}

function addS_width() {
    return days_widthS
}

function addS_height() {
    return 130
}

function addS_circle_cx(day) {
    if (planB1 < 5) {
        planB1 += 1
        return addS_x(day) + (addS_width()/2)
    }
    if (planB1 < 10) {
        planB1 += 1
        return addS_x(day) + (addS_width()/2) - 12
    }

    if (planB1 < 15) {
        planB1 += 1
        return addS_x(day) + (addS_width()/2) -31
    }
}

function addS_circle_cy() {
    return addS_y() + (addS_height()/2)
}

function popform() {
    console.log("please")
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
*Text*
 ***************/

function get_courseS_name(course){
    return course.mod
}

function get_courseS_title(res){
    return res.title
}

function get_courseS_name(course){
    return (course.department+ " : "+ course.mod)
}

function get_courseS_hour(course){
    return (get_time(course.start)+" - "+get_time(course.start+course.duration))
}

function get_timeS(val){
    var tostring = Math.floor(val/60)+"h"+(val%60)
    return tostring
}

function get_courseS_tutor(course){
    return "Tutor : "+course.tutor
}

function get_courseS_responsible(course){
    return "responsible : "+course.responsible
}

function res_textS_x(course){
    for (day of days)
    {
        if (day.ref == course.day){
        return day.num*days_width_T+room_width_T+(days_width_T/2)
        }
    }
    return room_width_T+(days_width_T/2)
}

function res_textS_y(course){
    return course_yS(course)+course.duration/4
}

function res_textS_hour_y(course){
    return course_yS(course)+course.duration/2
}

function res_textS_tutor_y(course){
    return course_yS(course)+course.duration*0.75
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

function rmv_addS() {
    c_addall
        .data("rect_add")
        .remove()
}

function rmv_reservS() {
    rmv_scaleS()
    rmv_dateS()
    rmv_grileS()
    rmv_addS()
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
        .attr("x",scale_textx_S)
        .attr("y", scale_each_time_soixante())
        .attr("text-anchor", "middle")

    /* display the first whole hour after the start hour */
    c_scale
        .append("text")
        .text(scale_day_start_hour_concat())
        .attr("class","display_hour_first")
        .attr("x",scale_textx_S)
        .attr("y", scale_each_time_soixante())
        .attr("text-anchor", "middle")

    /* add each hour until the end of the day */
    for (hh = scale_current_hour+1; hh<scale_end_time_day_hour()+1; hh++){
        c_scale
            .append("text")
            .text(scale_current_hour_concat)
            .attr("class","display_hour")
            .attr("x",scale_textx_S)
            .attr("y", scale_each_time_soixante())
            .attr("text-anchor", "middle")
    }
    each_hour_yS = each_hour_yS_safe
    scale_current_hour = scale_current_hour_safe
}

/* display the courses */
function display_coursesS(){

    c_courses_day = d3.select(".grilleS");
    for(room of rooms){
        if(room.name == current_room){
            for (day of days){
                c_course = c_courses_day
                    .select("."+day.name)
                    .selectAll("course")
                    .data(room.courses[day.ref])
                    .enter()
                    .append("g")
                    .attr("class",get_courseS_name)

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

                c_course
                    .append("text")
                    .text(get_courseS_name)
                    .attr("class", "course_text")
                    .attr("x", res_textS_x)
                    .attr("y", res_textS_y)
                    .attr("text-anchor", "middle")

                c_course
                    .append("text")
                    .text(get_courseS_hour)
                    .attr("class", "course_text")
                    .attr("x", res_textS_x)
                    .attr("y", res_textS_hour_y)
                    .attr("text-anchor", "middle")

                c_course
                    .append("text")
                    .text(get_courseS_tutor)
                    .attr("class", "course_text")
                    .attr("x", res_textS_x)
                    .attr("y", res_textS_tutor_y)
                    .attr("text-anchor", "middle")
            }
        }
    }
}

/* display the reservation */
function display_reservationS() {
    c_reservation_day = d3.select(".grilleS");
        for(room of rooms){
            if(room.name == current_room){
                for (day of days){
                    c_reservation = c_reservation_day
                        .select("."+day.name)
                        .selectAll("booking")
                        .data(room.booking[day.ref])
                        .enter()
                        .append("g")
                        .attr("class",get_courseS_title)

                    c_reservation
                        .append("rect")
                        .attr("class","course")
                        .attr("stroke","black")
                        .attr("stroke-width",2)
                        .attr("x",course_xS)
                        .attr("y",course_yS)
                        .attr("width",days_widthS)
                        .attr("height",course_heightS)
                        .attr("fill", "grey")

                    c_reservation
                        .append("text")
                        .text(get_courseS_title)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_y)
                        .attr("text-anchor", "middle")

                    c_reservation
                        .append("text")
                        .text(get_courseS_hour)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_hour_y)
                        .attr("text-anchor", "middle")

                    c_reservation
                        .append("text")
                        .text(get_courseS_responsible)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_tutor_y)
                        .attr("text-anchor", "middle")
                }
            }
        }
}

/* display the add button */
function display_addS() {
    c_addall = d3.select(".grilleS")
        .selectAll("rect_add")
        .data(days)
        .enter()
        .append("g")
        .attr("class","add")
        .on("click", popform)

    planB1 = 0
    planB1safe = planB1
    /* display the button */
    c_add = c_addall
        .append("circle")
        .attr("class","circle_add")
        .attr("fill","green")
        .attr("stroke","black")
        .attr("stroke-width",3)
        .attr("cx",addS_circle_cx)
        .attr("cy",addS_circle_cy)
        .attr("r", addS_val*0.66)

    /* display the vertical rectangle */
    c_add_rect_horizontal = c_addall
        .append("rect")
        .attr("class", "circle_add")
        .attr("fill", "white")
        //.attr("x",addS_circle_cx() - addS_val/4)
        .attr("x",addS_circle_cx)
        .attr("y",addS_circle_cy() - addS_val/2.5)
        .attr("width",addS_val - addS_val/1.5)
        .attr("height",addS_val - addS_val/6)

    /* display the horizontal rectangle */
    c_add_rect_vertical = c_addall
        .append("rect")
        .attr("class", "circle_add")
        .attr("fill", "white")
        .attr("x",addS_circle_cx)
        .attr("y",addS_circle_cy() - addS_val/6)
        .attr("width",addS_val - addS_val/6)
        .attr("height",addS_val - addS_val/1.5)
    planB1 = planB1safe


    /* display the add frame for the five days */
    c_add_frame = c_addall
        .append("rect")
        .attr("class","rect_add")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",addS_x)
        .attr("y",addS_y)
        .attr("width",addS_width)
        .attr("height",addS_height)
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
    /* display the courses */
    display_coursesS()
    /* display the booking */
    display_reservationS()
    /* display the add */
    display_addS()
}

d3.select("svg")
    .attr("height", 1600)
    .attr("width", 1600)
