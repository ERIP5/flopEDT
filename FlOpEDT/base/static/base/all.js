// This file is part of the FlOpEDT/FlOpScheduler project.
// Copyright (c) 2017
// Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// Affero General Public License for more details.
// 
// You should have received a copy of the GNU Affero General Public
// License along with this program. If not, see
// <http://www.gnu.org/licenses/>.
// 
// You can be released from the requirements of the license by purchasing
// a commercial license. Buying such a license is mandatory as soon as
// you develop activities involving the FlOpEDT/FlOpScheduler software
// without disclosing the source code of your own applications.

/*-------------------
  ---- VARIABLES ----
  -------------------*/



      // {"tot":15,
      //  "colors":[]},
      // {"tot":16,
      //  "colors":[]},
      // {"tot":18,
      //  "colors":[]},
      // {"tot":19,
      //  "colors":[]},
      // {"tot":20,
      //  "colors":[]}





var user = {nom: logged_usr.nom,
	    dispos: [],
	    dispos_bu: [],
	    dispos_type: []
	   };

var margin = {
    top: 250,     // - TOP BANNER - //
    left:  50,
    right:  110,
    bot:  10,
    but: -200
};


var bs_margin_w = 20 ;
var bs_margin_h = 5 ;

var svg = {
    height: window.innerHeight - $("#menu-edt").height() - bs_margin_h,
    width: window.innerWidth - bs_margin_w,
};


var week = 42 ;
var year = 2017;

var labgp = {height: 40, width: 30, tot: 8, height_init: 40, width_init: 30, hm: 40, wm:15};

//dim_dispo.height = 2*labgp.height ;



butgp.tly = margin.but;//-margin_but.ver-6*butgp.height-80 ;
sel_popup.tly = margin.but;


modules.x=sel_popup.selx + sel_popup.selx ;
modules.y=margin.top+gsckd_y(null)-40;
modules.width = 170 ;
modules.height = 0 ;


salles.x=modules.x-1.2*modules.width ; //5*butpr.width;
salles.y=modules.y-modules.height;//.6*butpr.height;
salles.width = 150 ; 
salles.height = modules.height ; 

pref_only = false ;

/*-------------------
  ------ BUILD ------
  -------------------*/


file_fetch.groups.callback = function () {

    create_groups(this.data);

    create_edt_grid();

    create_alarm_dispos() ;
    create_val_but() ;
    create_regen() ;
    create_quote() ;
    
//    go_ack_msg();

    create_bknews();

    go_promo_gp_init() ;


    fetch_all(true, false);

    
    fetch.groups_ok = true;
    create_grid_data();
}







/*---------------------
  ------ STARTER ------
  ---------------------*/


create_general_svg(false);
create_quote()

def_drag();
def_cm_change();

create_clipweek();
create_menus();

create_selections();

fetch_dispos_type();



d3.json(rooms_fi,
 	function(d){ main('rooms', d); } );

d3.json(constraints_fi,
 	function(d){ main('constraints', d); });

d3.json(departments_fi,
 	function(d){ main('department', d); });

d3.json(groupes_fi,
 	function(d){ main('groups', d); } );

    

d3.select("body")
    .on("click", function(d) {
	cancel_cm_adv_preferences();
	cancel_cm_room_tutor_change();
    })




