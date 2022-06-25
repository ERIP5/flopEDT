var allRoom = {};
var allAttributes = {};
var roomCourse = []
var allObjectReservations = []
var test = []
var alltype = []
var allTimeSetting = {}
var week_year_context = {'week': week_init, 'year': year_init};
var days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;

function main_reservation() {
    allRoom = {};
    show_loader(true);
     // Week days
    exp_week = wdw_weeks.get_selected();
    $.ajax({
        type: "GET",
        dataType: 'text',
        url: build_url(url_weekdays, exp_week.as_context()),
        async: false,
        contentType: "application/json",
        success: function (msg, ts, req) {
            var sel_week = wdw_weeks.get_selected();
            if (Week.compare(exp_week, sel_week) === 0) {
                week_days = new WeekDays(JSON.parse(msg));
                // week_days = {day_list : [{}, ], day_dict: {m: {}, ...}}
                days = week_days.day_list;
                for (day of days){
                    day.name = day.name.slice(0,3);
                }
            }
        },
        error: function(msg,ts,req){
            console.log(msg);
        }
    });
    getRooms();
    getCourses();
    getReservations();
    getAttributes();
    getTimeSettings();
    sortAllCourses();
    show_loader(false);
}


/*---------------------
  ------- WEEKS -------
  ---------------------*/
// Svg
var svg;

var dsp_svg =
    {
        w: 400,
        h: 440,
        margin: {
            top: 0,     // - TOP BANNER - //
            left: 0,
            right: 0,
            bot: 0
        },
        trans: function () {
            return "translate(" + this.margin.left + "," + this.margin.top + ")";
        }
    };

var dsp_weeks = {
    visible_weeks: 13,
    width: 40,
    height: 30,
    x: 0,      // top of week banner
    y: -40,   // "
    rad: 1.2,  // ratio for the radius of prev/next week buttons
    hfac: 0.9, // ratio for week selection ellipse
    wfac: 0.9, // ratio for week selection ellipse
    cont: null, // will be initiated in create_clipweek
};

// weeks in the current sliding window
var wdw_weeks = new WeeksExcerpt(dsp_weeks.visible_weeks);


function getRooms() {

    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: url_fetch_rooms_reservation,
        async: false,
        contentType: "application/json",
        success: function (msg) {
            jsonRoom = JSON.parse(msg)
            for (room of jsonRoom) {
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

function getCourses() {
    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: build_url(url_fetch_courses_reservation, week_year_context),
        async: false,
        contentType: "application/json",
        success: function (msg) {
            data = JSON.parse(msg);
            for (el of data) {
                if (el.room !== null) {
                    if (el.room.is_basic) {
                        organizeCourse(el)
                    }
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

function getReservations() {
    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: build_url(url_reservation_allReservations, week_year_context),
        async: false,
        contentType: "application/json",
        success: function (msg) {
            for (el of JSON.parse(msg)) {
                organizeReservation(el);
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

function getAttributes() {
    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: url_room_attribute,
        async: false,
        contentType: "application/json",
        success: function (msg) {
            for (data of JSON.parse(msg)) {
                allAttributes[data.id] = data;
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

function getTimeSettings() {
    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: url_base_timesettings,
        async: false,
        contentType: "application/json",
        success: function (msg) {
            allTimeSetting = JSON.parse(msg)
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

function listDays() {
    for (day of days) {
        roomCourse[day.ref] = []
    }
}

function creationRooms(room) {
    newRoom = new Object();
    newRoom.id = room.id;
    newRoom.is_basic = room.is_basic
    newRoom.name = room.name
    newRoom.types = room.types
    newRoom.attributes = room.attributes
    roomCourse = new Object(listDays());
    newRoom.courses = roomCourse
    roomCourse = new Object(listDays());
    let patate = new Object(listDays());
    newRoom.booking = roomCourse
    allRoom[room.name] = newRoom
}

function organizeCourse(course) {
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
    if (course.course.tutor != null) {
        newCourse.tutor = course.course.tutor.username
    } else {
        newCourse.tutor = ""

    }
    newCourse.supp_tutors = course.course.supp_tutor
    newCourse.group = []
    for (group of course.course.groups) {
        newCourse.group.push(group.name)
    }
    allRoom[course.room.name].courses[course.day].push(newCourse)
}

function organizeReservation(res) {
    var reservation = new Object();
    reservation.id_booking = res.id;
    reservation.responsible = res.responsible
    reservation.room = res.room.name
    reservation.room_type = res.room.types
    date = new Date(res.date)
    reservation.day = days[(date.getDay() - 1) % days.length].ref
    startsplit = res.start_time.split(':')
    reservation.start = (parseInt(startsplit[0] * 60 + parseInt(startsplit[1])))
    endsplit = res.end_time.split(':')
    reservation.duration = ((parseInt(endsplit[0] * 60 + parseInt(endsplit[1]))) - reservation.start)
    reservation.title = res.title
    reservation.description = res.description
    reservation.type = res.reservation_type
    reservation.key = res.with_key

    allRoom[reservation.room].booking[reservation.day].push(reservation)
}

function allBasic() {
    for (room in allRoom) {
        if (allRoom[room].is_basic == false) {
            delete allRoom[room]
        }
    }
}


function sortAllCourses() {
    for (room in allRoom) {
        for (day of days) {
            allRoom[room].courses[day.ref].sort(function compare(a, b) {
                if (a.start < b.start)
                    return -1;
                if (a.start > b.start)
                    return 1;
                return 0;
            });
        }
    }
}

// SVG fot the WeekBanner
dsp_svg.margin = {
    top: 50,     // - TOP BANNER - //
    left: 50,
    right: 110,
    bot: 10,
    but: -200
};
dsp_svg.h = window.innerHeight;
dsp_svg.w = window.innerWidth + dsp_svg.margin.left; //- 20 ;

dsp_svg.cadastre = [
    // weeks ground
    ["svg", "wg"],
    ["wg", "wg-bg"],
    ["wg", "wg-fg"],

    //reservation
    ["svg", "dateS"],
    ["svg", "salleS"],
    ["svg", "reservationS"],
    ["svg", "grilleS"],
    ["svg", "scaleS"],
    ["svg", "captionS"],
    ["svg", "dates"],
    ["svg", "room_lines"],
    ["svg", "grille"]
];


svg = new Svg(dsp_svg.layout_tree, false);
svg.create_container();
svg.create_layouts(dsp_svg.cadastre);


wdw_weeks.add_full_weeks(week_year_list);

// go to selected week
WeekBanner.prototype.apply_wk_change = function (d, i) { //if(fetch_status.done) {
    this.mix.weeks.change_selection(i);
    this.update(false);
    sel_week = wdw_weeks.get_selected();
    week_year_context.week = sel_week.week;
    week_year_context.year = sel_week.year;
    rmv_total();
    main_reservation();
    if (rmvStatut == 1) {
        mainT()
    }

    if (rmvStatut == 2) {
        mainS()
    }
    ;
}; //}
var week_banner = new WeekBanner(svg, "wg", "wg-fg", "wg-bg", wdw_weeks, dsp_weeks);
week_banner.spawn();


main_reservation();
