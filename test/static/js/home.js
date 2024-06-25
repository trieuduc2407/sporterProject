// document.addEventListener('DOMContentLoaded', function(){
//     const searchIcon = document.getElementById('searchicon'); // Đổi 'fa-magnifying-glass' thành 'searchicon'
//     const searchForm = document.getElementById('search-form'); // Đổi 'searchform' thành 'search-form'
//
//     searchIcon.addEventListener('click', function(){
//         if(searchForm.style.display === 'block' || searchForm.style.display === ''){
//             searchForm.style.display = 'none';
//         }else{
//             searchForm.style.display = 'block';
//         }
//     });
//
//     document.addEventListener('click', function(event){
//         if(event.target !== searchIcon && !searchForm.contains(event.target)){
//             searchForm.style.display = 'none';
//         }
//     });
// });
// Lấy các phần tử cần thiết từ DOM
const searchIcon = document.getElementById('searchicon');
const overlay = document.getElementById('overlay');
const searchContainer = document.getElementById('search-container');

// Sự kiện click vào biểu tượng tìm kiếm
searchIcon.addEventListener('click', function() {
    overlay.classList.add('show'); // Hiển thị lớp nền đen mờ
    searchContainer.classList.add('show'); // Hiển thị search container
});

// Đóng search container khi click vào overlay (lớp nền đen mờ)
overlay.addEventListener('click', function() {
    overlay.classList.remove('show'); // Ẩn lớp nền đen mờ
    searchContainer.classList.remove('show'); // Ẩn search container
});


//dropdown menu
$(document).ready(function() {
    $('.toggle-btn').click(function() {
        $('.dropdown-menu').toggleClass('dropdown-active');
        // Tính toán lại vị trí top cho dropdown-menu
        var menuHeight = $('.dropdown-menu').outerHeight();
        var windowHeight = $(window).height();
        var scrollTop = $(window).scrollTop();
        var topPosition = scrollTop + (windowHeight - menuHeight) / 2;
        $('.dropdown-menu').css('top', topPosition + 'px');
    });

    // Đóng dropdown menu nếu nhấp bên ngoài
    $(document).click(function(e) {
        if (!$(e.target).closest('.toggle-btn').length && !$(e.target).closest('.dropdown-menu').length) {
            $('.dropdown-menu').removeClass('dropdown-active');
        }
    });
});

function toggleDropdownMenu() {
    var dropdownMenu = document.querySelector('.dropdown-menu');
    dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
}

