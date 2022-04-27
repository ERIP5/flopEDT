var largeurWindow = window.innerWidth -40;
var days_width = (largeurWindow*0.9)/5


var room_width = largeurWindow - (days_width*5)

var date_width = days_width*5
var date_height = 50
var date_margtop = 20

var compt_room_height = 0
var compt_room_posy = 0
var compt_text_posy = 0
var compt_plusy = 0

var each_room_y = days_y()
var y_room_act = days_y()
var y_text_act = days_y()

var room_max_courses = []
var all_room_height = []

mini_add_button_height = 80

var res_posy = days_y()
var res_height = 150

var course = []

var couple_room_y = new Map();
var couple_textroom_y = new Map();
var rooms_height = new Map();


var date =[{}]
var plus =[{}]


/**********************
*gestion des variables*
**********************/

function days_x(day){

    return days_width*(day.num)+room_width}

function days_y(){
    return date_height+date_margtop
}


function days_height(){
    return (each_room_y - days_y())
}

function display_text(res){
    return res["name"]
}

function each_text_posy(){
        var y = y_text_act + (all_room_height[compt_text_posy]/2)
        y_text_act += all_room_height[compt_text_posy]
        compt_text_posy +=1
        return y
}
function courseT_x(course){
    for (element of days){
        if (element["ref"] ==  course["day"]){
            return days_width*element["num"]+room_width
        }
    }
}

function res_x(res){
    for (element of days){
        if (element["ref"] ==  res["day"]){
            return days_width*element["num"]+room_width
        }
    }
}

function courseT_y(course){
    var y = couple_room_y.get(course.room+course.day)
    couple_room_y.set(course.room+course.day, (y+res_height))
    return y;
}

function res_y(res)
{
    var y = couple_room_y.get(res.room+res.day)
    couple_room_y.set(res.room+res.day, (y+res_height))
    return y;
}

function res_text_roomy(course){
    var y = couple_textroom_y.get(course.room+ course.day+"room")
    couple_textroom_y.set(course.room+ course.day+"room", (y+res_height))
    return y+(res_height/4)
}

function res_text_daty(course){
    var y = couple_textroom_y.get(course.room+ course.day+"time")
    couple_textroom_y.set(course.room+ course.day+"time", (y+res_height))
    return y+(res_height/2)
}

function res_text_profy(course){
    var y = couple_textroom_y.get(course.room+ course.day+"prof")
    couple_textroom_y.set(course.room+ course.day+"prof", (y+res_height))
    return y+(res_height*0.75)
}

function res_text_x(course){
    for (day of days)
    {
        if (day.ref == course.day){
        return day.num*days_width+room_width+(days_width/2)
        }
    }
    return room_width+(days_width/2)
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

function max(){
for (room of rooms){
     var taller = 0
     for (day of days){
        if(room.courses[day.ref].length + room.booking[day.ref].length> taller){
            taller = room.courses[day.ref].length + room.booking[day.ref].length
            }
     }
    room_max_courses.push(taller)

    }
}

function get_room_height(){
        var h = all_room_height[compt_room_height]
        compt_room_height +=1
        return h
}

function cac_room_y(room){
        var y = y_room_act
        y_room_act += all_room_height[compt_room_posy]
        compt_room_posy +=1
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
    for (h of room_max_courses){
        all_room_height[cpt] = (res_height*h)+mini_add_button_height
        rooms_height.set(rooms[cpt].name,(res_height*h)+mini_add_button_height)
        cpt +=1
    }
}

function plus_x(day)
{
    return (day.num*days_width+room_width)
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
    return plus_x(day)+days_width/2
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
        .data(rooms)
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
  .attr("x",room_width)
  .attr("y",date_margtop)
  .attr("width",date_width)
  .attr("height",date_height)
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
  .attr("y",days_y)
  .attr("width",room_width)
  .attr("height",days_height())
  }

function display_each_room(){
compt_room_height = 0
compt_room_posy = 0
compt_text_posy = 0
c_room_all = d3.select(".room_lines")
  .selectAll("rect_each_room")
  .data(rooms);

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
  .attr("width",room_width)
  .attr("height",get_room_height);

c_room
  .append("text")
  .text(display_text)
  .attr("class","room_name")
  .attr("x",room_width/2)
  .attr("y", each_text_posy)
  .attr("text-anchor", "middle")


for(element of days){
c_room_gr
    .append("g")
    .attr("class", element["name"])
}
  }

function display_courses(){
c_all_courses = d3.select(".room_lines");

for(room of rooms)
{
    c_all_courses_day = c_all_courses
        .select("."+room_class(room))

            for(day of days){
            c_course_res_g = c_all_courses_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.courses[day.ref])
                .enter();


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
                .attr("height",res_height)
                .attr("fill",color_courses)

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_mod")
                .text(get_course_name)
                .attr("x", res_text_x)
                .attr("y", res_text_roomy)
                .attr("text-anchor", "middle")

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_date")
                .text(text_heure_res)
                .attr("x", res_text_x)
                .attr("y", res_text_daty)
                .attr("text-anchor", "middle")

            c_course_res
                .append("text")
                .attr("class", "display_courses_text_prof")
                .text(get_course_profg)
                .attr("x", res_text_x)
                .attr("y", res_text_profy)
                .attr("text-anchor", "middle")
        }
}
}

function display_reservation(){
c_all_reservations = d3.select(".room_lines");

for(room of rooms)
{
    c_all_reservations_day = c_all_reservations
        .select("."+room_class(room))


    for(day of days)
    {
        c_res_g = c_all_reservations_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.booking[day.ref])
                .enter();

        c_res = c_res_g
                .append("g")
                .attr("class",getreservation)

        c_res
            .append("rect")
                .attr("class","display_courses_frame")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",res_x)
                .attr("y",res_y)
                .attr("width",days_width)
                .attr("height",res_height)
                .attr("fill","none")

        }
    }
}

function display_plus(){
c_all_rooms = d3.select(".room_lines")
for (room of rooms){
    c_one_room = c_all_rooms
        .select(".Room"+room.name)
        for (day of days){
            c_plus = c_one_room
                .select("."+day.name)
                .selectAll("plus")
                .data(plus)
                .enter()
                .append("g")
                .attr("class","plus")
                .attr("id",room.name + day.ref)

            //pour afficher le bouton


            c_plus
                .append("circle")
                .attr("class","display_plus_circle")
                .attr("fill","green")
                .attr("stroke","black")
                .attr("stroke-width",1)
                .attr("cx",circle_plus_posx(day))
                .attr("cy",circle_plus_posy(room, day))
                .attr("r", mini_add_button_height/3)
                .attr("width",days_width)
                .attr("height",add_button_height(room,day))

            c_plus
                .append("rect")
                .attr("class","display_plus_circle")
                .attr("fill","white")
                .attr("x",circle_plus_posx(day) - mini_add_button_height/4)
                .attr("y",circle_plus_posy(room, day) - mini_add_button_height/12)
                .attr("width",mini_add_button_height/2)
                .attr("height",mini_add_button_height/6)

            c_plus
                .append("rect")
                .attr("class","display_plus_circle")
                .attr("fill","white")
                .attr("x",circle_plus_posx(day) - mini_add_button_height/12)
                .attr("y",circle_plus_posy(room, day) - mini_add_button_height/4)
                .attr("width",mini_add_button_height/6)
                .attr("height",mini_add_button_height/2)



            //pour afficher le cadre du bouton
            c_plus
                .append("rect")
                .attr("class","display_plus_rect")
                .attr("fill","none")
                .attr("stroke","black")
                .attr("stroke-width",2)
                .attr("x",plus_x(day))
                .attr("y",couple_room_y.get(room.name + day.ref))
                .attr("width",days_width)
                .attr("height",add_button_height(room,day))
        }

    }
}







function myFunction(el){
    console.log("test")
}

function add_listener(){
var test = document.querySelectorAll(".plus")
    //console.log(test)
for (el of test){
    el.addEventListener("click", function() {
  myFunction(el);
});
    //console.log(el)

}
}

function clean() {
    each_room_y = days_y()
    y_room_act = days_y()
    y_text_act = days_y()
    room_max_courses = []
    all_room_height = []
    compt_room_height = 0
    compt_room_posy = 0
    compt_text_posy = 0
    compt_plusy = 0
    course = []
    couple_room_y = new Map();
    couple_textroom_y = new Map();
    rooms_height = new Map();
    current_room = "all"
}


/***********
*gestion svg
***********/


function mainT() {
    clean();
    //console.log("mainT")
    //filling in the table room_max_courses which calculates, for each room, the day with the most lessons
    max();
    //function that populates the all_room_height using room_max_courses and adding the size of the plus button
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
    //add action listener for each button
    add_listener();
}

d3.select("svg")
     .attr("width", window.innerWidth -20)
     .attr("height", 2000)