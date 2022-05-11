var AllRoom =[]
var Roomcourse = {}


listDays();


$.ajax({
    type: "GET", //rest Type
    dataType: 'text',
    url: url_fetch_room_reservation,
    async: true,
    contentType: "application/json",
    success: function (msg) {
      data = JSON.parse(msg)
      for (room of data)
      {
        creationRooms(room);
      }
      show_loader(false);
    },
    error: function (xhr, error) {
      console.log("error");
      console.log(xhr);
      console.log(error);
      console.log(xhr.responseText);
      show_loader(false);
    }
  });

function listDays()
{
    for (day of days)
    {
        Roomcourse[day.ref]={}
    }
}

function creationRooms(room)
{
    room.courses = Roomcourse
    room.booking = Roomcourse

    AllRoom.push(room)
}
