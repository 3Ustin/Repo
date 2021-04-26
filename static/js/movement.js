
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
