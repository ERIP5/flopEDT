/****************
****variables****
****************/

nb_filter = 0;

/****************
*****Selects*****
****************/

function displayMenutext(id, text) {
    var select = document.getElementById(id);
    var CreateText = document.createElement("p")
    CreateText.innerText = text
    select.appendChild(CreateText)
}

function displaySelectRoom() {
    select = document.getElementById("selectRoom");
    for (room in allRoom) {
        var textC = allRoom[room].name;
        CreateElem = document.createElement("option");
        CreateElem.textContent = textC;
        CreateElem.value = textC;
        select.appendChild(CreateElem);
    }
}



function displayAllFilters() {
    select = document.getElementById("selectfilter");
    for (fil in allAttributes) {
        CreateElem = document.createElement("option");
        CreateElem.textContent = allAttributes[fil].name;
        CreateElem.value = allAttributes[fil].id;
        select.appendChild(CreateElem);
    }
}


function hidefilters() {
    var element = document.getElementById("filters").style.display = "none";
}

function showfilters() {
    var element = document.getElementById("filters").style.display = "block";
}


function addFilter(filter) {
    if(filter.value != "---") {
        select = document.getElementById("filterAct")

        buttonSuppr(select, filter[filter.selectedIndex].textContent)

        removeAddFilterOption("remove", filter)

        document.getElementById("selectfilter").selectedIndex = 0;
    }
}

function removeAddFilterOption(adr, object) {
    if(adr == "add") {
        var optionAdd = object.parentNode.id.split('-')
        CreateElem = document.createElement("option");
        CreateElem.textContent = optionAdd[0];
        CreateElem.value = optionAdd[1];
        document.getElementById('selectfilter').appendChild(CreateElem);
    }

    if(adr == "remove") {
        for (i = 0; i<object.length; i++) {
            if(object[i].value == object.value) {
                object.remove(i)
            }
        }
    }
}


function buttonSuppr(parent, text) {
    elemp = document.createElement("input")
    elemp.type = "button"
    elemp.value = text+" x"
    elemp.id = "suppr"+nb_filter;
    nb_filter+=1;
    elemp.onclick = supprFilter
    parent.appendChild(elemp)
}

function supprFilter(supr) {
    parent = supr.explicitOriginalTarget.parentNode
    delete filter_list[parent.id.split('-')[0]]
    removeAddFilterOption("add", supr.explicitOriginalTarget)
    parent.remove();
    rmv_reservT();
    mainT();
}

/************
**functions**
************/

function rmv_total() {
    if (rmvStatut == 1) {
         rmv_reservT()
    }

    if (rmvStatut == 2) {
         rmv_reservS()
    }
}

function getRoom() {
    var valRoom = document.getElementById("selectRoom").value;
    liste(valRoom)
}

function liste(room) {
    if (room == "all") {
         rmv_total()
         rmvStatut = 1
         showfilters()
         mainT()
    }

    if (room != "all") {
         rmv_total()
         rmvStatut = 2
         current_room = room
         hidefilters()
         mainS()
    }
}


function addFilterChange(filter) {
    filter_list[filter.explicitOriginalTarget.id] = filter.explicitOriginalTarget.value
    rmv_total();
    mainT();
}

function addFilterNumberMinChange(filter) {
    filter_list[filter.explicitOriginalTarget.id].min = filter.explicitOriginalTarget.value
    rmv_total();
    mainT();
}
function addFilterNumberMaxChange(filter) {
    filter_list[filter.explicitOriginalTarget.id].max = filter.explicitOriginalTarget.value
    rmv_total();
    mainT();
}

function displayFilters() {
        displaySelectRoom()
        displayAllFilters()
}

function mainMenu() {
    rmvStatut = 1
    valFilter = "aucun"
    displayFilters()
    mainT()
}

// execute the main
mainMenu()
