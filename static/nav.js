$(document).ready(function() {
    if($( window ).width() >= "600") {
        $('.narrow-hide').css("display", "block");
        $('.hamburger').hide();
        $('#banner-pic').addClass('banner-top-lrg')

    }

    $('.hamburger').click(function () {
        $('.hamburger').toggleClass("change");
        $(".slide-nav").slideToggle("medium");
    });

    $("#navToggle a").click(function(e){
        e.preventDefault();
        $(".slide-nav").slideToggle("medium");
    });

    $(window).resize(function() {
        if($( window ).width() >= "600") {
            $('.narrow-hide').css("display", "block");
            $('.hamburger').hide();
            $(".slide-nav").slideUp("medium");
            if($('.hamburger').hasClass("change")){
                $('.hamburger').removeClass("change");
            }

        }
        else {
            $('.narrow-hide').css("display", "none");
            $('.hamburger').show();
        }
    });

});