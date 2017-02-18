$(document).ready(function() {
    i18n.init({
        lng: currLng,
        resGetPath: '/static/common/locales/__lng__/__ns__.json',
        getAsync: false
    });

    $('.callback form input, .callback form select').change(callback_form_validate);
    $('.j-phone__input').mask('?999999999999');

    var formValidatorErrors = {
        errorTitle: $.t('errorTitle'),
        requiredFields: $.t('requiredFields'),
        badTime: $.t('badTime'),
        badEmail: $.t('badEmail'),
        badTelephone: $.t('badTelephone'),
        badSecurityAnswer: $.t('badSecurityAnswer'),
        badDate: $.t('badDate'),
        lengthBadStart: $.t('lengthBadStart'),
        lengthBadEnd: $.t('lengthBadEnd'),
        lengthTooLongStart: $.t('lengthTooLongStart'),
        lengthTooShortStart: $.t('lengthTooShortStart'),
        notConfirmed: $.t('notConfirmed'),
        badDomain: $.t('badDomain'),
        badUrl: $.t('badUrl'),
        badCustomVal: $.t('badCustomVal'),
        andSpaces: $.t('andSpaces'),
        badInt: $.t('badInt'),
        badSecurityNumber: $.t('badSecurityNumber'),
        badUKVatAnswer: $.t('badUKVatAnswer'),
        badStrength: $.t('badStrength'),
        badNumberOfSelectedOptionsStart: $.t('badNumberOfSelectedOptionsStart'),
        badNumberOfSelectedOptionsEnd: $.t('badNumberOfSelectedOptionsEnd'),
        badAlphaNumeric: $.t('badAlphaNumeric'),
        badAlphaNumericExtra: $.t('badAlphaNumericExtra'),
        wrongFileSize: $.t('wrongFileSize'),
        wrongFileType: $.t('wrongFileType'),
        groupCheckedRangeStart: $.t('groupCheckedRangeStart'),
        groupCheckedTooFewStart: $.t('groupCheckedTooFewStart'),
        groupCheckedTooManyStart: $.t('groupCheckedTooManyStart'),
        groupCheckedEnd: $.t('groupCheckedEnd'),
        badCreditCard: $.t('badCreditCard'),
        badCVV: $.t('badCVV')
    };

    $.validate({
        form: '#j-ask-question__form, #j-complaint__form, #j-callme__form',
        language: formValidatorErrors
    });

    $('.select-company-form .select-company').change(function(){
        var $inp = $(this);
        var $form_wrap = $inp.parents('.ins-form-select');
        $form_wrap.find('.b-rules__block').fadeOut(200, function() {
            $form_wrap.find('.b-company-' + $inp.val() + '__block').fadeIn(200);
        })
    });

    $('.splash-box-close').on('click', splash_box_close);
    if(!Cookies.get('oys_splash_viewed') && !$('html').hasClass('mobile') && !_.has(requestGet, 'show')) {
        Cookies.set('oys_splash_viewed', true, {expires: 1});
        splash_box_show();
    }

    $('.compare-box-close').on('click', compare_box_close);

    if(_.has(requestGet, 'show') && requestGet['show'] == 'calculator') {
        $('.n-modal__calk').modal('show', {backdrop: false})
    }
});

/**
* Проверяем форму "позвоните мне" 
* и разрешаем или запрещаем ее отправлять
*/
function callback_form_validate() {
    var has_errors = false;
    $('.callback form input, .callback form select').each(function() {
        if($(this).val() == '')
            has_errors = true
    });

    if(has_errors)
        $('#callback_form_btn').addClass('disabled');
    else
        $('#callback_form_btn').removeClass('disabled')
}

/**/
function splash_box_show(){
    $('body').toggleClass('no-overflow');
    var $sb = $('.splash-box-fix');
    var splashWidth = $sb.innerWidth();
    var $vp = $sb.find('.splash-video-container')
        .append('<video id="splash-video-player" class="video-js vjs-default-skin vjs-big-play-centered" style="margin: 0 auto;"></video>')
        .find('#splash-video-player');

    // Set video size
    var videoWidth = Math.round(splashWidth * 0.8);
    var videoHeight = Math.round(videoWidth * 0.5625);
    $vp.attr('width', videoWidth + 'px');
    $vp.attr('height', videoHeight + 'px');

    // Auto close
    $vp.on('ended', function(){
        $vp.off('ended');
        splash_box_close();
    });

    // Append video sources
    $vp.append('<source src="/static/common/video/oys_splash.mp4" type="video/mp4" />');

    videojs('splash-video-player', {controls: false, autoplay: true, preload: "auto", techOrder: ["html5", "flash"]}, function(){
        var splashHeight = $sb.innerHeight();
        var playerHeight = $('#splash-video-player').innerHeight();
        $sb.find('.splash-video-container').css('margin', '' + Math.round((splashHeight - playerHeight) / 2) + 'px 50px');
    });

    $sb.fadeIn(200);
}

/**/
function splash_box_close(){
    $('.splash-box-fix').fadeOut(200);

    // Disposing video player
    videojs('splash-video-player').dispose();

    $('body').toggleClass('no-overflow');
    return false;
}

function compare_box_show(type, query_string){
    $('body').toggleClass('no-overflow');
    var $sb = $('.compare-box-fix');

    // Setting compare container dimensions
    var $cc = $sb.find('.splash-compare-container');

    $cc.load('/compare/'+type+'/' + (query_string || ''), function () {
        $sb.fadeIn(200);
    });
}

function compare_box_close(){
    $('.compare-box-fix').fadeOut(200, function() {
        // Clearing compare container
        $(this).find('.splash-compare-container').html('').attr('style', '')
    });

    $('body').toggleClass('no-overflow');
    return false;
}