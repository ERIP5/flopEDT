var largeurWindow = window.innerWidth -40;
var days_width_T = (largeurWindow*0.9)/5


var room_width_T = largeurWindow - (days_width_T*5)

var date_width_T = days_width_T*5
var date_height_T = 50
var date_margtop_T = 20

var compt_room_height_T = 0
var compt_room_posy_T = 0
var compt_text_posy_T = 0
var compt_plusy_T = 0

var nbId = 0
var nbCBcold = 1
var nbCBhot = 2

var each_room_y_T = days_y_T()
var y_room_act_T = days_y_T()
var y_text_act_T = days_y_T()

var room_max_courses_T = []
var all_room_height_T = []

var mini_add_button_height_T = 80

var res_height_T = 130

var course = []

var couple_room_y = new Map();
var couple_textroom_y = new Map();
var rooms_height = new Map();


var date =[{}]

var rooms_sort = []

var f_room_type = "all";

var room_projo = "all";

var room_computer = "all";


/**********************
*gestion des variables*
**********************/

function days_y_T(){
    return date_height_T+date_margtop_T
}


function days_height_T(){
    return (each_room_y_T - days_y_T())
}

function display_text_T(res){
    return res["name"]
}

function each_text_posy(){
        var y = y_text_act_T + (all_room_height_T[compt_text_posy_T]/2)
        y_text_act_T += all_room_height_T[compt_text_posy_T]
        compt_text_posy_T +=1
        return y
}
function courseT_x(course){
    for (element of days){
        if (element["ref"] ==  course["day"]){
            return days_width_T*element["num"]+room_width_T
        }
    }
}

function res_x_T(res){
    for (element of days){
        if (element["ref"] ==  res["day"]){
            return days_width_T*element["num"]+room_width_T
        }
    }
}

function courseT_y(course){
    var y = couple_room_y.get(course.room+course.day)
    couple_room_y.set(course.room+course.day, (y+res_height_T))
    return y;
}

function res_y_T(res)
{
    var y = couple_room_y.get(res.room+res.day)
    couple_room_y.set(res.room+res.day, (y+res_height_T))
    return y;
}

function course_text_roomy(course){
    var y = couple_textroom_y.get(course.room+ course.day+"room")
    couple_textroom_y.set(course.room+ course.day+"room", (y+res_height_T))
    return y+(res_height_T/4)
}

function res_text_titley(res){
    var y = couple_textroom_y.get(res.room+ res.day+"room")
    couple_textroom_y.set(res.room+ res.day+"room", (y+res_height_T))
    return y+(res_height_T/4)
}

function res_text_daty(res){
    var y = couple_textroom_y.get(res.room+ res.day+"time")
    couple_textroom_y.set(res.room+ res.day+"time", (y+res_height_T))
    return y+(res_height_T/2)
}

function res_text_responsibley(res){
    var y = couple_textroom_y.get(res.room+ res.day+"prof")
    couple_textroom_y.set(res.room+ res.day+"prof", (y+res_height_T))
    return y+(res_height_T*0.75)
}

function course_text_daty(course){
    var y = couple_textroom_y.get(course.room+ course.day+"time")
    couple_textroom_y.set(course.room+ course.day+"time", (y+res_height_T))
    return y+(res_height_T/2)
}

function course_text_profy(course){
    var y = couple_textroom_y.get(course.room+ course.day+"prof")
    couple_textroom_y.set(course.room+ course.day+"prof", (y+res_height_T))
    return y+(res_height_T*0.75)
}

function res_text_x(course){
    for (day of days)
    {
        if (day.ref == course.day){
        return day.num*days_width_T+room_width_T+(days_width_T/2)
        }
    }
    return room_width_T+(days_width_T/2)
}

function text_heure_res(res){
    return (get_time(res.start)+" - "+get_time(res.start+res.duration))
}

function get_time(val){
    var tostring = ""+Math.floor(val/60)+"h"+(val%60)
    return tostring
}

function getday(day){
    return day["name"]
}

function room_class(res)
{
    return 'Room' + res["name"]
}

function getcourses(course){
    return course.mod
}

function getreservation(res){
    return res.title
}


function getresponsible(res){
    return "responsible : "+res.responsible
}

function max(){
for (room of rooms_sort){
     var taller = 0
     for (day of days){
        if(room.courses[day.ref].length + room.booking[day.ref].length> taller){
            taller = room.courses[day.ref].length + room.booking[day.ref].length
            }
     }
    room_max_courses_T.push(taller)

    }
}

function get_room_height(){
        var h = all_room_height_T[compt_room_height_T]
        compt_room_height_T +=1
        return h
}

function cac_room_y(room){
        var y = y_room_act_T
        y_room_act_T += all_room_height_T[compt_room_posy_T]
        compt_room_posy_T +=1
        for (day of days){
            couple_room_y.set(room.name+ day.ref, y)
            couple_room_y.set(room.name+ day.ref+"base", y)
            couple_textroom_y.set(room.name + day.ref + "room", y)
            couple_textroom_y.set(room.name + day.ref + "time", y)
            couple_textroom_y.set(room.name + day.ref + "prof", y)
        }
        return y
}

function cac_all_height(){
var cpt = 0
    for (h of room_max_courses_T){
        all_room_height_T[cpt] = (res_height_T*h)+mini_add_button_height_T
        rooms_height.set(rooms_sort[cpt].name,(res_height_T*h)+mini_add_button_height_T)
        cpt +=1
    }
}

function plus_x(day)
{
    return (day.num*days_width_T+room_width_T)
}

function color_courses(course){
    return course.color_bg
}

function get_course_name(course){
    return (course.department+" : "+course.mod)
}

function get_course_profg(course){
    return "Tutor : "+course.tutor
}

function add_button_height(room, day){

var  height = (rooms_height.get(room.name)+ couple_room_y.get(room.name + day.ref+"base")) - couple_room_y.get(room.name + day.ref)

return height

}

function circle_plus_posy(room, day){
    return (couple_room_y.get(room.name + day.ref) + add_button_height(room,day)/2)
}

function circle_plus_posx(day){
    return plus_x(day)+days_width_T/2
}

/***************
*function remove*
 ***************/

function rmv_dateT() {
    d3.select(".dates")
        .selectAll("rect")
        .data(date)
        .remove()
}

/* doesn't work ? */
function rmv_roomT() {
    d3.select("svg")
        .select(".salles")
        .selectAll("rect_room")
        .data(room)
        .remove()
}

/* remove nearly everything */
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
    rmv_dateT()
    rmv_roomT()
    rmv_each_roomT()
}

 /*********************************
*function color per courses/booking*
 *********************************/
function colorT() {
    nbCm = rooms_sort[nbId].courses["m"].length
    nbCtu = rooms_sort[nbId].courses["tu"].length
    nbCw = rooms_sort[nbId].courses["w"].length
    nbCth = rooms_sort[nbId].courses["th"].length
    nbCf = rooms_sort[nbId].courses["f"].length
    nbCtotal = nbCm + nbCtu + nbCw + nbCth + nbCf

    nbBm = rooms_sort[nbId].booking["m"].length
    nbBtu = rooms_sort[nbId].booking["tu"].length
    nbBw = rooms_sort[nbId].booking["w"].length
    nbBth = rooms_sort[nbId].booking["th"].length
    nbBf = rooms_sort[nbId].booking["f"].length
    nbBtotal = nbBm + nbBtu + nbBw + nbBth + nbBf

    nbCBtotal = nbCtotal + nbBtotal

    if (nbCBtotal >= nbCBhot) {
        nbId += 1
        return "red"
    }
    if (nbCBtotal >= nbCBcold) {
        nbId += 1
        return "yellow"
    }
    nbId += 1
    return "green"
}



 /***************
*function display*
 ***************/

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
  .attr("stroke-width",2)
  .attr("x",room_width_T)
  .attr("y",date_margtop_T)
  .attr("width",date_width_T)
  .attr("height",date_height_T)
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
  .attr("stroke-width",2)
  .attr("x",0)
  .attr("y",days_y_T)
  .attr("width",room_width_T)
  .attr("height",days_height_T())
  }

function display_each_room(){
compt_room_height_T = 0
compt_room_posy_T = 0
compt_text_posy_T = 0
c_room_all = d3.select(".room_lines")
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
  .attr("class","block_title_frame")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",2)
  .attr("x",0)
  .attr("y", cac_room_y)
  .attr("width",room_width_T)
  .attr("height",get_room_height)

c_room
  .append("text")
  .text(display_text_T)
  .attr("class","room_name")
  .attr("fill",colorT)
  .attr("x",room_width_T/2)
  .attr("y", each_text_posy)
  .attr("text-anchor", "middle")
  .on("click",change_room)


for(element of days){
c_room_gr
    .append("g")
    .attr("class", element["name"])
}
  }

function display_courses(){
c_all_courses = d3.select(".room_lines");

for(room of rooms_sort)
{
    c_all_courses_day = c_all_courses
        .select("."+room_class(room))

            for(day of days){
            c_course_res_g = c_all_courses_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.courses[day.ref])
                .enter()
                .append("g")
                .attr("class","plus")
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
                .attr("width",days_width_T)
                .attr("height",res_height_T)
                .attr("fill",color_courses)

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_mod")
                .text(get_course_name)
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

function display_reservation(){
c_all_reservations = d3.select(".room_lines");

for(room of rooms_sort)
{
    c_all_reservations_day = c_all_reservations
        .select("."+room_class(room))


    for(day of days)
    {
        c_res_g = c_all_reservations_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.booking[day.ref])
                .enter()
                .append("g")
                .attr("class","plus")
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
                .attr("width",days_width_T)
                .attr("height",res_height_T)
                .attr("fill","grey")

        c_res
            .append("text")
            .attr("class","infos")
            .text(getreservation)
            .attr("x",res_text_x)
            .attr("y",res_text_titley)
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

function display_plus(){
c_all_rooms = d3.select(".room_lines")
for (room of rooms_sort){
    c_one_room = c_all_rooms
        .select(".Room"+room.name)
        for (day of days){
            c_plus = c_one_room
                .select("."+day.name)
                .selectAll("plus")
                .data([{"room":room,"day":day}])
                .enter()
                .append("g")
                .attr("class","plus")
                .attr("id",room.name + day.ref)
                .on("click", go_popup)

            //pour afficher le bouton
            c_plus
                .append("circle")
                .attr("class","display_plus_circle")
                .attr("fill","green")
                .attr("stroke","black")
                .attr("stroke-width",1)
                .attr("cx",circle_plus_posx(day))
                .attr("cy",circle_plus_posy(room, day))
                .attr("r", mini_add_button_height_T/3)
                .attr("width",days_width_T)
                .attr("height",add_button_height(room,day))

            c_plus
                .append("rect")
                .attr("class","display_plus_circle")
                .attr("fill","white")
                .attr("x",circle_plus_posx(day) - mini_add_button_height_T/4)
                .attr("y",circle_plus_posy(room, day) - mini_add_button_height_T/12)
                .attr("width",mini_add_button_height_T/2)
                .attr("height",mini_add_button_height_T/6)

            c_plus
                .append("rect")
                .attr("class","display_plus_circle")
                .attr("fill","white")
                .attr("x",circle_plus_posx(day) - mini_add_button_height_T/12)
                .attr("y",circle_plus_posy(room, day) - mini_add_button_height_T/4)
                .attr("width",mini_add_button_height_T/6)
                .attr("height",mini_add_button_height_T/2)



            //pour afficher le cadre du bouton
            c_plus
                .append("rect")
                .attr("class","display_plus_rect")
                .attr("fill","none")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",plus_x(day))
                .attr("y",couple_room_y.get(room.name + day.ref))
                .attr("width",days_width_T)
                .attr("height",add_button_height(room,day))
        }

    }
}



function change_room(room){
    rmv_total()
    rmvStatut = 2
    current_room = room.name
    document.getElementById("selectRoom").value = current_room
    mainS()
}

function go_popup(ele)
{
    console.log(ele.room.name + " " +ele.day.name)
}

function go_popup_course(courT)
{
    console.log(courT.room + " " + courT.day)
}

function go_popup_res(resT)
{
    console.log(resT.room + " " + resT.day)
}

function clean() {
    each_room_y_T = days_y_T()
    y_room_act_T = days_y_T()
    y_text_act_T = days_y_T()
    room_max_courses_T = []
    all_room_height_T = []
    compt_room_height_T = 0
    compt_room_posy_T = 0
    compt_text_posy_T = 0
    compt_plusy_T = 0
    nbId = 0
    course = []
    couple_room_y = new Map();
    couple_textroom_y = new Map();
    rooms_height = new Map();
    current_room = "all"
}

/*******************
*gestion des filtres
*******************/
function sortRoom()
{
rooms_sort = rooms

    rooms_sort = sortType(rooms_sort)
    rooms_sort = sortProjector(rooms_sort)
    rooms_sort = sortComputer(rooms_sort)


}

function sortType(oldList)
{
newL = []
for (room of oldList)
{
    if(f_room_type != "all"){
        if(room.type == f_room_type)
        {
            newL.push(room)
        }
    }
    else
    {
    newL = oldList
    }
}
 return newL
}

function sortProjector(oldList)
{
newL = []
for (room of oldList)
{
    if(room_projo != "all"){
        if((""+room.projector+"") == room_projo)
            {
                newL.push(room)
            }
    }
    else
    {
    newL = oldList
    }
}
 return newL
}

function sortComputer(oldList)
{
newL = []
for (room of oldList)
{
    if(room_computer != "all"){
        if((""+room.computer+"") == room_computer)
            {
                newL.push(room)
            }
    }
    else
    {
    newL = oldList
    }
}
 return newL
}
/***********
*gestion svg
***********/

function mainT() {
    clean();

    sortRoom();

    //filling in the table room_max_courses_T which calculates, for each room, the day with the most lessons
    max();
    //function that populates the all_room_height_T using room_max_courses_T and adding the size of the plus button
    cac_all_height();
    //draw the first rect with dates
    display_date();
    //display left panel with all room numbers
    display_each_room();
    //for each days and each room, add a group for each course and display each course information's
    display_courses();
    //for each days and each room, add a group for each reservation and display each reservation information's
    display_reservation();
    //for each days and each room, add all plus buttons
    display_plus();
    d3.select("svg")
     .attr("width", window.innerWidth -20)
     .attr("height", 2000)
}
