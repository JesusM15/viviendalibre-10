var valor_total = document.getElementById('valor_total');
var porcentaje_valor = document.getElementById('porcentaje_valor');
var prestamo_valor = document.getElementById('prestamo_valor');
var prestamo_porcentaje = document.getElementById('prestamo_porcentaje');
var tasa_valor = document.getElementById('tasa_valor');
var tasa_porcentaje = document.getElementById('tasa_porcentaje');


porcentaje_valor.onchange = function(e){
    if(valor_total.value != ''){
        prestamo_porcentaje.innerHTML = `${porcentaje_valor.value}%`;
        prestamo = (porcentaje_valor.value/100) * parseInt(valor_total.value);
        prestamo_valor.innerHTML = `$${Math.round(prestamo)}`;
    }else{
        alert('Favor de primero colocar el valor de la propiedad');
        porcentaje_valor.value = 50;
    }
};

tasa_porcentaje.onchange = function(e){
    tasa_valor.innerHTML = `${tasa_porcentaje.value}%`;
};