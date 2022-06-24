/**********************
    *Initialisation*
**********************/

//-- scale --//
var scale_width = room_width * 0.6
var scale_margin = room_width - scale_width
var scale_x = 100

//-- add --//
var addS_val = 80 //should be 40 but the rectangle doesn't work

//-- color per courses/booking --//
// the number of course/booking is still acceptable
var nbCBcoldS = 3
// there is too much course/booking
var nbCBhotS = 4


// variable or cpt not defined reset in cleanS
var min_start_time = 99999
var i_start_time = 0
var max_end_time = 0
var i_end_time = 0
each_hour_yS = days_y_T()
var scale_current_hour = scale_day_start_hour()
var planB1 = 0
var nbIdS_test = 0
var nbSday = 1
var captNb = 0
var scaleS =[{}]

/**********************
*variable's management*
**********************/


//-- days --//
function days_durationS() {
    return (calc_scale_end_time()-calc_scale_start_time())
}

function days_heightS() {
    return days_durationS()
}

//-- scale --//
function calc_scale_start_time() {
    for (i_start_time; i_start_time < allTimeSetting.length; i_start_time++) {
        if (min_start_time > allTimeSetting[i_start_time].day_start_time) {
            min_start_time = allTimeSetting[i_start_time].day_start_time
        }
    }
    return min_start_time
}

function calc_scale_end_time() {
    for (i_end_time; i_end_time < allTimeSetting.length; i_end_time++) {
        if (max_end_time < allTimeSetting[i_end_time].day_finish_time) {
            max_end_time = allTimeSetting[i_end_time].day_finish_time
        }
    }
    return max_end_time
}


function cac_scale_y() {
    return date_height+date_margtop
}

function scale_y() {
    return cac_scale_y()
}

function scale_height() {
    return days_durationS()
}

function scale_day_start_hour() {
	return Math.floor(calc_scale_start_time()/60)+1
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
	return Math.floor(calc_scale_end_time()/60)
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
        each_hour_yS += ((calc_scale_start_time()+60)-calc_scale_start_time()-calc_scale_start_time()%60);
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
            return days_width*element["num"]+ room_width
        }
    }
}

function course_yS(course) {
   return course.start+date_margtop+date_height-calc_scale_start_time()
}

function course_heightS(course) {
   return course.duration
}

//-- add --//
function addS_x(day) {
    return days_width*(day.num)+room_width
}

function addS_y() {
    return days_y_T() + days_heightS()
}

function addS_width() {
    return days_width
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
    window.location.href = "http://localhost:8000/fr/reservation/INFO/addRes"
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
        return day.num*days_width+room_width+(days_width/2)
        }
    }
    return room_width+(days_width/2)
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
    return captionS_x() + days_width/2
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
    min_start_time = 99999
    i_start_time = 0
    max_end_time = 0
    i_end_time = 0
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
    rmv_date()
    rmv_grileS()
    rmv_addS()
    rmv_captS()
    }

 /***************
*function display*
 ***************/

// display the grid
function display_gridS() {
    c_gridallS = svg.get_dom("grilleS")
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
        .attr("x",day_x)
        .attr("y",days_y_T)
        .attr("width",days_width)
        .attr("height",days_heightS())
  }

// display the schedule with the hours
function display_scaleS() {
    c_scale = svg.get_dom("scaleS")
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

    c_courses_day = svg.get_dom("grilleS");
    for(room of Object.values(allRoom)) {
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
                    .attr("width",days_width)
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
    c_reservation_day = svg.get_dom("grilleS");
        for(room of Object.values(allRoom)) {
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
                        .attr("width",days_width)
                        .attr("height",course_heightS)
                        //.attr("fill", colorS_resType)
                        .attr("fill", '#95a5a6')

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
    c_addall = svg.get_dom("grilleS")
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
        .attr("fill","green")
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
    c_capt = svg.get_dom("captionS")
        .selectAll("rect")
        .data(days)
        .enter()

    c_capt
        .append("rect")
        .attr("class","rect_caption")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",captionS_x)
        .attr("y",captionS_y)
        .attr("width",days_width)
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
        .attr("width",days_width)
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
        .attr("width",days_width)
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
    display_dates()
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
