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
var each_room_height = 120

var each_text_y = days_y() + 60

var res_posy = days_y()
var res_height = 75

var course = []

var room =[{}]
let rooms = [
  {"name": "B112", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "f",
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
  }],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "E002", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "414", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "f",
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
  }], 'th':[],'f':[]}]},
  {"name": "G21", "display":false, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "G26", "display":false, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "E209", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "B111", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "B002", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]},
  {"name": "B203", "display":true, "type":"A","y":0, "height":0, 'courses':[{'m':[],'tu':[],'w':[], 'th':[],'f':[]}]}
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

function each_room_posy(){
    var y = each_room_y;
    each_room_y += each_room_height;
    return y;
}

function display_text(res){
    return res["name"]
}

function each_text_posy(){
    var y = each_text_y;
    each_text_y += each_room_height;
    return y;
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

function getsalle(res)
{
    return res["name"]
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

c_room_all = d3.select(".room_lines")
  .selectAll("rect_each_room")
  .data(rooms);

c_room_gr = c_room_all
    .enter()
    .append("g")
    .attr("class",getsalle)

c_room = c_room_gr
    .append("g")
    .attr("class", "bolck_title")

c_room
  .append("rect")
  .attr("class","block_title_frame")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",0)
  .attr("y", each_room_posy)
  .attr("width",room_width)
  .attr("height",each_room_height);

c_room
  .append("text")
  .text(display_text)
  .attr("class","room_name")
  .attr("x",25)
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
  .attr("height",days_height())
  }

function display_res(){
/*
c_res= d3.select(".room_lines")
          .data(rooms);

c_res
    .append("rect")
    .attr("class","cadre_reservation")
    .attr("fill","none")
    .attr("stroke","black")
    .attr("stroke-width",5)
    .attr("x", res_x)
    .attr("y", res_y)
    .attr("width", days_width)
    .attr("height", res_height)
c_res
    .enter()
    .append("text")
    .text(text_heure_res)
    .attr("x",)
    .attr("y", )*/


c_all_courses = d3.select(".room_lines");

for(room of rooms)
{
    c_all_courses_day = c_all_courses
        .select("."+room["name"])
            for(element of days){
            console.log(element["ref"])
            console.log(room)
            c_all_courses_day
                .select("."+element["name"])
                .selectAll("test")
                .data(course)
                .enter()
                .append("g")
                .attr("class","test")
        }
}
}

/***********
*gestion svg
***********/
function create_days(){
}

display_date();
display_each_room();
display_res();

d3.select("svg")
        .attr("height", 10000)
        .attr("width", 10000) ;


