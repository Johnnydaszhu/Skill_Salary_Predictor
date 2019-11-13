// ---------------------------------------
// Custom JS
// ---------------------------------------

// Preloader
$(window).load(function(){
    $('.preloader').fadeOut(1000); // set duration in brackets    
});

// Init Fastclick
$(function() {
    FastClick.attach(document.body);
});

// -----------------------------
//  Smooth scroll
// ----------------------------
$(document).ready(function() {
    $('.navbar-nav li a, .banner a').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// -----------------------------
//  CSS3 Transition
// -----------------------------
$('*').each(function(){
	if($(this).attr('data-animation')) {
		var $animationName = $(this).attr('data-animation'),
			$animationDelay = "delay-"+$(this).attr('data-animation-delay');
		$(this).appear(function() {
			$(this).addClass('animated').addClass($animationName);
			$(this).addClass('animated').addClass($animationDelay);
		});
	}
});



// -----------------------------
// Isotope filtering
// -----------------------------
$(function(){
    var $container = $('.isotope');
    // init
    $container.imagesLoaded( function() {
        $container.isotope({ 
            itemSelector: ".item",
            masonry: {
                columnWidth: ".grid-sizer",
                gutter: ".gutter-sizer"
            }
        });
    });
    // filter items when filter link is clicked
    $('#filter a').click(function(){
        var selector = $(this).attr('data-filter');
        $container.isotope({ filter: selector });
        return false;
    });
});




// -----------------------------
// Count To
// -----------------------------
$('.number').appear(function() {
    $('.number').countTo();
});




// -----------------------------
// Easy Pie Chart
// -----------------------------
$('.chart').appear(function() {
    $('.chart').easyPieChart({
        barColor: "#fff",//default, set optionaly in html data-bar-color option
        trackColor: "transparent",
        //scaleColor: "#CCC",
        scaleLength: 0,
        lineCap: "square",
        lineWidth: 5,
        animate: 2000,
        onStart: function() {
            $('.percent').countTo({
                speed: 2000
            });
        }
    });
});

jQuery(function($) {
    $("select[multiple]").bsmSelect();
});