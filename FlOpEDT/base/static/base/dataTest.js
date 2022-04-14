let thedata = [
{ "day" : "m", "room" : "Amphi1", "start": 8, "end" : 9, "name" : "PSE" },
{ "day" : "m", "room" : "Amphi1", "start": 14, "end" : 16, "name" : "PSE" },
{ "day" : "tu", "room" : "B115", "start": 8, "end" : 18, "name" : "ALE" },
{ "day" : "w", "room" : "B007", "start": 10, "end" : 14, "name" : "MCV" },
{ "day" : "w", "room" : "B007", "start": 8, "end" : 10, "name" : "MCV" },
{ "day" : "th", "room" : "B111", "start": 8, "end" : 9, "name" : "OT" },
{ "day" : "th", "room" : "B112", "start": 8, "end" : 9, "name" : "LN" }
];


let courses = [
  {
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
  },
  {
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
  }
]



let rooms = [{"name": "B112", "bookable":true, "type":"A"}, {"name": "E002", "bookable":true, "type":"A"},
{"name": "414", "bookable":true, "type":"A"}, {"name": "G21", "bookable":true, "type":"A"}, {"name": "G26", "bookable":true, "type":"A"}, {"name": "E209", "bookable":true, "type":"A"},
{"name": "B111", "bookable":true, "type":"A"}, {"name": "B002", "bookable":true, "type":"A"}, {"name": "B203", "bookable":true, "type":"A"}, {"name": "E005", "bookable":true, "type":"A"},
{"name": "VIS3", "bookable":true, "type":"A"}, {"name": "G25", "bookable":true, "type":"A"}, {"name": "B212", "bookable":true, "type":"A"}, {"name": "E117", "bookable":true, "type":"A"},
{"name": "A", "bookable":true, "type":"A"}, {"name": "Amphi1", "bookable":true, "type":"A"}, {"name": "B", "bookable":true, "type":"A"}, {"name": "amphi4", "bookable":true, "type":"A"},
{"name": "E222", "bookable":true, "type":"A"}, {"name": "E210", "bookable":true, "type":"A"}, {"name": "Visio", "bookable":true, "type":"A"}, {"name": "C004", "bookable":true, "type":"A"},
{"name": "E001", "bookable":true, "type":"A"}, {"name": "F113", "bookable":true, "type":"A"}, {"name": "G23", "bookable":true, "type":"A"}, {"name": "C", "bookable":true, "type":"A"}, {"name": "Amphi2", "bookable":true, "type":"A"},
{"name": "314", "bookable":true, "type":"A"}, {"name": "G22", "bookable":true, "type":"A"}, {"name": "STA4", "bookable":true, "type":"A"}, {"name": "D001", "bookable":true, "type":"A"}, {"name": "B003", "bookable":true, "type":"A"},
{"name": "C111", "bookable":true, "type":"A"}, {"name": "E101", "bookable":true, "type":"A"}, {"name": "STA3", "bookable":true, "type":"A"}, {"name": "B212b", "bookable":true, "type":"A"}, {"name": "labo1", "bookable":true, "type":"A"},
{"name": "F222", "bookable":true, "type":"A"}, {"name": "AUTRE", "bookable":true, "type":"A"}, {"name": "E113", "bookable":true, "type":"A"}, {"name": "C001", "bookable":true, "type":"A"}, {"name": "VIS2", "bookable":true, "type":"A"},
{"name": "B001", "bookable":true, "type":"A"}, {"name": "E206", "bookable":true, "type":"A"}, {"name": "C005", "bookable":true, "type":"A"}, {"name": "C114", "bookable":true, "type":"A"}, {"name": "B107", "bookable":true, "type":"A"},
{"name": "STA2", "bookable":true, "type":"A"}, {"name": "313", "bookable":true, "type":"A"}, {"name": "B113", "bookable":true, "type":"A"}, {"name": "E004", "bookable":true, "type":"A"}, {"name": "B201", "bookable":true, "type":"A"},
{"name": "A011", "bookable":true, "type":"A"}, {"name": "C006", "bookable":true, "type":"A"}, {"name": "VIS1", "bookable":true, "type":"A"}, {"name": "E207", "bookable":true, "type":"A"}, {"name": "E103", "bookable":true, "type":"A"},
{"name": "VIS4", "bookable":true, "type":"A"}, {"name": "Amphi3", "bookable":true, "type":"A"}, {"name": "B108", "bookable":true, "type":"A"}, {"name": "F111", "bookable":true, "type":"A"}, {"name": "E003", "bookable":true, "type":"A"},
{"name": "amphi1", "bookable":true, "type":"A"}, {"name": "STA1", "bookable":true, "type":"A"}, {"name": "E208", "bookable":true, "type":"A"}, {"name": "ATCI", "bookable":true, "type":"A"}, {"name": "E114", "bookable":true, "type":"A"},
{"name": "B110", "bookable":true, "type":"A"}, {"name": "VIRT", "bookable":true, "type":"A"}, {"name": "B202", "bookable":true, "type":"A"}, {"name": "E008", "bookable":true, "type":"A"}, {"name": "C003", "bookable":true, "type":"A"},
{"name": "E105", "bookable":true, "type":"A"}, {"name": "B109", "bookable":true, "type":"A"}, {"name": "512", "bookable":true, "type":"A"}, {"name": "G24", "bookable":true, "type":"A"}, {"name": "B234", "bookable":true, "type":"A"},
{"name": "E104", "bookable":true, "type":"A"}, {"name": "E102", "bookable":true, "type":"A"}, {"name": "I21", "bookable":true, "type":"A"}, {"name": "MIB", "bookable":true, "type":"A"}, {"name": "C002", "bookable":true, "type":"A"}]

