var search_ubicacion = document.getElementById('search_ubicacion');
var ubi = document.getElementById('ubicacion_id');
var option;

search_ubicacion.oninput = function(e){
    option = document.getElementById(`ubi${search_ubicacion.value}`);
    ubi.value = search_ubicacion.value;
    search_ubicacion.value = option.textContent;
};