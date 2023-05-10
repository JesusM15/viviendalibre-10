const btn = document.getElementById('btn-filters');
const sidebar = document.getElementById('sidebar_filters');
console.log(sidebar)

btn.addEventListener('click', function(e){
    console.log('click')
    sidebar.classList.toggle('hide')
});