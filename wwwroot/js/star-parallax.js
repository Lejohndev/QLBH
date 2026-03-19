// Star Parallax Effect
document.addEventListener('DOMContentLoaded', function() {
    let scrollTimeout;
    const body = document.body;

    window.addEventListener('scroll', function() {
        // Lấy vị trí scroll hiện tại
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;
        
        // Tính toán parallax offset cho các lớp khác nhau
        // Layer 1 (glow): chuyển động chậm nhất
        const offset1 = scrollY * 0.02;
        
        // Layer 2-6: chuyển động ở tốc độ khác nhau
        const offset2 = scrollY * 0.03;
        const offset3 = scrollY * 0.025;
        const offset4 = scrollY * 0.035;
        const offset5 = scrollY * 0.028;
        const offset6 = scrollY * 0.032;
        
        // Layer 7-11: chuyển động chậm
        const offset7 = scrollY * 0.018;
        const offset8 = scrollY * 0.022;
        const offset9 = scrollY * 0.02;
        const offset10 = scrollY * 0.024;
        const offset11 = scrollY * 0.019;
        
        // Layer 12-13 (sao mông mộ): chuyển động rất chậm
        const offset12 = scrollY * 0.005;
        const offset13 = scrollY * 0.01;
        
        // Cập nhật background-position
        body.style.backgroundPosition = 
            `0 0, 0% ${-offset1}%, 0% ${-offset2}%, 0% ${-offset3}%, 0% ${-offset4}%, 0% ${-offset5}%, 0% ${-offset6}%, 0% ${-offset7}%, 0% ${-offset8}%, 0% ${-offset9}%, 0% ${-offset10}%, ${-offset12}px ${-offset12}px, ${-offset13}px ${-offset13}px`;
        
        // Xóa class scrolling cũ
        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }
        body.classList.add('scrolling');
        
        // Thêm lại class scrolling sau khi stop scroll
        scrollTimeout = setTimeout(function() {
            body.classList.remove('scrolling');
        }, 100);
    });
    
    // Hiệu ứng twinkling random cho các sao
    const stars = document.querySelectorAll('[data-star]');
    if (stars.length === 0) {
        // Tạo random twinkling cho toàn bộ background
        setInterval(function() {
            // Có thể thêm các hiệu ứng khác ở đây
        }, 3000);
    }
});
