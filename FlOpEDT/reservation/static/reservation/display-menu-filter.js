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
        elemg = document.createElement("g")
        elemg.id = filter[filter.selectedIndex].textContent + "-" + filter[filter.selectedIndex].value
        select.appendChild(elemg)

        elemp = document.createElement("p")
        elemp.innerText = "filter by : " + filter[filter.selectedIndex].textContent
        elemg.appendChild(elemp)

        generateSelect(elemg, filter.value)

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

function generateSelect(parent, idAttribute) {
    switch (allAttributes[idAttribute].attribute_type) {

        case "B" :
            elemS = document.createElement("select")
            elemS.id = allAttributes[idAttribute].name
            elemS.onchange = addFilterChange
            parent.appendChild(elemS)

            elemO = document.createElement("option")
                elemO.value = "all"
                elemO.textContent = "all"
                elemS.appendChild(elemO)

            for (el of truefalse) {
                elemO = document.createElement("option")
                elemO.value = el
                elemO.textContent = el
                elemS.appendChild(elemO)
            }
            break;

        case "A" :
            elemS = document.createElement("select")
            elemS.id = allAttributes[idAttribute].name
            elemS.onchange = addFilterChange
            parent.appendChild(elemS)

            elemO = document.createElement("option")
                elemO.value = "all"
                elemO.textContent = "all"
                elemS.appendChild(elemO)

            for (el of allAttributes[idAttribute].array_values) {
                elemO = document.createElement("option")
                elemO.ngValue = el
                elemO.textContent = el
                elemS.appendChild(elemO)
            }
            break;

        case "N" :
            elemp = document.createElement("input")
            elemp.id = allAttributes[idAttribute].name
            elemp.type = "text"
            elemp.oninput = addFilterChange
            parent.appendChild(elemp)

            break;
    }
    buttonSuppr(parent)
}

function buttonSuppr(parent) {
    elemp = document.createElement("input")
    elemp.type = "button"
    elemp.value = "supprimer filtre"
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
