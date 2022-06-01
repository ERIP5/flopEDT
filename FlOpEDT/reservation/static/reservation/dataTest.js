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

// useless for now, must display booking with ajax before using it
//let book = [{"idBook": 0, "type": "partiel", "color" = "#99cccc"}, {"idBook": 1, "type": "type", "color" = "#95a5a6"}] ;


let rooms = [
  {"name": "B112", "display":true, "type":"A","y":0, "height":0, "projector":true,"computer":true, 'courses':{'m':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExplBD",
    "c_type": "Projet",
    "day": "m",
    "start": 585,
    "duration": 85,
    "room": "B112",
    "room_type": "M",
    "display": true, // voir models, ya pas
    "id_visio": -1,
    "graded": false,
    "color_bg": "#ec4dd8",
    "color_txt": "#000000",
    "tutor": "PSE",
    "supp_tutors" : [],
    "group": "4B",
    "promo": 0,
    "from_transversal": null // voir models
  }],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E002", "display":true, "type":"A","y":0, "height":0, "projector":true,"computer":false,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "414", "display":true, "type":"A","y":0, "height":0, "projector":false,"computer":true,'courses':{'m':[],'tu':[],'w':[{
    "id_course": 137455,
    "department": 'INFO',
    "mod": "ExploJAVA",
    "c_type": "Projet",
    "day": "w",
    "start": 495,
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
  }],'f':[]},'booking' :{'m':[],'tu':[],'w':[{
    "id_booking" : 123456,
    "responsible" : "Jean",
    "room" : "414",
    "room_type" : "M",
    "day": "w",
    "start" : 700,
    "duration" : 190,
    "title" : "réunion",
    "description": "une reservation pour tester l'affichage des réservations",
    "type": "type",
    "color_bg": "#99cccc",
    "color_txt": "#000000",
    "key":true
},
{
    "id_booking" : 654321,
    "responsible" : "Jeannot",
    "room" : "414",
    "room_type" : "M",
    "day": "w",
    "start" : 900,
    "duration" : 100,
    "title" : "BD",
    "description": "une reservation pour tester l'affichage des réservations",
    "type": "partiel",
    "color_bg": "#95a5a6",
    "color_txt": "#000000",
    "key":true
}], 'th':[],'f':[]}},
  {"name": "G21", "display":false, "type":"A","y":0, "height":0, "projector":false, "computer":false,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "G26", "display":false, "type":"A","y":0, "height":0, "projector":true, "computer":false,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "E209", "display":true, "type":"A","y":0, "height":0, "projector":true, "computer":true,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B111", "display":true, "type":"B","y":0, "height":0, "projector":true, "computer":true,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B002", "display":true, "type":"B","y":0, "height":0, "projector":false, "computer":true,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "B203", "display":true, "type":"B","y":0, "height":0, "projector":false, "computer":true,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}},
  {"name": "Amphi1", "display":true, "type":"amphi","y":0, "height":0, "projector":true, "computer":false,'courses':{'m':[],'tu':[],'w':[], 'th':[],'f':[]},'booking' :{'m':[],'tu':[],'w':[], 'th':[],'f':[]}}
]


let truefalse = ['True','False']