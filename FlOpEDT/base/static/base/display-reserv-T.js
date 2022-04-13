var days_width = 150
var days_heigth = 1000
var room_width = 100
var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;

/**********************
*gestion des variables*
**********************/

function days_x(day){
    return days_width*(day.num+1)}

function days_y(){
    return 0
}

/**********
*affichage*
**********/

function display_room(){
d3.select("svg")
  .selectAll("rect_date")
  .data(days)
  .enter()
  .append("rect")
  .attr("class","rect_date")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",0)
  .attr("y",0)
  .attr("width",days_width)
  .attr("height",days_heigth)
  }

function display_grid(){
d3.select("svg")
  .selectAll("rect_grid")
  .data(days)
  .enter()
  .append("rect")
  .attr("class","rect_grid")
  .attr("fill","none")
  .attr("stroke","black")
  .attr("stroke-width",5)
  .attr("x",days_x)
  .attr("y",days_y)
  .attr("width",days_width)
  .attr("height",days_heigth)
  }
d3.select("svg")
        .attr("height", days_heigth)
        .attr("width", 1000) ;
display_room();
display_grid();
