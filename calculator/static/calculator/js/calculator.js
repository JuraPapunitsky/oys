/* Shared calculator part */
var calculator = {

    /*
    * Calculator spinner control
    * */

    spinnerTimer: null,

    show_spinner: function(){
        var $calc = $('.n-modal__calk');
        var timerId = this.spinnerTimer;
        this.spinnerTimer = setTimeout(function () {
            $calc.find('.b-spinner__modal').fadeIn(100);
            timerId = null;
        }, 200);
    },

    hide_spinner: function(){
        var $calc = $('.n-modal__calk');
        if (this.spinnerTimer!=null) clearTimeout(this.spinnerTimer);
        $calc.find('.b-spinner__modal').fadeOut(200);
    },

    /*
    * AJAX request helpers
    * */

     ajax_fail_dialog_factory: function(dialog_retry_func, dialog_cancel_func){

        return function(jqXHR, textStatus, errorThrown){
            var retry_func = dialog_retry_func !== undefined ? dialog_retry_func : function(){};
            var cancel_func = dialog_cancel_func !== undefined ? dialog_cancel_func : function(){};
            $.confirm({
                'title'		: $.t('titleWarning'),
                'message'	: $.t('msgRequestErrorRetry'),
                'buttons'	: {
                    'Yes'	: {
                        'class'	: 'order confirm-btn confirm-yes',
                        'action': function(){ setTimeout(retry_func, 1000) }
                    },
                    'No'	: {
                        'class'	: 'confirm-btn confirm-no',
                        'action': function(){ setTimeout(cancel_func, 1000) }
                    }
                }
            });
        }

    },

    /*
    * Slider widget functions
    * */

    /* Sets value and position of slider's input box according to it's slider widget value */
    slider_input_default_set: function($slider_text_input) {
        $slider_text_input.each(function () {
            var left_pos = $(this).parent().find('.b-slider .ui-slider-range-min').css('width');
            var slider_val = $(this).parent().find('.b-slider').slider('value');
            $(this).css({left:left_pos}).val(slider_val);
        });
    },

    /* 'slide' event handler function */
    slider_slide_handler: function (event, slider) {
        $(this).parent().find('input[type=text]').val(slider.value);
    },

    /* 'change' event handler for slider's text inputs */
    slider_input_chng_handler: function () {
        var $inp = $(this);
        var input_val = parseInt($inp.val());

        var $sl = $inp.parent().find('.b-slider');
        var slider_min = $sl.slider("option", "min");
        var slider_max = $sl.slider("option", "max");

        if(input_val < slider_min)
            $inp.val(slider_min.toString());
        else if (input_val > slider_max)
            $inp.val(slider_max.toString());

        $sl.slider("value", $inp.val());
        var left_pos = $inp.parent().find('.ui-slider-handle').position().left;
        $inp.css({left: left_pos});
    },

    slider_ui_handle_mousedown: function () {
        var $el = $(this);
        $('body').mousemove(function () {
            var left_pos = $el.position().left;
            $el.parents('.b-style__slider').find('input[type=text]').css({left: left_pos});
        });
    },

    slider_ui_handle_click: function () {
        var $el = $(this);
        var left_pos = $el.find('.ui-slider-handle').position().left;
        $el.parents('.b-style__slider').find('input[type=text]').css({left: left_pos});
    },

    /* init 'b-price__from' and 'b-price__to' labels of slider from 'min' and 'max' options of sliders inside each element of $slider_blocks selector */
    slider_ui_blocks_init: function($slider_blocks, strSuffix) {
        var n_split = function(strNumber) {return strNumber.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ')};
        $slider_blocks.each(function(){
            var $sl = $(this).find('.b-slider');
            $(this).find('.b-price__from').html(
                n_split($sl.slider("option", "min").toString()) + (strSuffix === undefined ? '' : strSuffix)
            );
            $(this).find('.b-price__to').html(
                n_split($sl.slider("option", "max").toString()) + (strSuffix === undefined ? '' : strSuffix)
            );
        })
    },

    /*
    * General UI functions
    * */

    /* jClever initialization */
    init_jclever: function () {
        $('.j-clr-calcform').jClever({
            selfClass: 'default',
            applyTo: {
                select: true,
                checkbox: false,
                radio: false,
                button: false,
                file: false
            }
        });
    },

    /* Calculator Step 1 select insurance product */
    ins_type_select: function (el) {
        calculator.show_spinner();
        var ins_type = $(el).data('ins-type');
        $.get('/calculator/modal/'+ins_type+'/', function(data){
            $('.j-clr-calcform-steps').append(data);
            calculator.hide_spinner();
            init_calculator();
            calculator.calc_form('forward', $(el));
            $(document).trigger('step_2_loaded');
            return false;
        })
    },

    /* Question sign click handler */
    help_layer_opener: function() {
        $(this).parent().addClass('n-qw__open').find('.b-aw__info').fadeIn(200);
        $('body').append('<div class="b-layer__fix j-layer__fix" />');
    },

    /* Callback factory for calculator sub steps */
    get_substep_callback: function (contract, id_attr, title_attr) {
        return function(){
            contract[id_attr] = $(this).prev().val();
            contract[title_attr] = $(this).prev().data('value');
            if(workflow.next_stage()) calculator.calc_form('subst', $(this));
        }
    },

    /* Предыдущий суб шаг */
    previous_substep: function () {
        var prev_substep = 'substep_' + ($(this).parent().data('substep')-1);
        workflow.rollback_stage(prev_substep);
        calculator.calc_form('step_prev', $(this));
        return false;
    },

    /* Предыдущий слой */
    previous_layer: function () {
        calculator.calc_form('layer_prev', $(this));
        return false;
    },

    /* Scrolling right panel in calculator modal */
    right_panel_scroll: function () {
        var $html = $('html');
        if ($(window).width() > 768 && !$html.hasClass('ie') && !$html.hasClass('ie11') && $html.hasClass('desktop')) {
            var $calc_block = $('.b-calc__block');
            $calc_block.unbind('scroll').scroll(function () {
                var $form_right = $('.e-active .b-form__right');
                var $modal_dialog = $calc_block.find('.modal-dialog');
                var calc_margin_top = $modal_dialog.css('margin-top');
                var calc_margin_bottom = $modal_dialog.css('margin-bottom');
                var form_right_height = $form_right.outerHeight();
                var $right_info_fixed = $form_right.find('.j-right__info-fixed');
                var right_info_fixed_height = $right_info_fixed.outerHeight();
                var calc_scrollTop = $('.b-calc__block').scrollTop();
                var top = ($('html').hasClass('ie')) ? '33px' : calc_scrollTop - (parseInt(calc_margin_top) - 33);

                if (calc_scrollTop >= parseInt(calc_margin_top) && ((right_info_fixed_height + 66) < form_right_height)) {

                    $right_info_fixed.removeClass('e-fixed__btm').addClass('e-fixed__top')
                        .css({'top': top, 'max-width': $form_right.width() + 'px'});

                    if ((form_right_height + (parseInt(calc_margin_bottom) - 66) ) <= (calc_scrollTop + right_info_fixed_height)) {
                        $right_info_fixed.addClass('e-fixed__btm');
                    }

                } else {
                    $right_info_fixed.removeClass('e-fixed__btm e-fixed__top');
                }
            });
        }
    },

    /* Resets calculator state */
    reset_calculator: function(){
        $('.n-modal__calk').load('/calculator/modal/ .modal-dialog');
        return false;
    },

    /* Перезапуск калькулятора и начало расчета для {ins_type} */
    start_calculator: function(ins_type) {
        $('.n-modal__calk').load('/calculator/modal/ .modal-dialog', function() {
            calculator.ins_type_select(
                $('.n-modal__calk a[data-ins-type="'+ins_type+'"]')
            );
            $('.n-modal__calk').modal('show', {backdrop: false});
        });
        return false;
    },

    /*
    * Custom controls for modal
    * */

    /* Text simple replace selection control (country, city) */
    replace_selection_control: function () {
        var $el = $(this).closest('.j-block__scr');
        $el.find('.j-replace__text').text($(this).prev().data('value'));
        $el.find('.n-main__radio').val($(this).prev().val());
        $el.find('.b-block__scr').fadeOut();
    },

    /* Text replace selection control (bank) for radio field + selection */
    replace_selection_control2: function () {
        var $el = $(this).closest('.j-block__scr');
        $el.find('.j-replace__text').text($(this).prev().data('value'));
        $el.find('.b-block__scr').fadeOut();
    },

    /* Controls checkbox inputs with toggeable b-block__scr block and radio inputs child window element */
    additional_fields_control: function () {
        var $el = $(this);
        if ($el.is('input[type=checkbox]')) {
            $el.parent().find('.b-block__scr')[$el.prop('checked') ? 'fadeIn' : 'fadeOut'](200);
        } else if ($el.is('input[type=radio]')) {
            var window = $el.data('window');
            $el.closest('.j-block__scr').find('.b-block__scr').fadeOut(0, function () {
                if ($(this).data('window') == window) $(this).fadeIn();
            });
        }
    },

    /*
    * Workflow functions
    * */

    /* Automatically selects company for product */
    auto_select_companies: function (contract_obj, $tariff_table, product_id) {
        var p_comp = contract_obj['p'+product_id+'_inscompany'];
        if(p_comp == null)
            contract_obj['p'+product_id+'_inscompany'] = $tariff_table.find('input.product-' + product_id + '__radio').first().prop('checked', 'checked').val();
        else
            $tariff_table.find('input.product-'+product_id+'__radio[value="'+p_comp+'"]').prop('checked', 'checked');
    },

    /* Total cost of all selected products */
    calculate_total_sum: function ($ui) {
        var detailsAndPrices = [];
        // Main products
        $ui.find('.b-sigorta__table .n-main__radio').serializeArray().forEach(function (obj) {
            var detail_class = '.' + obj.name.replace('_inscompany', '__detail');
            var $el = $ui.find('input[name="' + obj.name + '"][value="' + obj.value + '"]');
            detailsAndPrices.push({
                sel: detail_class,
                text: $el.parents('tr').find('td').first().text(),
                price: $el.data('price')
            });
        });

        // Ateshgah additional options for vehicle insurance
        $ui.find('#ateshgah-options input:checked').serializeArray().forEach(function (obj) {
            var $el = $ui.find('input[name="' + obj.name + '"]');
            detailsAndPrices.push({
                sel: '.' + obj.name + '__detail',
                text: $ui.find('input[name="p2_inscompany"][value="1"]').parents('tr').find('td').first().text(),
                price: $el.data('price')
            });
        });

        // Free delivery
        detailsAndPrices.push({sel: '.delivery__detail', text: '', price: '0.0'});

        $ui.find('.b-right__detail').addClass('n-brd__btm-no').removeClass('n-brd__mrg').hide();

        var total_sum = 0;
        _.each(detailsAndPrices, function (detail) {
            var $detail = $ui.find(detail.sel).fadeIn(200, function () {
                $ui.find('.b-right__detail:visible').first().addClass('n-brd__mrg');
                $ui.find('.b-right__detail:visible').last().removeClass('n-brd__btm-no');
            });
            $detail.find('.b-detail__text span').html(detail.text);
            $detail.find('.b-detail__price span').html(detail.price);
            total_sum += parseFloat(detail.price);
        });

        $ui.find('.b-total__summ').html(total_sum.toString() + '<span>AZN</span>');

        return total_sum;
    },

    /* Switches stage, sub stages and layers */
    calc_form: function (direction, el) {
        var $calc_form = $('.n-modal__calk');

        switch (direction) {

            // Следующий шаг
            case 'forward':
                var current_step = $(el).parents('.n-form__step.e-active').attr('id').match(/[\d]/);
                var last_step = $('.n-form__step').last().attr('id').match(/[\d]/);
                current_step++;
                if (current_step > last_step) {
                    return false;
                } else {
                    $('.n-form__step').removeClass('e-active');
                    $('#step-' + current_step).addClass('e-active');
                    $calc_form.find('input[name="step"]').val('step-' + current_step);
                }
                break;

            // Пердыдущий шаг
            case 'backward':
                var current_step = $(el).parents('.n-form__step.e-active').attr('id').match(/[\d]/);
                var first_step = $('.n-form__step').first().attr('id').match(/[\d]/);
                current_step--;
                if (current_step < first_step) {
                    return false;
                } else {
                    $('.n-form__step').removeClass('e-active');
                    $('#step-' + current_step).addClass('e-active');
                    $calc_form.find('input[name="step"]').val('step-' + current_step);
                }
                break;

            // Следующая подступень
            case 'subst':
                var current_substep = $(el).parents('.e-active').attr('id').match(/[\d]/);
                var last_step = $('.n-form__substep').last().attr('id').match(/[\d]/);
                current_substep++;

                if ( current_substep > last_step ) {
                    return false;
                } else {
                    $('.n-form__substep').removeClass('e-active');
                    $('#substep-' + current_substep).addClass('e-active');
                    $('.n-modal__calk').find('input[name="substep"]').val('substep-' + current_substep);

                    var $last_step_item = $('.b-step__item').last();
                    var step_item_clone = $last_step_item.clone();

                    /* Create badge with value selected in sub step */
                    var substep_selection_text = '';
                    var $prev_el = $(el).prev();

                    if ($prev_el.is('input')) {
                        $('.b-step__list').show().append(step_item_clone);
                        $('.b-step__item').last().show();
                        if ($('.b-step__list .b-step__item span').last().text() == '') {
                            $('.b-step__list .b-step__item').first().remove();
                        }
                        substep_selection_text = $prev_el.data('value');

                    }else if ($prev_el.is('.input-wr')) {
                        $('.b-step__list').show().append(step_item_clone);
                        $('.b-step__item').last().show();
                        if ($('.b-step__list .b-step__item span').last().text() == '') {
                            $('.b-step__list .b-step__item').first().remove();
                        }
                        substep_selection_text = $prev_el.find('input').val();

                    } else if ($prev_el.is('div') && $prev_el.hasClass('badge-text-wr')) {
                        $('.b-step__list').show().append(step_item_clone);
                        $('.b-step__item').last().show();
                        if ($('.b-step__list .b-step__item span').last().text() == '') {
                            $('.b-step__list .b-step__item').first().remove();
                        }
                        substep_selection_text = $prev_el.find('input').val();

                    } else if ($prev_el.is('.jClever-element') && $prev_el.children().first().is('.jClever-element-select-wrapper')) {
                        $('.b-step__list').show().append(step_item_clone);
                        $('.b-step__item').last().show();
                        substep_selection_text = $prev_el.children().first().find('select :selected').text();

                    } else if ($prev_el.is('.b-style__slider') ){
                        $('.b-step__list').show().append(step_item_clone);
                        $('.b-step__item').last().show();
                        var strSuffix = '';
                        if (!$prev_el.is('.n-insured_days'))
                            strSuffix = ' AZN';
                        substep_selection_text = $prev_el.find('input[type=text]').val()+strSuffix;

                    } else
                        return false;

                    $('.b-step__list .b-step__item span').last().text(substep_selection_text).parent().attr('data-substep', current_substep);
                }
                break;

            // Переход к предыдущему шагу
            case 'step_prev':
                var current_substep = '#substep-'+parseInt($(el).parent().data('substep')-1);
                $('.n-form__substep').removeClass('e-active');
                $(current_substep).addClass('e-active');
                $calc_form.find('input[name="substep"]').val($(current_substep).attr('id'));
                $(el).parent().nextAll('.b-step__item').remove();
                if( parseInt($(el).parent().data('substep')-1) == 1 ) {
                    $(el).parent().hide(0).find('span').text('');
                } else {
                    $(el).parent().remove();
                }
                $('#step-2 .b-step__current-item.n-item__curr').each(function (e) {
                    e++;
                    if( parseInt(e) === parseInt($(el).parent().data('substep')-1) ){
                        $(this).nextAll().removeClass('n-item__curr');
                    }
                });
                break;

            // Переход к следующему слою
            case 'layer':
                $(el).parents('.b-layer__content').fadeOut(function () {
                    var $layer = $(el).parents('.n-form__layer').next('.n-form__layer').fadeIn().addClass('e-active');
                    $calc_form.find('input[name="layer"]').val($layer.attr('id'));
                    if ($(el).parents('.n-form__layer').next('.n-form__layer').children().is('a')) {
                        $(el).parents('.n-form__layer').next('.n-form__layer').children('a').replaceWith('<h3>' + $(el).parents('.n-form__layer').next('.n-form__layer').children('a').text() + '</h3>')
                        $(el).parents('.n-form__layer').next('.n-form__layer').find('.b-layer__content').fadeIn();
                    }
                    if ($(el).parents('.n-form__layer').children().is('h3')) {
                        $(el).parents('.n-form__layer').children('h3').replaceWith('<a href="#" class="b-prev__layer j-prev__layer">' + $(el).parents('.n-form__layer').children('h3').text() + '</a>');
                    }
                }).parents('.n-form__layer').removeClass('e-active');

                if ($(el).data('last') === true){
                    $('.j-last__show').addClass('e-show');
                }
                break;

            // Переход к предыдущему слою
            case 'layer_prev':
                $(el).parent().nextAll('.n-form__layer').fadeOut().removeClass('e-active');
                $(el).parent().fadeIn(function () {
                    var $layer = $(el).next('.b-layer__content').fadeIn().parent().addClass('e-active');
                    $calc_form.find('input[name="layer"]').val($layer.attr('id'));
                });
                $(el).replaceWith('<h3>'+$(el).text()+'</h3>');
                $('.j-next__click').removeClass('e-show');
                break;

            default:
                break;
        }

        if( $(el).parents('.b-form__block').find('.b-step__current-item.n-item__curr').length ) {
            $(el).parents('.b-form__block').find('.b-step__current-item.n-item__curr').last().next().addClass('n-item__curr');
        }

        return true;
    }
};
