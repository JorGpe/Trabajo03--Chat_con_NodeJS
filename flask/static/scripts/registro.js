var ro = document.querySelector(":root");
window.addEventListener("load", startup, false);
var color = sessionStorage.getItem('colorf');
console.log(color);
console.log("Hola");

function startup() {
    ro.style.setProperty('--color-f',sessionStorage.getItem('colorf'));
}