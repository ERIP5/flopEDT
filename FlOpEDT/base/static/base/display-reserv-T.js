var days_width = 150
var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;


var room_width = 100

var date_width = days_width*5
var date_height = 50
var date_margtop = 20

var each_room_y = days_y()
var compt_room_height = 0
var compt_room_posy = 0
var compt_text_posy = 0
var y_room_act = days_y()
var y_text_act = days_y()
var room_max_courses = []
var all_room_height = []

var add_button_height = 50

var each_text_y = days_y() + 60

var res_posy = days_y()
var res_height = 100

var course = []

var room =[{}]
let rooms = [
  {"name": "B112", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "m",
    "start": 585,
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
  }],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E002", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "414", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "w",
    "start": 585,
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
  },{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "w",
    "start": 585,
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
  }], 'th':[],'f':[]}},
  {"name": "G21", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "G26", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E209", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B111", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B002", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B203", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]}}
]
var date =[{}]
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
        console.log(y_text_act)
        return y
}
function res_x(res){
    for (element of days){
        if (element["ref"] ==  res["day"]){
            return days_width*element["num"]+room_width
        }
    }
}

function res_y(){
var y = res_posy;
    res_posy += each_room_height;
    return y;
}

function text_heure_res(res){
    return (res["start"] + " - " + res["end"]);
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

function max(){
for (room of rooms){
     var taller = 0
     for (day of days){
        if(room.courses[day.ref].length > taller){
            taller = room.courses[day.ref].length
            }
     }
    room_max_courses.push(taller)

}
console.log(room_max_courses)
}

function cac_room_height(){
        var h = all_room_height[compt_room_height]
        compt_room_height +=1
        return h
}

function cac_room_y(){
        var y = y_room_act
        y_room_act += all_room_height[compt_room_posy]
        compt_room_posy +=1
        return y
}

function cac_all_height(){
cpt = 0
    for (h of room_max_courses){
        all_room_height[cpt] = (res_height*h)+add_button_height
        cpt +=1
    }
}

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
  .attr("stroke-width",5)
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
  .attr("stroke-width",5)
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
  .attr("stroke-width",5)
  .attr("x",0)
  .attr("y", cac_room_y)
  .attr("width",room_width)
  .attr("height",cac_room_height);

c_room
  .append("text")
  .text(display_text)
  .attr("class","room_name")
  .attr("x",30)
  .attr("y", each_text_posy)


for(element of days){
c_room_gr
    .append("g")
    .attr("class", element["name"])
}
  }


function display_grid(){
c_grid = d3.select(".grille")
  .selectAll(".rect_grid")
  .data(days)
  .append("rect")
  .attr("class","rect_grid")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",days_x)
  .attr("y",days_y)
  .attr("width",days_width)
  .attr("height",res_y)
  }

function display_res(){

c_all_courses = d3.select(".room_lines");

for(room of rooms)
{
    c_all_courses_day = c_all_courses
        .select("."+room_class(room))
            for(day of days){
            courses_all = room.courses[day.ref]
            c_course_res = c_all_courses_day
                .select("."+day.name)
                .selectAll("test")
                .data(room.courses[day.ref])
                .enter()
                .append("g")
                .attr("class",getcourses)

            c_course_res
                .append("rect")
                .attr("class","display_res_frame")
                .attr("fill","none")
                .attr("stroke","black")
                .attr("stroke-width",5)
                .attr("x",res_x)
                .attr("y",days_y)
                .attr("width",days_width)
                .attr("height",res_height)

        }
}
}

/***********
*gestion svg
***********/
function create_days(){
}

display_date();
max();
cac_room_height();
cac_all_height();
display_each_room();
display_res();
display_grid();

d3.select("svg")
        .attr("height", 10000)
        .attr("width", 10000) ;


