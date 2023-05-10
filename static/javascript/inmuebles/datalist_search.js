var search_ubicacion = document.getElementById('search_ubicacion');
var option;
alert('ola')

search_ubicacion.oninput = function(e){
    option = document.getElementById(`ubi${search_ubicacion.value}`);
    console.log(option.innerHTML);
    console.log('hola')
};