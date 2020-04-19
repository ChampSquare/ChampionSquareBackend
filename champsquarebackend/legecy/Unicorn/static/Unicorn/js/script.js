 $(document).ready(function () {
            $('marquee').marquee().mouseover(function () {
                $(this).trigger('stop');
            }).mouseout(function () {
                $(this).trigger('start');
            });
            var owl = $('#clients-slider');
            owl.owlCarousel({
                items: 3, //10 items above 1000px browser width
                itemsDesktop: [1000, 5], //5 items between 1000px and 901px
                itemsDesktopSmall: [900, 3], // betweem 900px and 601px
                itemsTablet: [600, 2], //2 items between 600 and 0
                itemsMobile: false, // itemsMobile disabled - inherit from itemsTablet option
                autoPlay: true
            });
            $('#clients-slider').magnificPopup({ delegate: 'img', type: 'image', gallery: { enabled: true } });
        });


        $(document).ready(function () {
            $('marquee').marquee().mouseover(function () {
                $(this).trigger('stop');
            }).mouseout(function () {
                $(this).trigger('start');
            });
            var owl = $('#clients-slider-tpc');
            owl.owlCarousel({
                items: 3, //10 items above 1000px browser width
                itemsDesktop: [1000, 5], //5 items between 1000px and 901px
                itemsDesktopSmall: [900, 3], // betweem 900px and 601px
                itemsTablet: [600, 2], //2 items between 600 and 0
                itemsMobile: false, // itemsMobile disabled - inherit from itemsTablet option
                autoPlay: true
            });
            $('#clients-slider-tpc').magnificPopup({ delegate: 'img', type: 'image', gallery: { enabled: true } });
        });