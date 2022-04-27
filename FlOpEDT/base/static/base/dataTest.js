let thedata = [
{ "day" : "m", "room" : "Amphi1", "start": 8, "end" : 9, "name" : "PSE" },
{ "day" : "m", "room" : "Amphi1", "start": 14, "end" : 16, "name" : "PSE" },
{ "day" : "tu", "room" : "B115", "start": 8, "end" : 18, "name" : "ALE" },
{ "day" : "w", "room" : "B007", "start": 10, "end" : 14, "name" : "MCV" },
{ "day" : "w", "room" : "B007", "start": 8, "end" : 10, "name" : "MCV" },
{ "day" : "th", "room" : "B111", "start": 8, "end" : 9, "name" : "OT" },
{ "day" : "th", "room" : "B112", "start": 8, "end" : 9, "name" : "LN" }
];

let days = [{num: 0, ref: "m", name: "Lundi"},
            {num: 1, ref: "tu", name: "Mardi"},
            {num: 2, ref: "w", name: "Mercredi"},
            {num: 3, ref: "th", name: "Jeudi"},
            {num: 4, ref: "f", name: "Vendredi"}] ;


let rooms = [
  {"name": "B112", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "m",
    "start": 585,
    "duration": 85,
    "room": "B112",
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
  }],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E002", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "414", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExploJAVA",
    "c_type": "Projet",
    "day": "w",
    "start": 480,
    "duration": 85,
    "room": "414",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#CCFF99",
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
    "room": "414",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd7",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  },], 'th':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "th",
    "start": 585,
    "duration": 85,
    "room": "414",
    "room_type": "M",
    "display": true,
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd7",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null
  }],'f':[]},'booking' :{'m':[{
    "id_booking" : 123456,
    "responsible" : "Jean",
    "room" : "G21",
    "room_type" : "M",
    "start" : 480,
    "duration" : 190,
    "title" : "réunion",
    "description": "une reservation pour tester l'afficahge des réservations",
    "type": "type",
    "key":true
}],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "G21", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "G26", "display":false, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E209", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B111", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B002", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B203", "display":true, "type":"A","y":0, "height":0, 'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}}
]


let restest = {
"id_booking" : 123456,
"responsible" : "Jean",
"room" : "G21",
"room_type" : "M",
"start" : 480,
"duration" : 190,
"title" : "réunion",
"description": "une reservation pour tester l'afficahge des réservations",
"type": "type",
"key":true
}


