var map;

function initMap() {
    const lat = parseFloat(document.getElementById('lat').value);
    const lng = parseFloat(document.getElementById('lng').value);

    map = new google.maps.Map(document.getElementById('map'),
    {
        center: {lat: lat, lng: lng},
        zoom: 13,
    });

}