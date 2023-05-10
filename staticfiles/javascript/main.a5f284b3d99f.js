google.maps.event.addDomListener(window, "load", function(){

    const ubicacion = new Localizacion(()=>{
        const myLatIng = { lat: ubicacion.latitude, lng: ubicacion.longitude };

        const options = {
            center: myLatIng,
            zoom: 14
        }

        var map = document.getElementById('map');

        const mapa = new google.maps.Map(map, options);

        const marcador = new google.maps.Marker({
            position: myLatIng,
            map: mapa,
        });

        var informacion = new google.maps.InfoWindow();

        marcador.addListener('click', function(e){
            informacion.open(mapa, marcador);
        });

        var Lat = document.getElementById('Lat');
        var Lng = document.getElementById('Lng');

        Lat.value = myLatIng.lat;
        Lng.value = myLatIng.lng;

        var autocomplete = document.getElementById('autocomplete');

        const search = new google.maps.places.Autocomplete(autocomplete);
        search.bindTo("bounds", mapa);

        search.addListener("place_changed", function(e){
            informacion.close();
            marcador.setVisible(false);

            var place = search.getPlace();

            if (!place.geometry.viewport){
                alert("Error al mostrar el lugar");
                return;
            }

            if (place.geometry.viewport){
                mapa.fitBounds(place.geometry.viewport);
            }else{
                mapa.setCenter(place.geometry.location);
                mapa.setZoom(18)
            };

            marcador.setPosition(place.geometry.location);
            marcador.setVisible(true);

            var address = "";

            autocomplete.value = place.formatted_address;
            Lat.value = place.geometry.location.lat();
            Lng.value = place.geometry.location.lng();
        });

    });
});