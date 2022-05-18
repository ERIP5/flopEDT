/**********************
    *Initialisation*
**********************/

var window_widthS = window.innerWidth -40;

// width of a day
var days_widthS = (window_widthS*0.9)/5

//-- date --//
// height of the date rectangle
var date_heightS = 50
// margin of the date from the top
var date_margin_topS = 20

//-- scale --//
var scale_width_Total = window_widthS - (days_width_T*5)
var scale_width = (window_widthS - (days_width_T*5))*0.6
var scale_margin = (window_widthS - (days_width_T*5))*0.4
var scale_x = 100

// start of the day in minutes
var scale_start_time = 8*60//480
// end of the day in minutes
var scale_end_time_day = 18*60+45 //1125

//-- add --//
var addS_val = 80

//-- color per courses/booking --//
// the number of course/booking is still acceptable
var nbCBcoldS = 3
// there is too much course/booking
var nbCBhotS = 4


// variable or cpt not defined reset in cleanS
each_hour_yS = days_y_T()
var scale_current_hour = scale_day_start_hour()
var planB1 = 0
var nbIdS_test = 0
var nbSday = 1
var captNb = 0

var dateS =[{}]
var scaleS =[{}]

/**********************
*variable's management*
**********************/

//-- date --//
function date_widthS() {
    return days_widthS*5
}

//-- days --//
function days_durationS() {
    return (scale_end_time_day-scale_start_time)
}

function days_xS(day) {
    return days_widthS*(day.num)+scale_width_Total
}

function days_heightS() {
    return days_durationS()
}

//-- scale --//
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

function scale_each_time_sixty() {
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

//-- course --//
function course_xS(course) {
    for (element of days) {
        if (element["ref"] ==  course["day"]) {
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

//-- add --//
function addS_x(day) {
    return days_widthS*(day.num)+scale_width_Total
}

function addS_y() {
    return days_y_T() + days_heightS()
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

function popform(day) {
    console.log(current_room + " " +day.name)
}

function double_popform_course(cours) {
    console.log(current_room + " " + cours.day)
}

function double_popform_res(res) {
    console.log(current_room + " " + res.day)
}

/***************
     *Text*
 ***************/

function get_courseS_name(course) {
    return (course.department+ " : "+ course.mod)
}

function get_courseS_hour(course) {
    return (get_time(course.start)+" - "+get_time(course.start+course.duration))
}

function get_courseS_tutor(course) {
    return "Tutor : "+course.tutor
}

function res_textS_x(course) {
    for (day of days)
    {
        if (day.ref == course.day) {
        return day.num*days_width_T+room_width_T+(days_width_T/2)
        }
    }
    return room_width_T+(days_width_T/2)
}

function res_textS_y(course) {
    return course_yS(course)+course.duration/4
}

function res_textS_hour_y(course) {
    return course_yS(course)+course.duration/2
}

function res_textS_tutor_y(course) {
    return course_yS(course)+course.duration*0.75
}

/*********************************
*function color per courses/booking*
 *********************************/
function colorS_choiceRoom() {
    for (nbIdS_test; nbIdS_test < allRoom.length; nbIdS_test++) {
        if (allRoom[nbIdS_test].name == current_room) {
            nbIdS = nbIdS_test
            return nbIdS
        }
    }
}

function colorS() {
    if (nbSday == 1) {
        nbCS = allRoom[colorS_choiceRoom()].courses["m"].length
        nbBS = allRoom[colorS_choiceRoom()].booking["m"].length

        nbCBtotalS = nbCS + nbBS

        nbSday = 2

        if (nbCBtotalS >= nbCBhotS) {
            return "red"
        }
        if (nbCBtotalS >= nbCBcoldS) {
            return "yellow"
        }
        return "green"
    }

    if (nbSday == 2) {
        nbCS = allRoom[colorS_choiceRoom()].courses["tu"].length
        nbBS = allRoom[colorS_choiceRoom()].booking["tu"].length

        nbCBtotalS = nbCS + nbBS

        nbSday = 3

        if (nbCBtotalS >= nbCBhotS) {
            return "red"
        }
        if (nbCBtotalS >= nbCBcoldS) {
            return "yellow"
        }
        return "green"
    }

    if (nbSday == 3) {
        nbCS = allRoom[colorS_choiceRoom()].courses["w"].length
        nbBS = allRoom[colorS_choiceRoom()].booking["w"].length

        nbCBtotalS = nbCS + nbBS

        nbSday = 4

        if (nbCBtotalS >= nbCBhotS) {
            return "red"
        }
        if (nbCBtotalS >= nbCBcoldS) {
            return "yellow"
        }
        return "green"
    }

    if (nbSday == 4) {
        nbCS = allRoom[colorS_choiceRoom()].courses["th"].length
        nbBS = allRoom[colorS_choiceRoom()].booking["th"].length

        nbCBtotalS = nbCS + nbBS

        nbSday = 5

        if (nbCBtotalS >= nbCBhotS) {
            return "red"
        }
        if (nbCBtotalS >= nbCBcoldS) {
            return "yellow"
        }
        return "green"
    }

    if (nbSday == 5) {
        nbCS = allRoom[colorS_choiceRoom()].courses["f"].length
        nbBS = allRoom[colorS_choiceRoom()].booking["f"].length

        nbCBtotalS = nbCS + nbBS

        nbSday = 1

        if (nbCBtotalS >= nbCBhotS) {
            return "red"
        }
        if (nbCBtotalS >= nbCBcoldS) {
            return "yellow"
        }
        return "green"
    }
}

/*
//same function as reservS
function colorS_resType(course) {
    if (course.type == "type") {
        return "green"
    }
    if (course.type == "partiel") {
        return "red"
    }
    return "grey"
}
*/
function colorS_resType(course) {
    return course.color_bg
}

/***************
*function caption*
 ***************/

function captionS_x() {
    return scale_margin
}

function captionS_y() {
    captNb +=1
    return days_heightS() + 200 + (100*captNb)
}

function captionS_xText() {
    return captionS_x() + days_widthS/2
}

function captionS_yText() {
    captNb -=1
    return captionS_y() + 50
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

function rmv_captS() {
    c_capt
        .selectAll("rect")
        .remove()

    c_capt
        .selectAll("text")
        .remove()
}

function cleanS() {
    each_hour_yS = days_y_T()
    scale_current_hour = scale_day_start_hour()
    planB1 = 0
    nbIdS_test = 0
    nbSday = 1
    captNb = 0
}

function rmv_reservS() {
    cleanS()
    rmv_scaleS()
    rmv_dateS()
    rmv_grileS()
    rmv_addS()
    rmv_captS()
    }

 /***************
*function display*
 ***************/

// display the days
function display_dateS() {
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

// display the grid
function display_gridS() {
    c_gridallS = d3.select(".grilleS")
        .selectAll("rect_grid")
        .data(days)

    c_gridS = c_gridallS
        .enter()
        .append("g")
        .attr("class",getday)

    // display the column for the five days
    c_gridS
        .append("rect")
        .attr("class","rect_grid")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",days_xS)
        .attr("y",days_y_T)
        .attr("width",days_widthS)
        .attr("height",days_heightS())
  }

// display the schedule with the hours
function display_scaleS() {
    c_scale = d3.select(".scaleS")
        .selectAll("rect")
        .data(scaleS)
        .enter()

    // display the bar which contain the hour
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

    // location of the start hour
    c_scale
        .append("text")
        .text("")
        .attr("x",scale_textx_S)
        .attr("y", scale_each_time_sixty())
        .attr("text-anchor", "middle")

    // display the first whole hour after the start hour
    c_scale
        .append("text")
        .text(scale_day_start_hour_concat())
        .attr("class","display_hour_first")
        .attr("x",scale_textx_S)
        .attr("y", scale_each_time_sixty())
        .attr("text-anchor", "middle")

    // add each hour until the end of the day
    for (hh = scale_current_hour+1; hh<scale_end_time_day_hour()+1; hh++) {
        c_scale
            .append("text")
            .text(scale_current_hour_concat)
            .attr("class","display_hour")
            .attr("x",scale_textx_S)
            .attr("y", scale_each_time_sixty())
            .attr("text-anchor", "middle")
    }
}

// display the courses
function display_coursesS() {

    c_courses_day = d3.select(".grilleS");
    for(room of allRoom) {
        if(room.name == current_room) {
            for (day of days) {
                c_course = c_courses_day
                    .select("."+day.name)
                    .selectAll("course")
                    .data(room.courses[day.ref])
                    .enter()
                    .append("g")
                    .attr("class",get_courseS_name)
                    .on("dblclick", double_popform_course)

                // display the course rectangle
                c_course
                    .append("rect")
                    .attr("class","course")
                    .attr("stroke","black")
                    .attr("stroke-width",2)
                    .attr("x",course_xS)
                    .attr("y",course_yS)
                    .attr("width",days_widthS)
                    .attr("height",course_heightS)
                    .attr("fill",color_courses) // function in reservT

                // display the department and the courses name
                c_course
                    .append("text")
                    .text(get_courseS_name)
                    .attr("class", "course_text")
                    .attr("fill",color_text)
                    .attr("font-weight", "bold")
                    .attr("x", res_textS_x)
                    .attr("y", res_textS_y)
                    .attr("text-anchor", "middle")

                // display the start and end hour
                c_course
                    .append("text")
                    .text(get_courseS_hour)
                    .attr("class", "course_text")
                    .attr("x", res_textS_x)
                    .attr("y", res_textS_hour_y)
                    .attr("text-anchor", "middle")

                // display the tutor's name
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

// display the reservation
function display_reservationS() {
    c_reservation_day = d3.select(".grilleS");
        for(room of allRoom) {
            if(room.name == current_room) {
                for (day of days) {
                    c_reservation = c_reservation_day
                        .select("."+day.name)
                        .selectAll("booking")
                        .data(room.booking[day.ref])
                        .enter()
                        .append("g")
                        .attr("class",getreservation)
                        .on("dblclick", double_popform_res)

                    // display the reservation rectangle
                    c_reservation
                        .append("rect")
                        .attr("class","course")
                        .attr("stroke","black")
                        .attr("stroke-width",2)
                        .attr("x",course_xS)
                        .attr("y",course_yS)
                        .attr("width",days_widthS)
                        .attr("height",course_heightS)
                        //.attr("fill", colorS_resType)

                    // display the title of the reservation
                    c_reservation
                        .append("text")
                        .text(getreservation)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_y)
                        .attr("text-anchor", "middle")

                    // display the start and end hour
                    c_reservation
                        .append("text")
                        .text(get_courseS_hour)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_hour_y)
                        .attr("text-anchor", "middle")

                    // display the reservation's responsible
                    c_reservation
                        .append("text")
                        .text(getresponsible)
                        .attr("class", "course_text")
                        .attr("x", res_textS_x)
                        .attr("y", res_textS_tutor_y)
                        .attr("text-anchor", "middle")
                }
            }
        }
}

// display the add button
function display_addS() {
    c_addall = d3.select(".grilleS")
        .selectAll("rect_add")
        .data(days)
        .enter()
        .append("g")
        .attr("class","add")
        .on("click", popform)

    // display the circle
    c_add = c_addall
        .data(days)
        .append("circle")
        .attr("class","circle_add")
        .attr("fill",colorS)
        .attr("stroke","black")
        .attr("stroke-width",3)
        .attr("cx",addS_circle_cx)
        .attr("cy",addS_circle_cy)
        .attr("r", addS_val*0.66)

    // display the horizontal rectangle
    c_add_rect_horizontal = c_addall
        .append("rect")
        .attr("class", "circle_add")
        .attr("fill", "white")
        .attr("x",addS_circle_cx)
        .attr("y",addS_circle_cy() - addS_val/2.5)
        .attr("width",addS_val - addS_val/1.5)
        .attr("height",addS_val - addS_val/6)

    // display the vertical rectangle
    c_add_rect_vertical = c_addall
        .append("rect")
        .attr("class", "circle_add")
        .attr("fill", "white")
        .attr("x",addS_circle_cx)
        .attr("y",addS_circle_cy() - addS_val/6)
        .attr("width",addS_val - addS_val/6)
        .attr("height",addS_val - addS_val/1.5)

    // display the rectangle which contain the button
    c_add_frame = c_addall
        .append("rect")
        .attr("class","circle_add")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",addS_x)
        .attr("y",addS_y)
        .attr("width",addS_width)
        .attr("height",addS_height)
}

// display the caption for the booking
function display_captionS() {
    c_capt = d3.select(".captionS")
        .selectAll("rect")
        .data(dateS)
        .enter()

    c_capt
        .append("rect")
        .attr("class","rect_caption")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",captionS_x)
        .attr("y",captionS_y)
        .attr("width",days_widthS)
        .attr("height",100)

    c_capt
        .append("text")
        .text("Caption's booking :")
        .attr("class", "capt_text")
        .attr("x", captionS_xText)
        .attr("y", captionS_yText)
        .attr("text-anchor", "middle")
        .style("font-size", "25px")

    c_capt
        .append("rect")
        .attr("class","rect_caption")
        .attr("fill","#99cccc")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",captionS_x)
        .attr("y",captionS_y)
        .attr("width",days_widthS)
        .attr("height",100)

    c_capt
        .append("text")
        .text("Réunion")
        .attr("class", "capt_text")
        .attr("x", captionS_xText)
        .attr("y", captionS_yText)
        .attr("text-anchor", "middle")
        .style("font-size", "25px")

    c_capt
        .append("rect")
        .attr("class","rect_caption")
        .attr("fill","#95a5a6")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",captionS_x)
        .attr("y",captionS_y)
        .attr("width",days_widthS)
        .attr("height",100)

    c_capt
        .append("text")
        .text("Partiel")
        .attr("class", "capt_text")
        .attr("x", captionS_xText)
        .attr("y", captionS_yText)
        .attr("text-anchor", "middle")
        .style("font-size", "25px")
}

/*******
*display*
 ******/

// main for displaying all of what is need at once in other file
function mainS() {

    // display the days
    display_dateS()
    // display the grid
    display_gridS()
    // display the schedule with the hours
    display_scaleS()
    // display the courses
    display_coursesS()
    // display the booking
    display_reservationS()
    // display the add
    display_addS()
    // display the caption for the booking
    display_captionS()

    d3.select("svg")
    .attr("height", 1600)
    .attr("width", 1600)
}
