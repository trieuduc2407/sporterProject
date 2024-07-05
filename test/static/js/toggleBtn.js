let navBtn = document.getElementById('navBtn');
let dropdown = document.getElementById('dropdown');
let dropdownMenu = document.getElementById('dropdownMenu');

let searchBtn = document.getElementById('searchBtn');
let searchForm = document.getElementById('searchForm');
let searchText = document.getElementById('searchText')

searchBtn.addEventListener('click', () => {
    searchForm.style.display = 'block'
})

searchForm.addEventListener('click', () => {
    searchForm.style.display = 'none'
})

searchText.addEventListener('click', (event) => {
    event.stopPropagation()
})

navBtn.addEventListener('click', () => {
    dropdown.style.display = 'block';
})

dropdown.addEventListener('click', () => {
    dropdown.style.display = 'none';
})

dropdownMenu.addEventListener('click', (event) => {
    event.stopPropagation();
})


