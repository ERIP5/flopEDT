function errorHide() {
    document.getElementsByClassName("errorlist")

}

function mainHide() {
    // must be hidden
    document.getElementById("id_periodicity").parentElement.hidden=true

    // hide all at the start
    document.getElementById("id_periodicity_type").parentElement.hidden=true
    document.getElementById("id_start").parentElement.hidden=true
    document.getElementById("id_end").parentElement.hidden=true
    document.getElementById("id_bw_weekdays").parentElement.hidden=true
    document.getElementById("id_bw_weeks_nb").parentElement.hidden=true
    document.getElementById("id_bm_x_choice").parentElement.hidden=true
    document.getElementById("id_bm_y_choice").parentElement.hidden=true

    // has_periodicity checked = true
    if (document.getElementById("id_has_periodicity").checked == true){
        document.getElementById("id_periodicity_type").parentElement.hidden=false
        document.getElementById("id_start").parentElement.hidden=false
        document.getElementById("id_end").parentElement.hidden=false
    }

    // By week
    if (document.getElementById("id_periodicity_type").value == "BW") {
        document.getElementById("id_bm_x_choice").parentElement.hidden=true
        document.getElementById("id_bm_y_choice").parentElement.hidden=true
        document.getElementById("id_bw_weekdays").parentElement.hidden=false
        document.getElementById("id_bw_weeks_nb").parentElement.hidden=false
    }

    // Each month at the same date
    if (document.getElementById("id_periodicity_type").value == "EM") {
        document.getElementById("id_bw_weekdays").parentElement.hidden=true
        document.getElementById("id_bw_weeks_nb").parentElement.hidden=true
        document.getElementById("id_bm_x_choice").parentElement.hidden=true
        document.getElementById("id_bm_y_choice").parentElement.hidden=true
    }

    // By month
    if (document.getElementById("id_periodicity_type").value == "BM") {
        document.getElementById("id_bw_weekdays").parentElement.hidden=true
        document.getElementById("id_bw_weeks_nb").parentElement.hidden=true
        document.getElementById("id_bm_x_choice").parentElement.hidden=false
        document.getElementById("id_bm_y_choice").parentElement.hidden=false
    }

    // has_periodicity checked = false
    if (document.getElementById("id_has_periodicity").checked == false){
        document.getElementById("id_periodicity_type").parentElement.hidden=true
        document.getElementById("id_start").parentElement.hidden=true
        document.getElementById("id_end").parentElement.hidden=true
        document.getElementById("id_bw_weekdays").parentElement.hidden=true
        document.getElementById("id_bw_weeks_nb").parentElement.hidden=true
        document.getElementById("id_bm_x_choice").parentElement.hidden=true
        document.getElementById("id_bm_y_choice").parentElement.hidden=true
    }
}
