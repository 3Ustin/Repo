
var id = null;
function myMove() {
  var elem = document.getElementById("charIcon");   
  var pos = 0;
  clearInterval(id);
  id = setInterval(frame, 14);
  function frame() {
    if (pos == 140) {
    clearInterval(id);
    } else {
    pos++; 
    elem.style.bottom = pos + "px"; 
    elem.style.left = pos + "px"; 
    }
  }
}

function open_combat() {
  inv_menu = document.getElementById("combat_menu");
  inv_menu.style.removeProperty("display");
  inv_menu.style.display = "block";
}

function close_combat() {
  inv_menu = document.getElementById("combat_menu");
  inv_menu.style.removeProperty("display");
  inv_menu.style.display = "none";
}