$(".animated").addClass("delay-1s");

$('.number').appear(function() {
    $('.number').countTo();
});


import counterUp from 'counterup2'

const el = document.querySelector( '.counter' )

// Start counting, do this on DOM ready or with Waypoints.
counterUp( el, {
    duration: 1000,
    delay: 10,
} )



