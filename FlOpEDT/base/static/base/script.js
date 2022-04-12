/*------------------------
  ------ VARIABLES -------
  ------------------------*/

// input
var jour = 210;
var TD = jour/4;
var TP = TD/2;
var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;
var idays = {};
var groups = {} ;
var day_start = 8*60;      //8*60 ;
var day_end = 18*60+45;    //18*60 + 45 ;


// data
var courses = [] ;
// display settings
var min_to_px = 1 ;
var gp = {width: 30, nb_max: 7} ;


// initialisation function
function init() {

    d3.select("svg")
        .attr("height", svg_height())
        .attr("width", svg_width()) ;

    for(var i = 0 ; i<days.length ; i++){
        idays[days[i].ref] = days[i].num ;
    }

    groups["CE"] = {start: 0, width: 7} ;
    groups["1"] =  {start: 0, width: 2} ;
    groups["1A"] = {start: 0, width: 1} ;
    groups["1B"] = {start: 1, width: 1} ;
    groups["2"] =  {start: 2, width: 2} ;
    groups["2A"] = {start: 2, width: 1} ;
    groups["2B"] = {start: 3, width: 1} ;
    groups["3"] =  {start: 4, width: 2} ;
    groups["3A"] = {start: 4, width: 1} ;
    groups["3B"] = {start: 5, width: 1} ;
    groups["4"] =  {start: 6, width: 1} ;
    groups["234"]= {start: 2, width: 5} ;
}



/*------------------------
  ---- READ DATA FILE ----
  ------------------------*/

// Début de fonction pour récupérer les cours
// stockés sur le serveur
function fetch_courses() {
  //courses = thedata.slice();
  display_grid() ;
  //display_courses() ;
}


function svg_height() {
    return (day_end - day_start) * min_to_px + 200 ;
}
function svg_width() {
    return days.length * gp.nb_max * gp.width ;
}

/*------------------
  ----- DAY --------
  ------------------*/

function day_width(){
  return jour;
}

function day_height(){
  return 645;
}

function day_x(day){
  return day_width()*day.num;
}

function day_y(day){
  return 0;
}

/*------------------
  ----- COURS ------
  ------------------*/

function day_courses_x(c){
  switch (c.day_ref){
    case "m" :
      return 0;
    case "tu" :
      return jour;
    case "w" :
      return jour*2;
    case "th" :
      return jour*3;
    case "f" :
      return jour*4;
  }
  return groups[c.group].start;
}

function group_courses_x(c){
  switch(c.group){
    case "CE":
      return 0;
    case "234" :
      return TD;
    case "1" :
      return 0;
    case "1A" :
      return 0;
    case "1B" :
        return TP;
    case "2" :
      return TD;
    case "2A" :
      return TD;
    case "2B" :
      return TD+TP;
    case "3" :
      return TD*2;
    case "3A" :
      return TD*2;
    case "3B" :
      return TD*2+TP;
    case "4" :
      return TD*3;
  }

}

function course_x(c){
  return day_courses_x(c)+group_courses_x(c);
}

function course_y(c){
  return (c.start-480);
}

function course_width(c){
  if(c.c_type == "TP"){
    return TP;
  }
  else if (c.c_type == "TD"){
    return TD;
  }
  else if(c.c_type == "CM"){
    return jour;
  }
}

function course_height(c){
  return c.duration;
}

function course_color_back(c){
  return c.color_bg;
}

function course_color_text(c){
  return c.color_txt;
}

function get_courses_name(c){
  return c.module;
}
/*------------------
  ----- DISPLAY ----
  ------------------*/
function display_grid(){
d3.select("svg")
  .selectAll("rect")
  .data(days)
  .enter()
  .append("rect")
  .attr("class","jour")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",day_x)
  .attr("y",day_y)
  .attr("width",day_width)
  .attr("height",day_height)

}

function display_courses(){
d3.select("svg")
  .selectAll(".courses")
  .data(courses)
  .enter()
  .append("rect")
  .attr("class","courses")
  .attr("fill",course_color_back)
  .attr("stroke","grey")
  .attr("stroke-width",1)
  .attr("x",course_x)
  .attr("y",course_y)
  .attr("width",course_width)
  .attr("height",course_height)
}

/*------------------
  ------ RUN -------
  ------------------*/

init();
fetch_courses() ;
