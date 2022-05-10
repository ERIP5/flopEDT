/****************
****variables****
****************/

nb_filter = 0;


/****************
*****Selects*****
****************/

function displayMenutext(id, text)
{
var select = document.getElementById(id);
var CreateText = document.createElement("p")
CreateText.innerText = text
select.appendChild(CreateText)
}

function displaySelectRoom(){

select = document.getElementById("selectRoom");

for (var i = 0; i < rooms.length; i++) {
  var textC = rooms[i].name;
  CreateElem = document.createElement("option");
  CreateElem.textContent = textC;
  CreateElem.value = textC;
  select.appendChild(CreateElem);
}

}



function displayAllFilters(){

select = document.getElementById("selectfilter");
for (fil of filtersList) {
  CreateElem = document.createElement("option");
  CreateElem.textContent = fil;
  CreateElem.value = fil;
  select.appendChild(CreateElem);
}
}


function hidefilters()
{
var element = document.getElementById("filters").style.display = "none";
}

function showfilters()
{
var element = document.getElementById("filters").style.display = "block";
}


function addFilter(filtre)
{
    if(filtre.value != "---"){
    select = document.getElementById("filterAct")
    elemg = document.createElement("g")
    elemg.id= filtre.value
    select.appendChild(elemg)

    elemp = document.createElement("p")
    elemp.innerText = "filtre : " + filtre.value
    elemg.appendChild(elemp)

    generateSelect(elemg, filtre.value)

    removeAddFilterOption("remove", filtre)

    document.getElementById("selectfilter").selectedIndex = 0;

    }
}

function removeAddFilterOption(adr, object)
{
    if(adr == "add")
    {
    var textC = object.parentNode.id;
        CreateElem = document.createElement("option");
        CreateElem.textContent = textC;
        CreateElem.value = textC;
        document.getElementById('selectfilter').appendChild(CreateElem);
    }

    if(adr == "remove")
    {
        for (i = 0; i<object.length; i++)
        {
            if(object[i].value == object.value)
            {
            object.remove(i)
            }
        }
    }
}

function generateSelect(parent, dataName)
{
    switch (dataName) {
        case "type" :

            elemp = document.createElement("p")
            elemp.innerText = "Choisir un type de salle : "
            parent.appendChild(elemp)

            elemS = document.createElement("select")
            elemS.id = "selectType"
            elemS.onchange = changeRoomType
            parent.appendChild(elemS)

            elemO = document.createElement("option")
                elemO.value = "all"
                elemO.textContent = "all"
                elemS.appendChild(elemO)

            for (el of typeRoom){
                elemO = document.createElement("option")
                elemO.value = el
                elemO.textContent = el
                elemS.appendChild(elemO)
            }
            break;
        case "projector" :
            elemp = document.createElement("p")
            elemp.innerText = "Salle avec projecteur ? "
            parent.appendChild(elemp)

            elemS = document.createElement("select")
            elemS.id = "selectProjo"
            elemS.onchange = changeRoomProjo
            parent.appendChild(elemS)

            elemO = document.createElement("option")
                elemO.value = "all"
                elemO.textContent = "all"
                elemS.appendChild(elemO)

            for (el of truefalse){
                elemO = document.createElement("option")
                elemO.ngValue = el
                elemO.textContent = el
                elemS.appendChild(elemO)
            }
            break;

            case "computer" :
            elemp = document.createElement("p")
            elemp.innerText = "Salle avec ordinateur ? "
            parent.appendChild(elemp)

            elemS = document.createElement("select")
            elemS.id = "selectComputer"
            elemS.onchange = changeRoomComputer
            parent.appendChild(elemS)

            elemO = document.createElement("option")
                elemO.value = "all"
                elemO.textContent = "all"
                elemS.appendChild(elemO)

            for (el of truefalse){
                elemO = document.createElement("option")
                elemO.ngValue = el
                elemO.textContent = el
                elemS.appendChild(elemO)
            }
            break;
    }

    buttonSuppr(parent)
}

function buttonSuppr(parent)
{
    elemp = document.createElement("input")
    elemp.type = "button"
    elemp.value = "supprimer filtre"
    elemp.id = "suppr"+nb_filter;
    nb_filter+=1;
    elemp.onclick = supprFilter
    parent.appendChild(elemp)
}

function supprFilter(supr)
{
    parent = supr.explicitOriginalTarget.parentNode
    switch (parent.id) {
        case "type" :
            f_room_type = "all";
            break;
        case "projector" :
            room_projo = "all";
            break;
        case "computer" :
            room_computer = "all";
            break;
    }
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

function changeRoomType(){
    f_room_type = document.getElementById("selectType").value;
    rmv_total();
    mainT();
}

function changeRoomProjo(){
    room_projo = document.getElementById("selectProjo").value;
    rmv_total();
    mainT();
}

function changeRoomComputer(){
    room_computer = document.getElementById("selectComputer").value;
    console.log(room_computer)
    rmv_total();
    mainT();
}

function displayFilters(){
        displaySelectRoom()
        displayAllFilters()
}

function mainMenu(){
    rmvStatut = 1
    valFilter = "aucun"
    displayFilters()
    mainT()
}

mainMenu()
