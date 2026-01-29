// Promotional Carousel Script
function scrollCarousel(direction) {
    const carousel = document.getElementById('promoCarousel');
    if (!carousel) return;

    const scrollAmount = 320; // Width of one card + gap
    
    if (direction === -1) {
        // Scroll left
        carousel.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    } else if (direction === 1) {
        // Scroll right
        carousel.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    }
}

// Keyboard navigation
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('promoCarousel');
    if (!carousel) return;

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            scrollCarousel(-1);
        } else if (e.key === 'ArrowRight') {
            scrollCarousel(1);
        }
    });

    // Touch/Swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    carousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    carousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);

    function handleSwipe() {
        if (touchStartX - touchEndX > 50) {
            // Swiped left - scroll right
            scrollCarousel(1);
        } else if (touchEndX - touchStartX > 50) {
            // Swiped right - scroll left
            scrollCarousel(-1);
        }
    }
});
