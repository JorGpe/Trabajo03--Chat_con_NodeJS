var muestrario;
var colorPredeterminado = "#FFFFFF";
var r = document.querySelector(":root");

window.addEventListener("load", startup, false);

function startup() {
    muestrario = document.querySelector("#color_fav");
    muestrario.value = colorPredeterminado;
    muestrario.addEventListener("input", actualizarPrimero, false);
    muestrario.select();
}

function actualizarPrimero(event) {
    sessionStorage.setItem('colorf', event.target.value);
    r.style.setProperty('--color-fav',sessionStorage.getItem('colorf'));
}
  

