var allRoom = [];
var allDept = [];
var roomCourse = []
var allObjectCourses = []
var test = []
var alltype = []

show_loader(true);
getRooms();
getCourses();
getDepts();
putCourseRoom();
sortAllCourses();
show_loader(false);

function getRooms(){

$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_fetch_rooms_reservation,
    async: false,
    contentType: "application/json",
    success: function (msg) {
      allRoom = JSON.parse(msg)
      creationRooms()
        allBasic();
    },
    error: function (xhr, error) {
      console.log("error");
      console.log(xhr);
      console.log(error);
      console.log(xhr.responseText);
      show_loader(false);
    }
  });
}

function getCourses()
{let my = {"week" : 11 , "year" :2022}
$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: build_url(url_fetch_courses_reservation, my),
    async: false,
    contentType: "application/json",
    success: function (msg) {
      data = JSON.parse(msg)
      for (el of data)
      {
        if(el.room.is_basic){
            organizeCourse(el)
        }else{
            organizeNotBasicCourses(el)
        }

      }
    },
    error: function (xhr, error) {
      console.log("error");
      console.log(xhr);
      console.log(error);
      console.log(xhr.responseText);
      show_loader(false);
    }
  });
}

function getDepts(){
    $.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_fetch_departments_reservation,
    async: false,
    contentType: "application/json",
    success: function (msg) {
      allDept = JSON.parse(msg)
      console.log(allDept)
    },
    error: function (xhr, error) {
      console.log("error");
      console.log(xhr);
      console.log(error);
      console.log(xhr.responseText);
      show_loader(false);
    }
  });
}
function listDays()
{
    for (day of days)
    {
        roomCourse[day.ref]=[]
    }
}

function creationRooms()
{
    for (room of allRoom)
    {
    roomCourse = new Object(listDays());
    room.courses = roomCourse
    roomCourse = new Object(listDays());
    room.booking = roomCourse
    }
}

function organizeCourse(course)
{
    var newCourse = new Object();
    newCourse.id = course.id
    newCourse.department = course.course.type.department.abbrev
    newCourse.mod = course.course.module.abbrev
    newCourse.C_type = course.course.type.name
    newCourse.day = course.day
    newCourse.start = course.start_time
    newCourse.duration = course.course.type.duration
    newCourse.room = course.room.name
    newCourse.room_type = course.course.room_type
    newCourse.graded = course.course.is_graded
    newCourse.color_bg = course.course.module.display.color_bg
    newCourse.color_txt = course.course.module.display.color_txt
    if (course.course.tutor != null)
    {
        newCourse.tutor = course.course.tutor.username
    }
    else
    {
        newCourse.tutor = ""

    }
    newCourse.supp_tutors = course.course.supp_tutor
    newCourse.group = []
    for (group of course.course.groups)
    {
        newCourse.group.push(group.name)
    }
    allObjectCourses.push(newCourse)
}

function organizeNotBasicCourses(course)
{
    if ((course.room.name).includes('+')){
        var tabRoomC = (course.room.name).split('+')
        var pref = (course.room.name.substr(0,1))
        for (room of tabRoomC){
            if(room.substr(0,1) == pref){
                course.room.name = room
            }else{
                course.room.name = pref+room
            }
            organizeCourse(course)
        }
    }
    if ((course.room.name).includes('-')){
        var tabRoomC = (course.room.name).split('-')
        for (room of tabRoomC){
            course.room.name = room
            organizeCourse(course)
        }
    }

}

function putCourseRoom()
{
    allRoom.forEach(element => addCourse(element))
}

function addCourse(room)
{
    for (course of allObjectCourses)
    {
        if(room.name == course.room)
        {
            room.courses[course.day].push(course)
        }
    }
}

function allBasic()
{
    for (room of allRoom)
    {
        if (room.is_basic == false)
        {
            var remove = allRoom.indexOf(room)
            if (remove != -1)
            {
                allRoom.splice(remove)
            }
        }
    }
}

function sortAllCourses()
{
for (room of allRoom){
        for(day of days){
        room.courses[day.ref].sort(function compare(a, b)
            {
                if (a.start < b.start)
                    return -1;
                if (a.start > b.start )
                    return 1;
                return 0;
            });
        }
    }
}
