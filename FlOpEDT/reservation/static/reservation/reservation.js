var allRoom = {};
var allAttributes = [];
var roomCourse = []
var allObjectCourses = []
var test = []
var alltype = []


function main_reservation(){
show_loader(true);
getRooms();
getCourses();
getAttributes();
//getRoomAttributes();
sortAllCourses();
show_loader(false);
}

function getRooms(){

$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_fetch_rooms_reservation,
    async: false,
    contentType: "application/json",
    success: function (msg) {
      jsonRoom = JSON.parse(msg)
      for (room of jsonRoom){
        creationRooms(room)
      }
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

function getAttributes(){
$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_room_attribute,
    async: false,
    contentType: "application/json",
    success: function (msg) {
        allAttributes = msg
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

function getRoomAttributes(){
$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_room_attribute,
    async: false,
    contentType: "application/json",
    success: function (msg) {
        allAttributes = msg
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

function creationRooms(room){
    newRoom = new Object();
    newRoom.id = room.id;
    newRoom.is_basic = room.is_basic
    newRoom.name = room.name
    newRoom.types = room.types
    roomCourse = new Object(listDays());
    newRoom.courses = roomCourse
    roomCourse = new Object(listDays());
    newRoom.attributes = {}
    newRoom.booking = roomCourse
    allRoom[room.name]= newRoom
}

function organizeCourse(course)
{
    var newCourse = new Object();
    newCourse.id = course.id
    newCourse.department = course.course.type.department
    newCourse.mod = course.course.module.abbrev
    newCourse.C_type = course.course.type.name
    newCourse.day = course.day
    newCourse.start = course.start_time
    newCourse.duration = course.course.type.duration
    newCourse.room = course.room.name
    newCourse.room_type = course.course.room_type
    newCourse.graded = course.course.is_graded
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
    allRoom[course.room.name].courses[course.day].push(newCourse)
}

function allBasic()
{
    for (room in allRoom)
    {
        if (allRoom[room].is_basic == false){
            delete allRoom[room]
        }
    }
}

function sortAllCourses()
{
for (room in allRoom){
        for(day of days){
        allRoom[room].courses[day.ref].sort(function compare(a, b)
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
