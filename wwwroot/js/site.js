document.addEventListener("DOMContentLoaded", function () {
    const logo = document.querySelector('.logo');

    // Thay đổi kích thước logo khi cuộn trang
    window.addEventListener('scroll', function () {
        if (window.scrollY < 50) {
            logo.classList.add('zoom');
        } else {
            logo.classList.remove('zoom');
        }
    });
});