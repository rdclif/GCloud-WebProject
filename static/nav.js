//jquery for nav bar function
$(document).ready(function() {
    //loading larger screens
    if($( window ).width() >= "600") {
        $('.narrow-hide').css("display", "block");
        $('.hamburger').hide();
        $('#banner-pic').addClass('banner-top-lrg');
    }

    //for loading very small screens
    if($( window ).width() <= "350") {
        $('.hamburger').hide();
        $(".slide-nav").slideToggle("medium");
    }

    //click function for hamburger
    $('.hamburger').click(function () {
        $('.hamburger').toggleClass("change");
        $(".slide-nav").slideToggle("medium");
    });

    $("#navToggle a").click(function(e){
        e.preventDefault();
        $(".slide-nav").slideToggle("medium");
    });

    //adjust for window resizing
    $(window).resize(function() {
        //for larger screens
        if($( window ).width() >= "600") {
            $('.narrow-hide').css("display", "block");
            $('.hamburger').hide();
            $('.slide-nav').slideUp("medium");
            if($('.hamburger').hasClass("change")){
                $('.hamburger').removeClass("change");
            }
            if ($('#tpBttn').is(":visible")) {
                $('#tpBttn').fadeOut("medium");
            }

        }
        //for very small screens
        else if($( window ).width() <= "350"){
            $('.hamburger').hide();
            $(".slide-nav").slideDown("medium");
        }
        else {
            $('.narrow-hide').css("display", "none");
            $(".slide-nav").slideUp("medium");
            $('.hamburger').show();
            if($('.hamburger').hasClass("change")){
                $('.hamburger').removeClass("change");
            }
        }
    });

    //check scroll for top button
    $(window).scroll(function(){
        if($( window ).width() < "600") {
            if ($(this).scrollTop() > 100) {
                $('#tpBttn').fadeIn("medium");
            } else {
                $('#tpBttn').fadeOut("medium");
            }
        }
    });

    //window scroll function for top button
    $('#tpBttn').click(function(event) {
        event.preventDefault();
        $("html, body").animate({scrollTop: 0}, "medium");
        return false;
    });
});