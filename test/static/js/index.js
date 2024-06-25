let navBtn = document.getElementById('navBtn');
let dropdown = document.getElementById('dropdown');
let dropdownMenu = document.getElementById('dropdownMenu');

navBtn.addEventListener('click', (event) => {
    dropdown.style.display = 'block';
})

dropdown.addEventListener('click', (event) => {
    dropdown.style.display = 'none';
})

dropdownMenu.addEventListener('click', (event) => {
    event.stopPropagation();
})