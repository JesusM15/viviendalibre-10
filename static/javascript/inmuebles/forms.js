var form_search = document.getElementById('form-search-bar');
var filter_form = document.getElementById('filter-form');
var search_bar = document.getElementById('default-search');
var operacion = document.getElementsByName('operacion');
var mRange = document.getElementById('min_range');
var maRange = document.getElementById('max_range');
var inmueble = document.getElementById('tipo');
const csrftoken = Cookies.get('csrftoken'); 

const form_submit = (e) =>{
    const base_url = 'https://viviendalibre.up.railway.app/';
    var operacion = '', tipo = '', ordenar = '-precio', search_s = '', min_range = '0', max_range='9223372036854775806'; 
     
    for(let i=0; i< filter_form.elements.length; i++){
        if (filter_form.elements[i].checked == true){ 
            switch(filter_form.elements[i].name){
                case "operacion":
                    operacion = filter_form.elements[i].value;
                break
                case "tipo":
                    tipo = filter_form.elements[i].value;
                break
                case "list-radio":
                    ordenar = filter_form.elements[i].value;
                break;
                case "min_range":
                    if (filter_form.elements[i].value != ''){
                        min_range = filter_form.elements[i].value;
                    }
                break;
                case "max_range":
                    if (filter_form.elements[i].value != ''){
                        max_range = filter_form.elements[i].value;
                    }
                break;
            default:
                break;
            };
        };
    };

    if(search_bar.value != null || search_bar.value != ' ' || search_bar != '') { search = search_bar.value };
    const url = base_url + `filtrado` + `?search=${search}&operacion=${operacion}&tipo=${tipo}&ordenar=${ordenar}&min_range=${min_range}&max_range${max_range}`;

    window.location.href = url; 
    

};