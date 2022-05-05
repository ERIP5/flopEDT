document.onclick = hideMenu;
document.oncontextmenu = rightClick;

function hideMenu() {
			document.getElementById("contextMenu").style.visibility = "hidden"
			//console.log("hide")
		}

function rightClick(e) {
    e.preventDefault()

    if (document.getElementById("contextMenu").style.visibility == 'visible') {
        console.log("if")
        hideMenu();
        }

    else {
        var menu = document.createElement("contextMenu")
        menu.id = "contextMenu"

        menu.style.visibility = 'visible';
        menu.style.left = e.pageX + "px";
        menu.style.top = e.pageY + "px";

        menu.onmouseleave = () => contextMenu.outerHTML = ''

        menu.innerHTML = "<p onclick='console.log(`edit`)'>edit</p><p onclick='console.log(`change room`)'>change room</p>"
        document.body.appendChild(menu)
    }
}
