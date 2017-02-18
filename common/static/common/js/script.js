navigator.sayswho = (function(){
    var ua=  navigator.userAgent, tem,
        M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*([\d\.]+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=  /\brv[ :]+(\d+(\.\d+)?)/g.exec(ua) || [];
        return 'IE '+(tem[1] || '');
    }
    M= M[2]? [M[1], M[2]]:[navigator.appName, navigator.appVersion, '-?'];
    if((tem= ua.match(/version\/([\.\d]+)/i))!= null) M[2]= tem[1];
    return M.join(' ');
})();

// Map
function initializeMap(lat, lng, zoom) {
    var lat_c = lat === undefined ? 40.398417 : lat;
    var lng_c = lng === undefined ? 49.832223 : lng;
    var zoom_c = zoom === undefined ? 17 : zoom;
    var mapOptions = {
        center: new google.maps.LatLng(lat_c, lng_c),
        zoom: zoom_c,
        panControl : false,
        scrollwheel: false,
        streetViewControl : false,
        mapTypeControl : false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    var marker = new google.maps.Marker({
        position: map.getCenter(),
        map: map
    });
}

function listMap(lat, lng, zoom) {
    var lat_c = lat === undefined ? 40.398417 : lat;
    var lng_c = lng === undefined ? 49.832223 : lng;
    var zoom_c = zoom === undefined ? 17 : zoom;
    var mapOptions = {
        center: new google.maps.LatLng(lat_c, lng_c),
        zoom: zoom_c,
        panControl : false,
        scrollwheel: false,
        streetViewControl : false,
        zoomControl : false,
        mapTypeControl : false
    };
    var map = new google.maps.Map(document.getElementById("map_list"), mapOptions);
    var marker = new google.maps.Marker({
        position: map.getCenter(),
        map: map
    });
}

function over_position(){
    var window_w = $(window).width();
    if( window_w > 768 ){
        var over = $('.over');
        var over_h = over.outerHeight();
        var window_h = $(window).height();
        if( window_h < 597 || (window_w < 1440) ){
            over.css({marginTop:0, top:'200px'});
        }else if( window_h > 597 && window_h < 700){
            over.css({marginTop:0, top:(window_h-over_h) / 2 - 30});
        }else if( window_h > 700 && window_h < 800){
            over.css({marginTop:0, top:(window_h-over_h) / 2 - 100});
        }else if( window_h > 800){
            over.css({marginTop:0, top:(window_h-over_h) / 2 - 130});
        }
    } else {
        $('.over').removeAttr('style');
    }
    $('.main,.slider-wr').animate({opacity:1}, 500);
}

function layer_box_close(){
    $('.layer-box-fix').fadeOut(100);
    $('body').toggleClass('no-overflow');
    return false;
}

//var stikerm
$(document).ready(function () {
    /* ??? */
    if( $('.over').length ) over_position();

    /*******************************************************************/

    $(".faq_button").click(function(){
        $(".faq").css('display', 'none');
        $('.question_modal .right li a').removeClass('faq_open');
        var p = $(this);
        var id = p.attr("data-target");
        $(id).css('display', 'block');
        if($( window ).width()>=768){
            p.addClass('faq_open');
            var position = p.position();
            var height = p.height();
            $(".arrow_ri").css('top', position.top+10+"px");
            $(".arrow_ri").css('display', 'block');
        }
    });
    $(".faq .close").click(function(){
        $(".faq").css('display', 'none');
        $(".question_modal .right li a").removeClass('faq_open');
        $(".arrow_ri").css('display', 'none');
    });

    $('.j-edit__data').click(function () {
        $('.j-data__save').fadeOut(function () {
            $('.j-data__edit').fadeIn();
        });
        return false;
    });

    $('.j-remove__calcitem').click(function(){
        var elem = $(this).closest('.calc-row');
        $.confirm({
            'title'		: 'Внимание',
            'message'	: 'Вы уверены, что хотите удалить запись?',
            'buttons'	: {
                'Да'	: {
                    'class'	: 'order confirm-btn confirm-yes',
                    'action': function(){
                        elem.slideUp(function () {
                            elem.remove();
                        });
                    }
                },
                'Нет'	: {
                    'class'	: 'confirm-btn confirm-no',
                    'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
                }
            }
        });
        return false;
    });

    $(document).on('click','.confirmClose', function () {
        $('#confirmOverlay').fadeOut(function(){
            $(this).remove();
        });
        return false;
    });

    $('.j-contract-read__more').click(function () {
        $(this).parents('.j-contract__more').find('.j-contract__moreblock').fadeToggle();
        return false;
    });

    $('.j-layer__fix').click(function () {
        $('.layer-box-fix').fadeIn(200);
        $('body').toggleClass('no-overflow');
        return false;
    });

    $('.layer-box-close,.layer-box-close-dark').click(layer_box_close);

    $('.j-ins__show').click(function () {
        $('.l-ico-wrapp').fadeOut();
        $(this).parents('.l-table-main').fadeOut(function () {
            $(this).parents('.layer-box-fix').find('.j-ins-v').fadeIn();
        });
        return false;
    });
    $('.j-ins__hide').click(function () {
        $(this).parents('.layer-box-fix').find('.j-ins-v').fadeOut(function(){
            $(this).parents('.layer-box-fix').find('.l-table-main').fadeIn();
            $(this).parents('.layer-box-fix').find('.l-ico-wrapp').fadeIn();
        });
        return false;
    });

    if($(window).width() <= 768){
        $('#top_nav').removeClass("navbar-fixed-top navbar-default");
        $("#logo #logo-img").removeClass('logo-img-poz2').addClass('logo-img-poz1');
    } else {
        if ($(".feed .cont").length) {
            $(".feed .cont").rollbar({zIndex: 100});
        }
    }

    if ($(".n-adress__map").length) {
        $(".n-adress__map").rollbar({zIndex: 100});
    }

    /* Callback form */
    if( $('.j-clr-form').length ){
        $('.j-clr-form').jClever({
            selfClass: 'default',
            applyTo: {
                select: true,
                checkbox: true,
                radio: true,
                button: false,
                file: false
            }
        });
    }

    if($(window).width() >= 768 && $("div").hasClass("sticker-l") ) {
        $('.modal-header').mousedown(function(){
            $('.sticker-l').removeClass('zindex');
            $(this).parents('.sticker-l').addClass('zindex');
        });
        $('.modal-dialog').click(function(){
            $('.sticker-l').removeClass('zindex');
            $(this).parents('.sticker-l').addClass('zindex');
        });
        $(".feed ").draggable({
            handle: '.modal-header'
        });
        $(".chat").draggable({
            //containment:'.chat',
            handle: '.modal-header'
        });
        $(".calk").draggable({
            //containment:'body',
            handle: '.modal-header'
        });
    }
    $('.spoiler-title').click(function(){
        $(this).next().toggle();
        $(this).parent().toggleClass('q_act');
    });

    $(".calk-open").click(function(){
        $(".calk").show();
        return false;
    });

    $(".feed-open").click(function(){
        $(".feed").show( );
        $("body").addClass('b-cover');
        return false;
    });

    $(".chat-open").click(function(){
        $(".chat").show();
        return false;
    });

    $('.close').click(function() {
        var par = $(this).parents('.sticker-l');
        par.hide();
        par.removeAttr('style');
        if (par.hasClass("feed") ){
            $("body").removeClass('b-cover');
        }
    });
    $('#slides1').slick({
        speed: 300,
        slidesToShow: 1,
        adaptiveHeight: true,
        autoplay: true,
        autoplaySpeed: 5000,
        dots: true,
        arrows: false
    });
    $('#slides2').slick({
        speed: 300,
        slidesToShow: 1,
        adaptiveHeight: true,
        autoplay: true,
        autoplaySpeed: 5000,
        dots: true,
        arrows: false
    });
    $('#slides3').slick({
        speed: 300,
        fade:true,
        slidesToShow: 1,
        adaptiveHeight: true,
        autoplay: true,
        autoplaySpeed: 5000,
        dots: true,
        arrows: false
    });

    $('.j-date__input').datepicker({
        showOtherMonths: true,
        selectOtherMonths: true,
        dateFormat: 'dd.mm.yy',
        onClose: function (selectedDate) {
            $('.j-date__input').datepicker("option", "maxDate", selectedDate);
        }
    });

    if($('.over .order').length) {
        $('.stiker.hidden-xs').css('top', $('.order').offset().top);
    }
});



$(window).load(function(){
    if( $('#map_canvas').length ){
        initializeMap();
    }
    if( !$('html').hasClass('ie') || !$('html').hasClass('mac')) {
        $('.modal').on('show.bs.modal', function (e) {
            $('.head-r').css('margin-right', '17px');
            $('.stiker').css('right', 17);
        });
        $('.modal').on('hidden.bs.modal', function (e) {
            $('.head-r').removeAttr('style');
            $('.stiker').css('right', 0);
        });
    }

    /*** Set input value and left position when load page ***/
    $('.b-style__slider input[type=text]').each(function () {
        var left_pos = $(this).parent().find('.b-slider .ui-slider-range-min').css('width');
        var slider_val = $(this).parent().find('.b-slider').slider('value');
        $(this).css({left:left_pos}).val(slider_val);
    });

    if(navigator.sayswho == 'IE 11.0') {
        document.querySelector('html').className += ' ie11';
    }

});

window.onscroll = function () {
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    if ($("header").hasClass("main")) {
        if (scrolled > 195 && $(window).width() >= 767) {
            $('#top_nav').addClass('navbar-fixed-top navbar-default');
            $('#logo #logo-img').removeClass('logo-img-poz1').addClass('logo-img-poz2');
            $('#logo #logo-text').removeClass('logo-text-poz1').addClass('logo-text-poz2');
            $('#logo').removeClass('col-sm-2').addClass('col-md-3 col-sm-5 col-sm-1');
            if ($(window).width() >= 1400) {
                $('.stiker').css({'margin-right': '-140px', 'color': 'transparent'});
            }
            else {
                $('.stiker').css({'margin-right': '-120px', 'color': 'transparent'});
            }
        }
        else {
            $('.stiker').css({'margin-right': '0', 'color': '#fff'});
            $('#top_nav').removeClass('navbar-fixed-top navbar-default');
            $('#logo #logo-img').removeClass('logo-img-poz2').addClass('logo-img-poz1');
            $('#logo #logo-text').removeClass('logo-text-poz2').addClass('logo-text-poz1');
            $('#logo').removeClass('col-md-4 col-sm-5 col-sm-1').addClass('col-sm-2');
        }
    }
};

$(window).resize(function(){
    if( $('.over').length ){
        over_position();
    }
    if(!$("header").hasClass("main") ){
        if($(window).width() <= 751)
        {
            $('#top_nav').removeClass('navbar-fixed-top navbar-default');
            $('#logo #logo-img').removeClass('logo-img-poz2').addClass('logo-img-poz1');
        }
        else{
            $('#top_nav').addClass('navbar-fixed-top navbar-default');
            $('#logo #logo-img').addClass('logo-img-poz2').removeClass('logo-img-poz1');
        };};
});

if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
  var msViewportStyle = document.createElement('style');
  msViewportStyle.appendChild(
    document.createTextNode(
      '@-ms-viewport{width:auto!important}'
    )
  );
  document.querySelector('head').appendChild(msViewportStyle)
}
