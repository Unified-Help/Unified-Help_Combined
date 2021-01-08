function openNav() {
document.getElementById("mySidenav").style.width = "16.875em";
document.getElementById("main").style.marginLeft = "16.875em";
document.getElementById("Main").style.marginLeft = "17.5em";
}

function closeNav() {
document.getElementById("mySidenav").style.width = "0";
document.getElementById("main").style.marginLeft = "0";
document.getElementById("Main").style.marginLeft = "0.8em";
}

var timesClicked = 0;

$("#sidebarToggle").click(function() {
timesClicked++;

if (timesClicked%2==0) {
  closeNav()
} else {
  openNav()
}

})
