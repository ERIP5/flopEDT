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





           /*     \
          ----------           
        --------------         
      ------------------       
    ----------------------     
  --------------------------   
------------------------------ 
-------    CREATION    -------
------------------------------ 
  --------------------------   
    ----------------------     
      ------------------       
        --------------         
          ----------           
                 */




/*----------------------
  -------   SVG  -------
  ----------------------*/



function create_general_svg(light) {
    var tot;

    if (light) {
        tot = d3.select("body");
    } else {
        tot = d3.select("body").append("div");

        mog = tot
            .append("div")
            .attr("id", "div-mod")
            .text("Module ")
            .append("select")
            .attr("id", "dd-mod")
            .on("change", go_modules);

        sag = tot
            .append("div")
            .attr("id", "div-sal")
            .text("Salle ")
            .append("select")
            .attr("id", "dd-sal")
            .on("change", go_rooms);


    }

    svg_cont = tot
        .append("svg")
        .attr("width", svg.width)
        .attr("height", svg.height)
        .attr("id", "edt-main")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    create_layouts(svg_cont, light);

    // var divtip = d3.select("body").append("div")
    // 	.attr("class", "tooltip")
    // 	.style("opacity", 0);

}




function create_layouts(svg_cont, light) {
    // menus ground
    meg = svg_cont.append("g")
        .attr("id", "lay-meg");

    // weeks ground
    wg.upper = svg_cont.append("g")
        .attr("id", "lay-wg");
    wg.bg = wg.upper.append("g")
        .attr("id", "wg-bg");
    wg.fg = wg.upper.append("g")
        .attr("id", "wg-fg");

    // groupes ground
    gpg = svg_cont.append("g")
        .attr("id", "lay-gpg");

    // profs ground
    prg = svg_cont.append("g")
        .attr("id", "lay-prg");

    // module ground
    // moved directly to the html
    
    //  mog = d3.select("body").select("select")
    // svg_cont.append("g")
    // 	.attr("id","lay-mog")
    // 	.attr("transform","translate("+modules.x+","+modules.y+")")
    // 	.append("foreignObject")
    // 	.append("xhtml:select")
    // 	.attr("id","dd-mod")
    //	.on("change",go_modules);


    if (!light) {

        $("#div-mod").css("width", modules.width);
        $("#div-mod").css({
            position: "relative",
            left: modules.x,
            top: modules.y
        });
        $("#div-mod").css("height", modules.height);

        $("#div-sal").css("width", salles.width);
        $("#div-sal").css({
            position: "relative",
            left: salles.x,
            top: salles.y
        });
        $("#div-sal").css("height", salles.height);

    }



    // semaine type ground
    stg = svg_cont.append("g")
        .attr("id", "lay-stg");


    // dispos info ground
    dig = svg_cont.append("g")
        .attr("id", "lay-dg");


    // valider
    vg = svg_cont.append("g")
        .attr("id", "lay-vg");

    // background, middleground, foreground, dragground
    var edtg = svg_cont.append("g")
        .attr("id", "lay-edtg");
    bg = edtg.append("g")
        .attr("id", "lay-bg");
    mg = edtg.append("g")
        .attr("id", "lay-mg");
    fig = edtg.append("g")
        .attr("id", "lay-fig");
    fg = edtg.append("g")
        .attr("id", "lay-fg");

    // logo ground
    log = edtg.append("g")
        .attr("id", "lay-log");

    // drag ground
    dg = svg_cont.append("g")
        .attr("id", "lay-dg");


}




/*---------------------------
  ------- PREFERENCES -------
  ---------------------------*/

function create_alarm_dispos() {
    di = dig
        .append("g")
        .attr("text-anchor", "start")
        .attr("class", "disp-info");

    di
        .append("text")
        .attr("class", "disp-required")
        .text(txt_reqDispos);

    di
        .append("text")
        .attr("class", "disp-filled")
        .text(txt_filDispos);
}


/*---------------------
  ------- WEEKS -------
  ---------------------*/



// PRECONDITION: semaine_init, week_init, weeks.init_data
function find_week(week_list) {
    var i, up;
    i = 0;
    up = false ;
    
    while (i < week_list.length && !up) {
        if (an_init < week_list[i].an ||
            (an_init == week_list[i].an &&
                semaine_init < week_list[i].semaine)) {
            up = true;
        } else {
            i++;
        }
    }
    if (!up) {
        i = 0;
    }
    return i;
}




function create_clipweek() {

    weeks.init_data = semaine_an_list;

    var min = weeks.init_data[0];
    var max = weeks.init_data[weeks.init_data.length - 1];

    weeks.ndisp = Math.min(weeks.ndisp, weeks.init_data.length);

    weeks.init_data.push({
        an: max.an,
        semaine: max.semaine + 1
    });
    weeks.init_data.unshift({
        an: min.an,
        semaine: min.semaine - 1,
    });

    var fw ;

    if (min.an > an_init ||
	(min.an == an_init && min.semaine > semaine_init)) {
	weeks.cur_data = weeks.init_data.slice(1,
					       1 + weeks.ndisp + 2);
	weeks.fdisp = 1;
	weeks.sel[0] = 2 ;
	
    } else if (max.an < an_init ||
	(max.an == an_init && max.semaine < semaine_init)) {
	weeks.cur_data = weeks.init_data.slice(weeks.init_data.length - 1  - 2 - weeks.ndisp,
					       weeks.init_data.length -1);
	weeks.fdisp = weeks.init_data.length - 1  - 2 - weeks.ndisp ;
	weeks.sel[0] = weeks.ndisp ;
    } else {
	var fw = find_week(weeks.init_data);
	
	fw = Math.max(
            Math.min(fw - 2,
		     weeks.init_data.length - 1 - (weeks.ndisp + 1)),
            0);
	
	weeks.cur_data = weeks.init_data.slice(fw,
					       fw + weeks.ndisp + 2);
	
	weeks.fdisp = fw;
	
	weeks.sel[0] = fw + find_week(weeks.cur_data) - 1 ;
    }


    wg.upper
        .attr("transform", "translate(" + weeks.x + "," + weeks.y + ")");


    wg.fg
        .selectAll(".sel_wk")
        .data(weeks.sel)
        .enter()
        .append("g")
        .attr("class", "sel_wk")
        .attr("clip-path", "url(#clipwk)")
        .attr("pointer-events", "none")
        .append("ellipse")
        .attr("cx", week_sel_x)
        .attr("cy", .5 * weeks.height)
        .attr("rx", .5 * weeks.wfac * weeks.width)
        .attr("ry", .5 * weeks.hfac * weeks.height);



    var but =
        wg.fg
        .append("g")
        .attr("class", "cir_wk")
        .on("click", week_left);


    but
        .append("circle")
        .attr("stroke", "white")
        .attr("stroke-width", 1)
        .attr("cx", 0)
        .attr("cy", .5 * weeks.height)
        .attr("r", weeks.rad * .5 * weeks.height);

    but
        .append("text")
        .attr("fill", "white")
        .attr("x", 0)
        .attr("y", .5 * weeks.height)
        .text("<");


    but =
        wg.fg
        .append("g")
        .attr("class", "cir_wk")
        .on("click", week_right);

    but
        .append("circle")
        .attr("stroke", "white")
        .attr("stroke-width", 1)
        .attr("cx", (weeks.ndisp + 1) * weeks.width)
        .attr("cy", .5 * weeks.height)
        .attr("r", weeks.rad * .5 * weeks.height)

    but
        .append("text")
        .attr("fill", "white")
        .attr("x", (weeks.ndisp + 1) * weeks.width)
        .attr("y", .5 * weeks.height)
        .text(">");


    wg.bg
        .append("rect")
        .attr("class", "cir_wk")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", (weeks.ndisp + 1) * weeks.width)
        .attr("height", weeks.height);

    wg.bg
        .append("g")
        .append("clipPath")
        .attr("id", "clipwk")
        .append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("height", weeks.height)
        .attr("width", (weeks.ndisp + 1) * weeks.width);

    weeks.cont = wg.bg
        .append("g")
        .attr("clip-path", "url(#clipwk)");


    go_week_menu(true);
}






/*----------------------
  -------- GRID --------
  ----------------------*/


// PRE: groups
function create_edt_grid() {
    create_grid_data();
    //go_grid(false);
}



function add_garbage(){
    data_slot_grid.push(garbage);
}
function remove_garbage(){
    var found = false ;
    var i  = 0 ;
    while(!found && i < data_slot_grid.length){
	if (data_slot_grid[i].day == garbage.day
	    && data_slot_grid[i].slot == garbage.slot) {
	    found = true ;
	    data_slot_grid.splice(i,1);
	}
	i += 1 ;
    }
}


function create_grid_data() {
    for (var j = 0; j < nbPer; j++) {
        for (var s = 0; s < nbSl; s++) {
            var gs = {
                day: j,
                slot: s,
                display: false,
                dispo: false,
                pop: false,
                reason: ""
            };
            data_slot_grid.push(gs);
        }
    }

    for (var p = 0; p < set_promos.length; p++) {
        compute_promo_leaves(root_gp[p].gp);
    }


    for (var s = 0; s < nbSl; s++) {
        for (var r = 0; r < set_rows.length; r++) {
            var gscp = {
                row: r,
                slot: s,
                name: set_promos[row_gp[r].promos[0]]
            };
            for (var p = 1; p < row_gp[r].promos.length; p++) {
                gscp.name += "|";
                gscp.name += set_promos[row_gp[r].promos[p]];
            }
            data_grid_scale_row.push(gscp);
        }
    }
    create_dh_keys();
}



function create_dh_keys() {
    bg
        .selectAll(".gridsckd")
        .data(data_grid_scale_day)
        .enter()
        .append("text")
        .attr("class", "gridsckd")
        .attr("x", gsckd_x)
        .attr("y", gsckd_y)
        .attr("font-size", 13)
        .attr("font-weight", "bold")
        .text(gsckd_txt);

    bg
        .selectAll(".gridsckh")
        .data(data_grid_scale_hour)
        .enter()
        .append("text")
        .attr("class", "gridsckh")
        .attr("x", gsckh_x)
        .attr("y", gsckh_y)
        .text(gsckh_txt);


}



/*----------------------
  -------- SCALE -------
  ----------------------*/

function create_but_scale() {
    def_drag_sca();

    var grp = fg
        .append("g")
        .attr("class", "h-sca")
        .attr("cursor", "pointer")
        .call(drag_listener_hs);

    grp
        .append("rect")
        .attr("fill", "darkslategrey")
        .attr("x", but_sca_h_x())
        .attr("y", but_sca_h_y())
        .attr("width", but_sca_thick())
        .attr("height", but_sca_long());

    grp
        .append("path")
        .attr("d", but_sca_tri_h(0))
        .attr("stroke", "white")
        .attr("fill", "white");



    grp = fg
        .append("g")
        .attr("class", "v-sca")
        .attr("cursor", "pointer")
        .call(drag_listener_vs);
    grp
        .append("rect")
        .attr("fill", "darkslategrey")
        .attr("x", but_sca_v_x())
        .attr("y", but_sca_v_y())
        .attr("width", but_sca_long())
        .attr("height", but_sca_thick());

    grp
        .append("path")
        .attr("d", but_sca_tri_v(0))
        .attr("stroke", "white")
        .attr("fill", "white");


}


function def_drag_sca() {
    drag_listener_hs = d3.drag()
        .on("start", function(c) {
            if (fetch.done) {
                drag.sel = d3.select(this);
                drag.x = 0;
                drag.y = 0;
                drag.svg = d3.select("#edt-main");
                drag.svg_w = +drag.svg.attr("width");
                drag.init = +drag.sel.select("rect").attr("x");
                dg.node().appendChild(drag.sel.node());


                drag.sel
                    .append("g")
                    .attr("class", "h-sca-l")
                    .append("line")
                    .attr("x1", drag.init)
                    .attr("y1", 0)
                    .attr("x2", drag.init)
                    .attr("y2", grid_height())
                    .attr("stroke", "black")
                    .attr("stroke-width", 2)
                    .attr("stroke-dasharray", "21,3,3,3");

            }
        })
        .on("drag", function(c) {
            if (fetch.done) {
                drag.x += d3.event.dx;
                if (drag.x + drag.init > 0) {
                    drag.sel.attr("transform", "translate(" + drag.x + "," + drag.y + ")");
                    if (drag.init + drag.x + margin.left + margin.right > drag.svg_w) {
                        drag.svg.attr("width", drag.init + drag.x + margin.left + margin.right);
                    }
                }
            }
        })
        .on("end", function(c) {
            if (fetch.done) {
                if (drag.x + drag.init <= 0) {
                    drag.x = -drag.init;
                }
                drag.sel.attr("transform", "translate(0,0)");
                drag.sel.select("rect").attr("x", drag.init + drag.x);
                if (rootgp_width != 0) {
                    labgp.width = ((drag.x + drag.init) / nbPer - dim_dispo.plot * (dim_dispo.width + dim_dispo.right)) / rootgp_width;
                }
                drag.sel.select("path").attr("d", but_sca_tri_h(0));
                //(drag.x+drag.init)/(grid_width());
                go_edt(false);
                fg.node().appendChild(drag.sel.node());
                drag.sel.select(".h-sca-l").remove();
            }
        });

    drag_listener_vs = d3.drag()
        .on("start", function(c) {
            if (fetch.done) {
                drag.sel = d3.select(this);
                drag.x = 0;
                drag.y = 0;
                drag.init = +drag.sel.select("rect").attr("y");
                dg.node().appendChild(drag.sel.node());
                drag.svg = d3.select("#edt-main")
                drag.svg_h = +drag.svg.attr("height"); //+200;

                drag.sel
                    .append("g")
                    .attr("class", "v-sca-l")
                    .append("line")
                    .attr("x1", 0)
                    .attr("y1", drag.init)
                    .attr("x2", but_sca_h_mid_x())
                    .attr("y2", drag.init)
                    .attr("stroke", "black")
                    .attr("stroke-width", 2)
                    .attr("stroke-dasharray", "21,3,3,3");

            }
        })
        .on("drag", function(c) {
            if (fetch.done) {
                drag.y += d3.event.dy;
                if (drag.init + drag.y >= 0) {
                    drag.sel.attr("transform",
				  "translate(" + drag.x + "," + drag.y + ")");
                    drag.svg.attr("height", drag.svg_h + drag.y);
                }
//                console.log(drag.svg.attr("height"));
            }
        })
        .on("end", function(c) {
            if (fetch.done) {
                if (drag.init + drag.y < 0) {
                    drag.y = -(drag.init);
                }
                labgp.height = labgp_from_grid_height(drag.init + drag.y) ;
		//                drag.sel.select("path").attr("d", but_sca_tri_v(drag.y));
                drag.sel.attr("transform", "translate(0,0)");
                drag.sel.select("rect").attr("y", grid_height());
		drag.sel.select("path").attr("d", but_sca_tri_v(0));
                go_edt(false);
                fg.node().appendChild(drag.sel.node());
                drag.sel.select(".v-sca-l").remove();

		svg.height = svg_height() ;
		d3.select("#edt-main").attr("height", svg.height);

//		drag.svg.attr("height", svg_height());
            }
        });

}



/*----------------------
  ------- GROUPS -------
  ----------------------*/

// Only for the current case
function set_butgp() {
    var topx = 620;

    root_gp[0].buty = margin.but;
    root_gp[0].butx = topx;
    root_gp[1].buty = root_gp[0].buty + 3 * butgp.height + margin_but.ver;
    root_gp[1].butx = topx - .5 * margin_but.hor;
    root_gp[2].buty = root_gp[1].buty;
    root_gp[2].butx = root_gp[1].butx + margin_but.hor;


}



function indexOf_promo(promo) {
    for (var p = 0 ; p < set_promos.length ; p++ ) {
	if (set_promos[p] == promo_init ) {
	    return p ;
	}
    }
    return -1 ;
}

function go_promo_gp_init(button_available) {
    var gp_2_click = [] ;
    var found_gp, gpk, gpc, gpa ;

    if (promo_init != 0){
	promo_init = indexOf_promo(promo_init) ;
	if (gp_init == "") {
	    gp_init = root_gp[promo_init].gp.nom ;
	}
	if (Object.keys(groups[promo_init]).map(function(g) { return groups[promo_init][g].nom ; }).indexOf(gp_init) != -1) {
	    apply_gp_display(groups[promo_init][gp_init], true, button_available);
	}
    } else if (gp_init != "") {
	if (Object.keys(groups[0]).map(function(g) { return groups[0][g].nom ; }).indexOf(gp_init) != -1) {
	    apply_gp_display(groups[0][gp_init], true, button_available);
	}
    }
}


function create_groups(data_groups) {
    extract_all_groups_structure(data_groups);
    set_butgp();
    update_all_groups();
}


function extract_all_groups_structure(r) {
    var init_nbPromos = r.length;
    for (var npro = 0; npro < init_nbPromos; npro++) {
        extract_groups_structure(r[npro], -1, -1);
    }
}

function extract_groups_structure(r, npro, nrow) {
    var gr = {
        nom: r.name,
        ancetres: null,
        descendants: null,
        display: true,
        parent: null,
        children: null,
        x: 0,
        maxx: 0,
        width: 0,
        est: 0,
        lft: 0,
    }

    if ("undefined" === typeof r.buth) {
        gr.buth = 1;
    } else {
        gr.buth = r.buth * .01;
    }

    if ("undefined" === typeof r.buttxt) {
        gr.buttxt = gr.nom;
    } else {
        gr.buttxt = r.buttxt;
    }
    

    if (r.parent == "null") {

        // promo number should be unique
        set_promos.push(r.promo);

        npro = set_promos.indexOf(r.promo);


        // promo number should be unique
        groups[npro] = [];
        root_gp[npro] = {};


        root_gp[npro].gp = gr;

        if (set_rows.indexOf(r.row) == -1) {
            set_rows.push(r.row);
            row_gp[set_rows.indexOf(r.row)] = {};
            row_gp[set_rows.indexOf(r.row)].promos = [];
        }
        nrow = set_rows.indexOf(r.row);

        root_gp[npro].row = nrow;

        row_gp[nrow].promos.push(npro);

    } else {
        gr.parent = r.parent;
    }

    gr.promo = npro;


    if ("undefined" === typeof r.children || r.children.length == 0) {
        gr.children = [];
    } else {
        gr.children = r.children.map(function(d) {
            return d.name;
        });
        for (var i = 0; i < r.children.length; i++) {
            extract_groups_structure(r.children[i], npro, nrow);
        }
    }
    groups[npro][gr.nom] = gr;
}



// Earliest Starting Time (i.e. leftest possible position)
// for a node and its descendance, given node.est
function compute_promo_est_n_wh(node) {
    var child;


    if (node.parent == null) {
        node.ancetres = [];
        node.by = 0;
	root_gp[node.promo].maxby = node.by + node.buth ;
    } else {
	if (node.by + node.buth > root_gp[node.promo].maxby) {
	    root_gp[node.promo].maxby = node.by + node.buth ;
	}
    }
    node.descendants = [];


    node.width = 0;
    if (node.children.length == 0) {
        node.width = 1;
    } else {
        for (var i = 0; i < node.children.length; i++) {
            child = groups[node.promo][node.children[i]];
            child.est = node.est + node.width;
            child.by = node.by + node.buth;
            if (!child.display) {
                child.width = 0;
            } else {
                child.ancetres = node.ancetres.slice(0);
                child.ancetres.push(node.nom);
                compute_promo_est_n_wh(child);
                node.descendants = node.descendants.concat(child.descendants);
                node.descendants.push(child.nom);
            }
            node.width += child.width;
        }
    }
}

// Latest Finishing Time (i.e. rightest possible position)
// for a node and its descendance, given node.lft
function compute_promo_lft(node) {
    var child;
    var eaten = 0;
    for (var i = node.children.length - 1; i >= 0; i--) {
        child = groups[node.promo][node.children[i]];
        child.lft = node.lft - eaten;
        compute_promo_lft(child);
        eaten += child.width;
    }
}


// Least Mobile X 
function compute_promo_lmx(node) {
    var child;

    //    console.log(node.promo,node.nom,node.x,node.maxx);

    if (node.x < node.est) {
        node.x = node.est;
    }
    if (node.x + node.width > node.lft) {
        node.x = node.lft - node.width;
    }

    if (node.children.length == 0) {
        node.maxx = node.x + node.width;
    } else {
        var lastmax = node.x;
        var lastmin = -1;
        for (var i = 0; i < node.children.length; i++) {
            child = groups[node.promo][node.children[i]];
            if (child.display) {
                if (child.x < lastmax) {
                    child.x = lastmax;
                }
                compute_promo_lmx(child);
                if (lastmin == -1) {
                    lastmin = child.x;
                }
                lastmax = child.maxx;
            }
        }
        if (node.display) {
            node.maxx = lastmax;
            node.x = lastmin;
        }
    }

    //  //console.log(node.promo,node.nom,node.x,node.maxx);

}



function update_all_groups() {
    var max_rw = 0;
    var cur_rw, root, disp;

    // compute EST and width, and compute display row
    for (var r = 0; r < set_rows.length; r++) {
        cur_rw = 0;
        disp = false;
        for (var p = 0; p < row_gp[r].promos.length; p++) {
            root = root_gp[row_gp[r].promos[p]].gp;
            root.est = cur_rw;
            compute_promo_est_n_wh(root);
            cur_rw += root.width;
            if (root.display) {
                row_gp[r].display = true;
            }
        }
        if (cur_rw > max_rw) {
            max_rw = cur_rw;
        }
    }
    rootgp_width = max_rw;

    if (rootgp_width > 0) {
        if (pos_rootgp_width == 0) {
            pos_rootgp_width = rootgp_width;
        }
        labgp.width *= pos_rootgp_width / rootgp_width;
        pos_rootgp_width = rootgp_width;
    }



    // compute LFT
    for (var r = 0; r < set_rows.length; r++) {
        cur_rw = max_rw;
        for (var p = row_gp[r].promos.length - 1; p >= 0; p--) {
            root = root_gp[row_gp[r].promos[p]].gp;
            root.lft = cur_rw;
            compute_promo_lft(root);
            cur_rw -= root.width;
        }
    }
    // move x if necessary
    for (var r = 0; r < set_rows.length; r++) {
        cur_rw = 0;
        for (var p = 0; p < row_gp[r].promos.length; p++) {
            root = root_gp[row_gp[r].promos[p]].gp;
            if (root.x < cur_rw) {
                root.x = cur_rw;
            }
            compute_promo_lmx(root);
            cur_rw = root.maxx;
        }
    }

    // move y if necessary
    nbRows = 0;
    for (var r = 0; r < set_rows.length; r++) {
        root = row_gp[r];
        root.display = false;
        root.y = nbRows;
        for (var p = 0; p < row_gp[r].promos.length; p++) {
            root.display = root.display || root_gp[root.promos[p]].gp.display;
        }
        if (root.display) {
            nbRows += 1;
        }
    }

    if (nbRows > 0) {
        if (pos_nbRows == 0) {
            pos_nbRows = nbRows;
        }
        labgp.height *= pos_nbRows / nbRows;
        pos_nbRows = nbRows;
    }


    //    compute_promo_lmx(node)
}



// data related to leaves
function compute_promo_leaves(node) {
    var gp;

    if (node.children.length == 0) {
        for (var j = 0; j < nbPer; j++) {
            data_grid_scale_gp.push({
                day: j,
                gp: node
            });
            for (var s = 0; s < nbSl; s++) {
                if (!is_free(j, s, node.promo)) {
                    data_mini_slot_grid.push({
                        day: j,
                        slot: s,
                        gp: node
                    });
                }
            }
        }
    }

    for (var i = 0; i < node.children.length; i++) {
        child = groups[node.promo][node.children[i]];
        compute_promo_leaves(child);
    }
}


/*--------------------
  ------ MENUS -------
  --------------------*/



function create_menus() {

    meg
        .attr("transform", "translate(" + menus.x + "," + menus.y + ")")
        .attr("text-anchor", "start")
        .attr("font-size", 18);

    meg
        .append("rect")
        .attr("class", "menu")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", menus.coled + menus.colcb)
        .attr("height", 160) //(Object.keys(ckbox).length+1)*menus.h)
        .attr("rx", 10)
        .attr("ry", 10);

    meg
        .append("rect")
        .attr("class", "menu")
        .attr("x", menus.dx)
        .attr("y", 0)
        .attr("width", menus.coled + menus.colcb)
        .attr("height", 160) //(Object.keys(ckbox).length+1)*menus.h)
        .attr("rx", 10)
        .attr("ry", 10);

    meg
        .append("text")
        .attr("x", menus.mx)
        .attr("y", menus.h - 10)
        .attr("fill", "black")
        .text("Cours :");

    meg
        .append("text")
        .attr("x", menus.mx + menus.dx)
        .attr("y", menus.h - 10)
        .attr("fill", "black")
        .text("Dispos :");

    go_menus();
}



/*---------------------
  ------- BKNEWS ------
  ---------------------*/

function create_regen() {
    vg
        .append("g")
        .attr("class", "ack-reg")
        .append("text");
}




function create_bknews() {
    var flash = fig
	.append("g")
	.attr("class", "flashinfo");


    flash
	.append("line")
	.attr("class","bot-bar")
        .attr("stroke", "black")
        .attr("stroke-width", 4)
        .attr("x1", 0)
        .attr("y1", bknews_bot_y())
        .attr("x2", grid_width())
        .attr("y2", bknews_bot_y());

    flash
	.append("line")
	.attr("class","top-bar")
        .attr("stroke", "black")
        .attr("stroke-width", 4)
        .attr("x1", 0)
        .attr("y1", bknews_top_y())
        .attr("x2", grid_width())
        .attr("y2", bknews_top_y());

    var fl_txt = flash
	.append("g")
	.attr("class","txt-info");


    
}


function translate_bknews_from_csv(d){
    return {
	x_beg: +d.x_beg,
	x_end: +d.x_end,
	y: +d.y,
	fill_col: d.fill_col,
	strk_col: d.strk_col,
	txt: d.txt
    }
}


/*---------------------
  ------- QUOTES ------
  ---------------------*/

function create_quote() {
    vg
	.append("g")
	.attr("class", "quote")
	.append("text");

    show_loader(true);
    $.ajax({
        type: "GET", //rest Type
        dataType: 'text',
        url: url_quote,
        async: true,
        contentType: "text/json",
        success: function(msg) {
            //console.log(msg);

            quote = JSON.parse(msg).quote ;
	    vg.select(".quote").select("text")
		.text(quote);


            show_loader(false);

        },
        error: function(msg) {
            console.log("error");
            show_loader(false);
        }
    });
}



/*----------------------
   ------ COURSES ------
  ----------------------*/


function def_drag() {
    var cur_over = null;
    var sl = null;
    dragListener = d3.drag()
        .on("start", function(c) {
            if (ckbox["edt-mod"].cked && fetch.done) {

                data_slot_grid.forEach(function(sl) {
                    check_cours(c, sl);
                });

                drag.x = 0;
                drag.y = 0;

                drag.sel = d3.select(this);
                dg.node().appendChild(drag.sel.node());


            }
        })
        .on("drag", function(d) {
            if (ckbox["edt-mod"].cked && fetch.done) {
                cur_over = which_slot(drag.x +
				      parseInt(drag.sel.select("rect")
					       .attr("x")),
				      drag.y +
				      parseInt(drag.sel.select("rect")
					       .attr("y")),
				      cours_width(d),
				      cours_height(d));

                if (!is_garbage(cur_over.day,cur_over.slot)) {
                    sl = data_slot_grid.filter(function(c) {
                        return c.day == cur_over.day && c.slot == cur_over.slot;
                    });
                    if (sl != null && sl.length > 0) {
                        if (!sl[0].display) {
                            data_slot_grid.forEach(function(s) {
                                s.display = false;
                            });
                            sl[0].display = true;
                        }
                    }
                } else {
                    data_slot_grid.forEach(function(s) {
                        s.display = false;
                    });
                }
                go_grid(true);

                drag.x += d3.event.dx;
                drag.y += d3.event.dy;
                drag.sel.attr("transform", "translate(" + drag.x + "," + drag.y + ")");
            }
        }).on("end", function(d) {
            if (cur_over != null && ckbox["edt-mod"].cked && fetch.done) {

                mg.node().appendChild(drag.sel.node());

                data_slot_grid.forEach(function(s) {
                    s.display = false;
                });


                if (!is_garbage(cur_over.day,cur_over.slot)) {
                    var ngs = data_slot_grid.filter(function(s) {
                        return s.day == cur_over.day && s.slot == cur_over.slot;
                    })[0];


                    if (ngs.dispo) {
                        add_bouge(d);
                        ////console.log(cours_bouge);
                        d.day = cur_over.day;
                        d.slot = cur_over.slot;
                    } else {
                        ngs.pop = true;
                    }
                } else {
                    d.day = cur_over.day;
                    d.slot = cur_over.slot;
		}

                drag.sel.attr("transform", "translate(0,0)");

                drag.x = 0;
                drag.y = 0;
                drag.sel = null;
                cur_over = null;

                go_grid(true);
                go_courses(true);
            }
        });

}

function check_cours(c2m, grid_slot) {


    grid_slot.dispo = true;
    grid_slot.reason = "";


    if (is_garbage(grid_slot.day, grid_slot.slot)) {
	return ;
    }

    if (c2m.id_cours == -1) {
	grid_slot.dispo = false;
	grid_slot.reason = "Cours fixe";
	return ;
    }

    if (is_free(grid_slot.day, grid_slot.slot, c2m.promo)) {
        grid_slot.dispo = false;
        grid_slot.reason = "CRENEAU NON DISPO POUR " + set_promos[c2m.promo];
        return;
    }


    var cs = cours.filter(function(c) {
        return (c.day == grid_slot.day &&
            c.slot == grid_slot.slot &&
            c.prof == c2m.prof);
    });
    if (cs.length > 0 && cs[0] != c2m) {
        grid_slot.dispo = false;
        grid_slot.reason = "PB PROF OCCUPE";
        return;
    }


    cs = cours.filter(function(c) {
        return (c.day == grid_slot.day &&
            c.slot == grid_slot.slot &&
            (c.group == c2m.group ||
                groups[c2m.promo][c2m.group].ancetres.indexOf(c.group) > -1 ||
                groups[c2m.promo][c2m.group].descendants.indexOf(c.group) > -1) &&
            c.promo == c2m.promo);
    });
    if (cs.length > 0 && cs[0] != c2m) {
        grid_slot.dispo = false;
        grid_slot.reason = "PB GROUPE";
        return;
    }

    if (dispos[c2m.prof] !== undefined &&
        dispos[c2m.prof][grid_slot.day][grid_slot.slot] == 0) {
        grid_slot.dispo = false;
        grid_slot.reason = "PB PROF PAS DISPO";
        return;
    }


}

function which_slot(x, y, w, h) {
    var wday = (rootgp_width * labgp.width +
        dim_dispo.plot *
        (dim_dispo.width + dim_dispo.right));
    var day = Math.floor((x + .5 * w) / wday);
    var hslot = nbRows * labgp.height;
    var slot = Math.floor((y + .5 * h) / hslot);
    return {
        day: day,
        slot: slot
    };
}


function is_garbage(day, hour) {
    return (hour >= nbSl || hour < 0 || day < 0 || day >= nbPer);
}

function is_free(day, hour, promo) {
    return (promo < 2 && (day == 3 && hour > 2));
}



/*--------------------
  ------- TUTORS -----
  --------------------*/

function create_forall_prof() {
    var contg = prg
        .append("g")
        .attr("class", "tutor-button-all")
        .attr("transform", "translate(" + butpr.tlx + "," + butpr.tly + ")")
        .attr("cursor", "pointer")
        .on("click", apply_tutor_display_all);


    contg
        .append("rect")
        .attr("width", butpr.width)
        .attr("height", butpr.height)
        .attr("class", "tutor-button-me")
        .attr("rx", 5)
        .attr("ry", 10)
        .attr("x", 0)
        .attr("y", 0);

    contg
        .append("text")
        .text("\u2200")
        .attr("x", .5 * butpr.width)
        .attr("y", .5 * butpr.height);
}



/*---------------------
  ------- VALIDER -----
  ---------------------*/

function create_val_but() {

    edt_but = vg
        .append("g")
        .attr("but", "edt")
        .on("mouseover", but_bold)
        .on("mouseout", but_back)
        .on("click", confirm_change)
        .attr("cursor", "pointer");

    edt_but
        .append("rect")
        .attr("width", valid.w)
        .attr("height", valid.h)
        .attr("fill", "steelblue")
        .attr("stroke", "black")
        .attr("stroke-width", 2)
        .attr("rx", 10)
        .attr("ry", 10)
        .attr("x", menus.x + menus.mx - 5)
        .attr("y", did.tly);

    edt_but
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "white")
        .text("Valider EdT")
        .attr("x", menus.x + menus.mx + .5 * valid.w)
        .attr("y", did.tly + .5 * valid.h);

    edt_but.attr("visibility", "hidden");


    edt_message = vg
        .append("g")
        .attr("message", "edt");

    edt_message
        .append("rect")
        .attr("width", menus.coled + menus.colcb)
        .attr("height", 30)
        .attr("fill", "white")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1)
        .attr("rx", 10)
        .attr("ry", 10)
        .attr("x", menus.x)
        .attr("y", did.tly + 94);

    edt_message
        .append("g")
        .attr("class", "ack-edt")
        .append("text")
        .attr("x", menus.x + (menus.coled + menus.colcb) * 0.5)
        .attr("y", did.tly + 94 + 15);

    edt_message.attr("visibility", "hidden");

}




/*--------------------
   ------ STYPE ------
  --------------------*/

function create_stype() {
    var t, dat, datdi, datsmi;

    // sometimes, all preferences are not in the database
    // -> by default, not available
    for (var i = 0; i < user.dispos_type.length; i++) {
        if (typeof user.dispos_type[i] == 'undefined') {
            // cf translate_dispos_type_from_csv
            user.dispos_type[i] = create_dispo_default_from_index(i);
        }
    }


    dat = stg.selectAll(".dispot")
        .data(user.dispos_type);

    datdi = dat
        .enter()
        .append("g")
        .attr("class", "dispot")
        .attr("transform", "translate(" +
            did.tlx + "," +
            did.tly + ")");

    var datdisi = datdi
        .append("g")
        .attr("class", "dispot-si");



    datdisi
        .append("rect")
        .attr("class", "dispot-bg")
        .attr("stroke", "#555555")
        .attr("stroke-width", 1)
        .attr("fill", function(d) {
            return smi_fill(d.val / par_dispos.nmax);
        })
        .attr("width", dispot_w)
        .attr("height", dispot_h)
        .attr("x", dispot_x)
        .attr("y", dispot_y)
        .attr("fill", function(d) {
            return smi_fill(d.val / par_dispos.nmax);
        });

    datdisi
        .append("line")
        .attr("stroke", "#555555")
        .attr("stroke-width", 2)
        .attr("x1", 0)
        .attr("y1", gsclbt_y)
        .attr("x2", gsclbt_x)
        .attr("y2", gsclbt_y);

    stg.attr("visibility", "hidden");

    var dis_but = stg
        .append("g")
        .attr("but", "dis")
        .on("mouseover", but_bold)
        .on("mouseout", but_back)
        .on("click", send_dis_change)
        .attr("cursor", "pointer");

    dis_but
        .append("rect")
        .attr("width", valid.w)
        .attr("height", valid.h)
        .attr("fill", "steelblue")
        .attr("stroke", "black")
        .attr("stroke-width", 2)
        .attr("rx", 10)
        .attr("ry", 10)
        .attr("x", did.tlx)
        .attr("y", did.tly);

    dis_but
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "white")
        .text("Valider disponibilités")
        .attr("x", did.tlx + .5 * valid.w)
        .attr("y", did.tly + .5 * valid.h);

    var stap_but = stg
        .append("g")
        .attr("but", "st-ap")
        .on("mouseover", st_but_bold)
        .on("mouseout", st_but_back)
        .on("click", apply_stype)
        .attr("cursor", st_but_ptr);

    stap_but
        .append("rect")
        .attr("width", stbut.w)
        .attr("height", stbut.h + 20)
        .attr("x", dispot_but_x)
        .attr("y", dispot_but_y("app"))
        .attr("rx", 10)
        .attr("ry", 10)
        .attr("fill", "steelblue")
        .attr("stroke", "black")
        .attr("stroke-width", 2);

    stap_but
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "white")
        .attr("x", dispot_but_txt_x)
        .attr("y", dispot_but_txt_y("app"))
        .text("Appliquer");

    stap_but
        .append("text")
        .attr("font-size", 18)
        .attr("fill", "white")
        .attr("x", dispot_but_txt_x)
        .attr("y", dispot_but_txt_y("app") + 20)
        .text("Semaine type");

}



function fetch_dispos_type() {
    if (user.nom != "") {
        show_loader(true);
        $.ajax({
            type: "GET", //rest Type
            dataType: 'text',
            url: url_fetch_stype,
            async: true,
            contentType: "text/csv",
            success: function(msg) {
                user.dispos_type = new Array(nbSl * nbPer);

                d3.csvParse(msg, translate_dispos_type_from_csv);
                create_stype();
                show_loader(false);
            },
            error: function(xhr, error) {
                console.log("error");
                console.log(xhr);
                console.log(error);
                console.log(xhr.responseText);
                show_loader(false);
                // window.location.href = url_login;
                //window.location.replace(url_login+"?next="+url_stype);
            }
        });
    }
}


function translate_dispos_type_from_csv(d) {
    var d2p = {
        day: +d.jour,
        hour: +d.heure,
        val: +d.valeur,
        off: -1
    };
    user.dispos_type[day_hour_2_1D(d2p)] = d2p;
}

function create_dispo_default_from_index(ind) {
    return {
        day: Math.floor(ind / nbSl),
        hour: ind % nbSl,
        val: 0,
        off: -1
    };
}





