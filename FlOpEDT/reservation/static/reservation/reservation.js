var allRoom = [];
var roomCourse = []
var allObjectCourses = []
var test = []

show_loader(true);
getRooms();
getCourses();
putCourseRoom();
show_loader(false);

function getRooms(){

$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_fetch_room_reservation,
    async: false,
    contentType: "application/json",
    success: function (msg) {
      allRoom = JSON.parse(msg)
      creationRooms()
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
        organizeCourse(el)
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
    roomCourse = new Object();
    listDays();
    room.courses = roomCourse
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
    newCourse.room = course.room
    newCourse.room_type = course.course.room_type
    newCourse.graded = course.course.is_graded
    newCourse.color_bg = course.course.module.display.color_bg
    newCourse.color_txt = course.course.module.display.color_txt
    newCourse.tutor = course.course.tutor.username
    newCourse.supp_tutors = course.course.supp_tutor
    newCourse.group = []
    for (group of course.course.groups)
    {
    newCourse.group.push(group.name)
    }
    allObjectCourses.push(newCourse)
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
