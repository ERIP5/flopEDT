/**********************
    *Initialisation*
**********************/

var window_width = window.innerWidth - 40;
var date_width = window_width * 0.9
var days_width = date_width / days.length
var room_width = window_width - date_width

var date_height = 50
var date_margtop = 20

var mini_add_button_height_T = 40

var res_height_T = 70

var rooms_sort = []

var filter_list = {}

// variable or cpt not defined reset in cleanT
var y_room_act_T = days_y_T()
var y_text_act_T = days_y_T()
var each_room_y_T = days_y_T()
var room_max_courses_T = []
var all_room_height_T = []
var compt_room_height_T = 0
var compt_room_posy_T = 0
var compt_text_posy_T = 0
var compt_plusy_T = 0
var nbIdT = 0
var course = []
var couple_room_y = new Map();
var couple_textroom_y = new Map();
var rooms_height = new Map();
var current_room = "all"

/**********************
*variable's management*
**********************/

// use in reserv_S
function days_y_T() {
    return date_height+date_margtop
}


function days_height_T() {
    return (each_room_y_T - days_y_T())
}

function display_text_T(res) {
    return res["name"]
}

function each_text_posy() {
        var y = y_text_act_T + (all_room_height_T[compt_text_posy_T]/2)
        y_text_act_T += all_room_height_T[compt_text_posy_T]
        compt_text_posy_T +=1
        return y
}

function courseT_x(course) {
    for (element of days) {
        if (element["ref"] ==  course["day"]) {
            return days_width*element["num"]+room_width
        }
    }
}

function res_x_T(res) {
    for (element of days) {
        if (element["ref"] ==  res["day"]) {
            return days_width*element["num"]+room_width
        }
    }
}

function courseT_y(course) {
    var y = couple_room_y.get(course.room+course.day)
    couple_room_y.set(course.room+course.day, (y+res_height_T))
    return y;
}

function res_y_T(res) {
    var y = couple_room_y.get(res.room+res.day)
    couple_room_y.set(res.room+res.day, (y+res_height_T))
    return y;
}

function course_text_roomy(course) {
    var y = couple_textroom_y.get(course.room+ course.day+"room")
    couple_textroom_y.set(course.room+ course.day+"room", (y+res_height_T))
    return y+(res_height_T/4)
}

function res_text_titley(res) {
    var y = couple_textroom_y.get(res.room+ res.day+"room")
    couple_textroom_y.set(res.room+ res.day+"room", (y+res_height_T))
    return y+(res_height_T/4)
}

function res_text_daty(res) {
    var y = couple_textroom_y.get(res.room+ res.day+"time")
    couple_textroom_y.set(res.room+ res.day+"time", (y+res_height_T))
    return y+(res_height_T/2)
}

function res_text_responsibley(res) {
    var y = couple_textroom_y.get(res.room+ res.day+"prof")
    couple_textroom_y.set(res.room+ res.day+"prof", (y+res_height_T))
    return y+(res_height_T*0.75)
}

function course_text_daty(course) {
    var y = couple_textroom_y.get(course.room+ course.day+"time")
    couple_textroom_y.set(course.room+ course.day+"time", (y+res_height_T))
    return y+(res_height_T/2)
}

function course_text_profy(course) {
    var y = couple_textroom_y.get(course.room+ course.day+"prof")
    couple_textroom_y.set(course.room+ course.day+"prof", (y+res_height_T))
    return y+(res_height_T*0.75)
}

function res_text_x(course) {
    for (day of days) {
        if (day.ref == course.day) {
            return day.num*days_width+room_width+(days_width/2)
        }
    }
    return room_width+(days_width/2)
}

function text_heure_res(res) {
    return (get_time(res.start)+ " - "+ get_time(res.start+res.duration))
}

// use in reserv_S
function get_time(val) {
    if (val%60 ==0) {
        var tostring = ""+Math.floor(val/60)+"h00"
        return tostring
    }
    var tostring = ""+Math.floor(val/60)+"h"+(val%60)
    return tostring
}

// use in reserv_S
function getday(day) {
    return day["name"]
}

function room_class(res) {
    return 'Room' + res["name"]
}

function getcourses(course) {
    return course.mod
}

//use in reserv_S
function getreservation(res) {
    return res.title
}

// use in resrv_S
function getresponsible(res) {
    return "responsible : "+res.responsible
}

function max() {
    for (room of rooms_sort) {
        var taller = 0
        for (day of days) {
            if(room.courses[day.ref].length + room.booking[day.ref].length> taller) {
                taller = room.courses[day.ref].length + room.booking[day.ref].length
            }
        }
        room_max_courses_T.push(taller)
    }
}

function get_room_height() {
    var h = all_room_height_T[compt_room_height_T]
    compt_room_height_T +=1
    return h
}

function cac_room_y(room) {
    var y = y_room_act_T
    y_room_act_T += all_room_height_T[compt_room_posy_T]
    compt_room_posy_T +=1
    for (day of days) {
        couple_room_y.set(room.name+ day.ref, y)
        couple_room_y.set(room.name+ day.ref+"base", y)
        couple_textroom_y.set(room.name + day.ref + "room", y)
        couple_textroom_y.set(room.name + day.ref + "time", y)
        couple_textroom_y.set(room.name + day.ref + "prof", y)
    }
    return y
}

function cac_all_height() {
    var cpt = 0
        for (h of room_max_courses_T) {
            if(is_tutor){
                all_room_height_T[cpt] = (res_height_T*h)+mini_add_button_height_T
                rooms_height.set(rooms_sort[cpt].name,(res_height_T*h)+mini_add_button_height_T)
            }else{
                if(h == 0){
                    all_room_height_T[cpt] = mini_add_button_height_T
                rooms_height.set(rooms_sort[cpt].name,mini_add_button_height_T)
                }else{
                all_room_height_T[cpt] = (res_height_T*h)
                rooms_height.set(rooms_sort[cpt].name,(res_height_T*h))
                }
            }
            cpt +=1
        }
}

function day_x(day) {
    return (day.num*days_width+room_width)
}

function color_courses() {
    return "#4169e1"
}

function get_course_name(course) {
    return (course.department+ " : "+ course.mod)
}

function get_course_profg(course) {
    return "Tutor : "+course.tutor
}

function add_button_height(room, day) {

var  height = (rooms_height.get(room.name)+ couple_room_y.get(room.name + day.ref+"base")) - couple_room_y.get(room.name + day.ref)

return height

}

function circle_add_posy(room, day) {
    return (couple_room_y.get(room.name + day.ref) + add_button_height(room,day)/2)
}

function centered_x(day) {
    return day_x(day)+days_width/2
}

/*******************
*filter management*
*******************/
function sortRoom() {
    rooms_sort = []

    if (Object.keys(filter_list).length == 0){
        rooms_sort = Object.values(allRoom)
    }else{
        for (room of Object.values(allRoom)){
            var toadd = true
            for (filter in filter_list){
                if ((typeof filter_list[filter]) == "object"){
                    for (value in filter_list[filter]){
                        if (value == "min" && Number(room.attributes[filter]) < filter_list[filter][value] && filter_list[filter][value] != ""){
                            toadd = false
                        }else if (value == "max" && Number(room.attributes[filter]) > filter_list[filter][value] && filter_list[filter][value] != ""){
                            toadd = false
                        }
                    }
                }else{
                    if((room.attributes[filter] != filter_list[filter]) && (filter_list[filter] !="all")){
                                toadd = false
                        }
                    }
                }
            if (toadd){
                rooms_sort.push(room)
            }
        }
    }


}

/***********
 *form*
***********/

function go_popup(ele) {
    window.location.href = "http://localhost:8000/fr/reservation/INFO/addRes"
}

function go_popup_course(courT) {
    console.log(courT.room + " " + courT.day)
}

function go_popup_res(resT) {
    console.log(resT.responsible + resT.type + resT.title + resT.description + resT.key + resT.id_booking + resT.start + resT.duration + resT.room)
}

/*********************************
*function color per courses/booking*
 *********************************/

function colorT() {
    return "green"
}

/*
function colorT_resType(course) {
    if (course.type == "type") {
        return "blue"
    }
    if (course.type == "partiel") {
        return "red"
    }

    return "grey"
}*/

function colorT_resType(course) {
    return course.color_bg
}

function color_text(course) {
    return "black"
}

/***************
*function remove*
 ***************/

function rmv_date() {
    svg.get_dom("dates")
        .selectAll(".date_text")
        .data(days)
        .remove()
}

function rmv_grille() {
    svg.get_dom("grille")
        .selectAll("rect")
        .data(days)
        .remove()
}

function rmv_roomT() {
    svg.get_dom("svg")
        .select(".salles")
        .selectAll("rect_room")
        .data(room)
        .remove()
}

function rmv_each_roomT() {
    c_room_all
        .selectAll("rect_each_room")
        .data(rooms_sort)
        .remove()
    c_room_gr
        .remove()

    c_room
        .remove()
}

function rmv_reservT() {
    rmv_date()
    rmv_roomT()
    rmv_each_roomT()
    rmv_grille()
}

function change_room(room) {
    hidefilters()
    rmv_total()
    rmvStatut = 2
    current_room = room.name
    document.getElementById("selectRoom").value = current_room
    mainS()
}

function clean() {
    y_room_act_T = days_y_T()
    y_text_act_T = days_y_T()
    each_room_y_T = days_y_T()
    room_max_courses_T = []
    all_room_height_T = []
    compt_room_height_T = 0
    compt_room_posy_T = 0
    compt_text_posy_T = 0
    compt_plusy_T = 0
    nbIdT = 0
    course = []
    couple_room_y = new Map();
    couple_textroom_y = new Map();
    rooms_height = new Map();
    current_room = "all"
}

 /***************
*function display*
 ***************/

function display_dates() {
    svg.get_dom("dates")
        .selectAll(".date_text")
        .data(days)
        .enter()
        .append("text")
        .attr("class","date_text")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",1)
        .attr("x",centered_x)
        .attr("y",date_margtop + date_height/2)
        .attr("width",days_width)
        .attr("height",date_height)
        .text(display_day_text)

}

function display_day_text(day){
    return day.name + '. '+ day.date
}

function display_room() {
    svg.get_dom("salles")
        .selectAll("rect_room")
        .data(room)
        .enter()
        .append("rect")
        .attr("class","rect_room")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",0)
        .attr("y",days_y_T)
        .attr("width",room_width)
        .attr("height",days_height_T())
}

function display_each_room() {
    c_room_all = svg.get_dom("room_lines")
        .selectAll("rect_each_room")
        .data(rooms_sort);

    c_room_gr = c_room_all
        .enter()
        .append("g")
        .attr("class", room_class)

    c_room = c_room_gr
        .append("g")
        .attr("class", "block_title")

    c_room
        .append("rect")
        .attr("class","room_frame_all")
        .attr("fill","none")
        .attr("stroke","black")
        .attr("stroke-width",2)
        .attr("x",0)
        .attr("y", cac_room_y)
        .attr("width",window_width)
        .attr("height",get_room_height)

    c_room
        .append("text")
        .text(display_text_T)
        .attr("class","room_name")
        .style("font-size", "25px")
        .attr("fill",colorT)
        .attr("x",room_width/2)
        .attr("y", each_text_posy)
        .attr("text-anchor", "middle")
        .on("click",change_room)

    for(element of days) {
        c_room_gr
            .append("g")
            .attr("class", element["name"])
    }
}

function display_courses() {
    c_all_courses = svg.get_dom("room_lines");

    for(room of rooms_sort) {
        c_all_courses_day = c_all_courses
            .select("."+room_class(room))

        for(day of days) {
            c_course_res_g = c_all_courses_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.courses[day.ref])
                .enter()
                .append("g")
                .attr("class","add")
                .attr("id",room.name + day.ref)
                .on("dblclick", go_popup_course)


            c_course_res = c_course_res_g
                .append("g")
                .attr("class",getcourses)


            c_course_res
                .append("rect")
                .attr("class","display_courses_frame")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",courseT_x)
                .attr("y",courseT_y)
                .attr("width",days_width)
                .attr("height",res_height_T)
                .attr("fill",color_courses)

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_mod")
                .text(get_course_name)
                .attr("fill",color_text)
                .attr("font-weight", "bold")
                .attr("x", res_text_x)
                .attr("y", course_text_roomy)
                .attr("text-anchor", "middle")

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_date")
                .text(text_heure_res)
                .attr("x", res_text_x)
                .attr("y", course_text_daty)
                .attr("text-anchor", "middle")

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_prof")
                .text(get_course_profg)
                .attr("x", res_text_x)
                .attr("y", course_text_profy)
                .attr("text-anchor", "middle")
        }
    }
}

function display_reservation() {
    c_all_reservations = svg.get_dom("room_lines");

    for(room of rooms_sort) {
        c_all_reservations_day = c_all_reservations
            .select("."+room_class(room))

        for(day of days) {
            c_res_g = c_all_reservations_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.booking[day.ref])
                .enter()
                .append("g")
                .attr("class","add")
                .attr("id",room.name + day.ref)
                .on("dblclick", go_popup_res)

            c_res = c_res_g
                .append("g")
                .attr("class",getreservation)

            c_res
                .append("rect")
                .attr("class","display_courses_frame")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",res_x_T)
                .attr("y",res_y_T)
                .attr("width",days_width)
                .attr("height",res_height_T)
                .attr("fill","#95a5a6")

            c_res
                .append("text")
                .attr("class","infos")
                .text(getreservation)
                .attr("x",res_text_x)
                .attr("y",res_text_titley)
                //.style("color", "color_text")
                .attr("text-anchor", "middle")

            c_res
                .append("text")
                .attr("class","infos")
                .text(text_heure_res)
                .attr("x",res_text_x)
                .attr("y",res_text_daty)
                .attr("text-anchor", "middle")

            c_res
                .append("text")
                .attr("class","infos")
                .text(getresponsible)
                .attr("x",res_text_x)
                .attr("y",res_text_responsibley)
                .attr("text-anchor", "middle")
        }
    }
}

function display_add() {
    c_all_rooms = svg.get_dom("room_lines")
    for (room of rooms_sort) {
        c_one_room = c_all_rooms
            .select(".Room"+room.name)

        for (day of days) {
            c_add = c_one_room
                .select("."+day.name)
                .selectAll("add")
                .data([{"room":room,"day":day}])
                .enter()
                .append("g")
                .attr("class","add")
                .attr("id",room.name + day.ref)
                .on("click", go_popup)

            //pour afficher le bouton
            c_add
                .append("circle")
                .attr("class","display_add_circle")
                .attr("fill","green")
                .attr("stroke","black")
                .attr("stroke-width",1)
                .attr("cx",centered_x(day))
                .attr("cy",circle_add_posy(room, day))
                .attr("r", mini_add_button_height_T/3)
                .attr("width",days_width)
                .attr("height",add_button_height(room,day))

            c_add
                .append("rect")
                .attr("class","display_add_circle")
                .attr("fill","white")
                .attr("x",centered_x(day) - mini_add_button_height_T/4)
                .attr("y",circle_add_posy(room, day) - mini_add_button_height_T/12)
                .attr("width",mini_add_button_height_T/2)
                .attr("height",mini_add_button_height_T/6)

            c_add
                .append("rect")
                .attr("class","display_add_circle")
                .attr("fill","white")
                .attr("x",centered_x(day) - mini_add_button_height_T/12)
                .attr("y",circle_add_posy(room, day) - mini_add_button_height_T/4)
                .attr("width",mini_add_button_height_T/6)
                .attr("height",mini_add_button_height_T/2)

            //pour afficher le cadre du bouton
            c_add
                .append("rect")
                .attr("class","display_add_rect")
                .attr("fill","none")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",day_x(day))
                .attr("y",couple_room_y.get(room.name + day.ref))
                .attr("width",days_width)
                .attr("height",add_button_height(room,day))
        }
    }
}

function display_grid(){
svg.get_dom("grille")
    .selectAll("rect_day")
    .data(days)
    .enter()
    .append("rect")
    .attr("class","rect_day")
    .attr("fill","none")
    .attr("stroke","black")
    .attr("stroke-width",2)
    .attr("x",day_x)
    .attr("y", date_margtop)
    .attr("width", days_width)
    .attr("height",y_room_act_T - 20)
}

/***********
 *display*
***********/

function mainT() {
    clean();
    sortRoom();
    //filling in the table room_max_courses_T which calculates, for each room, the day with the most lessons
    max();
    //function that populates the all_room_height_T using room_max_courses_T and adding the size of the add button
    cac_all_height();
    //draw the first rect with dates
    display_dates();
    //display left panel with all room numbers
    display_each_room();
    //for each days and each room, add a group for each course and display each course information's
    display_courses();
    //for each days and each room, add a group for each reservation and display each reservation information's
    display_reservation();
    //for each days and each room, add all add buttons
    if(is_tutor){
    display_add();
    }
    display_grid();

    d3.select("svg")
     .attr("width", window.innerWidth + 20)
     .attr("height", y_room_act_T)
}
