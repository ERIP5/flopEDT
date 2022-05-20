/*
a=document.getElementById("id_bm_x_choice")
a.hidden=true
a.hidden=false
a.parentElement.hidden=true

laisser hidden le select periodicity



hide le 2eme formulaire
if has_periodicity == true
    show : start_time, duration, periodicity

    if by week


    if each month


    if by month
*/
var truck = 3

function first_hide() {
    document.getElementById("id_periodicity_type").parentElement.hidden=true
}

function mainHide() {
    first_hide()
}
