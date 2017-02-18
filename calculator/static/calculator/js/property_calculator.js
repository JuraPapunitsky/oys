var property_calculator = {

    contract: {},

    /* Init contract object */
    init_contract: function(){
        this.contract = {
            csrfmiddlewaretoken:'',
            step: '',
            substep: '',
            layer: '',
            /**/
            main_product: null,
            main_product_text: '',
            p3_selected: false,
            d_start: null,
            term_insurance: null,
            /* Недвижимость */
            realty_type: null,
            realty_type_text: '',
            city: null,
            city_text: '',
            branch: null,
            branch_text: '',
            s_insurance: null,
            franchise: null,
            /* Общее - страхователь */
            ins_person_pin: '',
            ins_person_fname: '',
            ins_person_lname: '',
            ins_person_mname: '',
            ins_person_gender: null,
            ins_person_birthday: null,
            ins_country: null,
            ins_city: null,
            ins_city_custom: '',
            ins_address: '',
            ins_index: '',
            ins_street: '',
            ins_house: '',
            ins_apartment: '',
            ins_phone: '',
            ins_email: '',
            /* Доставка и оплата */
            delivery_type: '',
            delivery_date: null,
            delivery_time: null,
            delivery_city: null,
            delivery_region: '',
            delivery_street: '',
            delivery_house: '',
            delivery_apartment: '',
            delivery_phone: '',
            delivery_comment: '',
            delivery_takeout: null,
            delivery_email: '',
            payment_type: ''
        }
    },

    get_title: function(){
        return this.contract.realty_type_text
    },

    get_description: function(){
        var msg = this.contract.city_text;
        msg += ', ' + $.t('tInsSum') + ' ' + this.contract.s_insurance.toString() + ' AZN,<br/>';
        msg += $.t('tFranSum') + ' ' + this.contract.franchise.toString() + ' AZN';
        return msg
    },

    /* Refreshes inputs, controlling current step, substep and layer of calculator UI */
    refresh_state: function(){
        var $form = $('.j-clr-calcform');
        $form.find('input[name="step"]').val($form.find('.n-form__step.e-active').attr('id'));
        $form.find('input[name="substep"]').val($form.find('.n-form__substep.e-active').attr('id'));
        $form.find('input[name="layer"]').val($form.find('.n-form__layer.e-active').attr('id'));
    },

    /* Refreshes internal data structures (calculator-specific) */
    refresh_data: function(){
        var calc = property_calculator;
        var $form = $('.j-clr-calcform');

        // Product select from step-3
        calc.contract['p3_selected'] = false;
        if(calc.contract['main_product'] && calc.contract['main_product'] !== undefined)
            calc.contract['p'+calc.contract['main_product']+'_selected'] = true;

        var boolFields = ['p3_selected'];
        $form.serializeArray().forEach(function(obj){
            if (boolFields.indexOf(obj.name) >= 0) {
                calc.contract[obj.name] = true;
            } else {
                calc.contract[obj.name] = obj.value;
            }
        });
    },

    /* Validates {contract} fields via ajax json request */
    validate_contract: function(fields, complete){
        property_calculator.refresh_state();
        property_calculator.refresh_data();

        /* Clean up previous errors (removes data-iserror classes and cleans .field-error block spans */
        fields.forEach(function(fld){
            $('.j-clr-calcform').find('input[name="'+fld+'"]').parents('.b-data__line').removeClass('data-iserror').find('.field-error span').html('');
        });

        /* Call 'validate' method via AJAX */
        $.post('/calculator/modal/property/?m=json&cl=validate', property_calculator.contract, function(result){
            var has_errors = false;
            if (result.has_errors) {
                // Parse result object's errors attribute, expecting JSON string there
                var field_errors = $.parseJSON(result.errors);
                fields.forEach(function(fld){
                    var $fld_wr = $('.j-clr-calcform').find('input[name="'+fld+'"]').closest('.b-data__line');

                    /*
                    Если проверяемое поле есть в списке полей с ошибками, то собираем текст всех ошибок и помеяаем
                    в интерфейсе поле как содержащее ошибки
                     */
                    var errors_text = '';
                    if (field_errors.hasOwnProperty(fld)){

                        field_errors[fld].forEach(function(e){
                            errors_text += e.message + '<br/>';
                        });

                        /*
                        Если были обнаружены ошибки, то обертке блока с контролом проставляется класс data-iserror
                        и текст ошибок записывается в .field-errors span
                        */
                        $fld_wr.addClass('data-iserror').find('.field-error span').append(errors_text);

                        has_errors = true;
                    }
                });
            }
            complete(has_errors);
        });
    },

    /* Property params edit */
    property_edit_click: function(){
        var rb_step = property_calculator.contract.realty_type == '1' ? 'substep_2': 'substep_5';
        if(workflow.rollback_stage(rb_step)) {
            $('.n-form__step').removeClass('e-active');
            $('#step-2').addClass('e-active');
        }
    },

    /* Copy selected products and total price */
    copy_right_info: function($source_step, $target_step){
        ['.p3__detail', '.delivery__detail'].forEach(function(cls){
            var $prev_product = $source_step.find(cls);
            var $curr_product = $target_step.find(cls);

            $curr_product.attr('style', $prev_product.attr('style'));
            $curr_product.attr('class', $prev_product.attr('class'));

            /*** Coping product title, company and price from previous step ***/
            $prev_product.find('.b-detail__title, .b-detail__text, .b-detail__price').each(function(){
                $curr_product.find('.'+$(this).attr('class')).html($(this).html());
            })
        });
        $target_step.find('.b-total__summ').html($source_step.find('.b-total__summ').html());
    },

    /* Field value masks (calculator-specific method) */
    init_field_masks: function(){
        delete $.mask.definitions[9];
        $.mask.definitions['#']='[0-9]';
        $.mask.definitions['@']='[A-Za-züöğçşəıƏÜĞÇŞÖİI ]';
        $.mask.definitions['~']='[A-Za-z0-9üöğçşəıƏÜĞÇŞÖİI,. /-]';
        $.mask.definitions['%'] = '[0-9ABCDEFGHJKLMNPRSTUVWXYabcdefghjklmnprstuvwxy]';

        $('#id_auto_vin').mask('%%%%%%%%%%%%%%%%%');
        $('#id_auto_number').mask('?*********');
        $('#id_ins_person_pin').mask('*******');
        $('#id_ins_person_fname, #id_ins_person_lname').mask('?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@');
        $('#id_ins_person_mname').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_street, #id_delivery_street').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_phone, #id_delivery_phone').mask('?############');
        $('#id_index').mask('AZ####');
        $('#id_ins_index').mask(property_calculator.contract.ins_country == '4' ? 'AZ####' : '######');
        $('#id_d_start, #id_ins_person_birthday, #id_delivery_date').mask('##.##.####');
    },

    /* Step 4 sliders initialization */
    init_step4_sliders: function ($ui, step_obj) {
        var calc = property_calculator;
        $('.b-s_insurance_2__slider .b-slider').slider({
            range: 'min',
            value: calc.contract.s_insurance,
            step: 1000,
            min: 1000,
            max: 1000000
        });
        var sl_params = calc.get_franchise_slider_params(calc.contract.s_insurance);
        sl_params.value = calc.contract.franchise;
        $('.b-franchise_2__slider .b-slider').slider(sl_params);

        var $slider_blocks = $ui.find('.b-style__slider');
        var $sliders = $slider_blocks.find('.b-slider');

        var delayTimeout = null;
        $sliders.slider({
            slide: function (event, slider) {
                $(this).parent().find('input[type=text]').val(slider.value);

                // Load product matrix
                if (delayTimeout != null) {
                    clearTimeout(delayTimeout);
                }

                delayTimeout = setTimeout(function () {
                    var new_s_insurance = parseInt($ui.find('[name="s_insurance_2"]').val());
                    var $franchise_inp = $ui.find('[name="franchise_2"]');
                    var new_franchise = parseInt($franchise_inp.val());
                    var s_ins_changed = (calc.contract.s_insurance != new_s_insurance);

                    if (s_ins_changed) {
                        var sl_params = calc.get_franchise_slider_params(new_s_insurance);
                        if (new_franchise > sl_params.max) new_franchise = sl_params.max;
                        sl_params.value = new_franchise;
                        $('.b-franchise_2__slider .b-slider').slider(sl_params);
                        calculator.slider_ui_blocks_init($('.b-franchise_2__slider'), ' AZN');
                        calculator.slider_input_default_set($franchise_inp)
                    }

                    $('[name="s_insurance"]').val(new_s_insurance);
                    $('[name="franchise"]').val(new_franchise);
                    calc.contract.s_insurance = new_s_insurance;
                    calc.contract.franchise = new_franchise;

                    step_obj.load_product_matrix();
                }, 1000);
            }
        });

        var $all_slider_inputs = $slider_blocks.find('input[type=text]');
        /*** Set input value when change ***/
        $all_slider_inputs.change(calculator.slider_input_chng_handler);
        /*** Set input value and left position when load page ***/
        calculator.slider_input_default_set($all_slider_inputs);
        calculator.slider_ui_blocks_init($slider_blocks, ' AZN');
        $slider_blocks.find('.ui-slider-handle').mousedown(calculator.slider_ui_handle_mousedown);
        $slider_blocks.find('.ui-slider').click(calculator.slider_ui_handle_click);
    },

    get_franchise_slider_params: function(ins_sum){
        var sl_defaults = null;
        if (1000 <= ins_sum && ins_sum < 100000)
            sl_defaults = {range: 'min', step: 50, min: 50, max: 4999, value: 500};
        else if (100000 <= ins_sum && ins_sum  < 250000)
            sl_defaults = {range: 'min', step: 50, min: 100, max: 9999, value: 500};
        else if (250000 <= ins_sum && ins_sum < 500000)
            sl_defaults = {range: 'min', step: 50, min: 150, max: 24999, value: 500};
        else if (500000 <= ins_sum && ins_sum < 1000000)
            sl_defaults = {range: 'min', step: 50, min: 500, max: 49999, value: 500};
        else if (1000000 <= ins_sum && ins_sum < 2500000)
            sl_defaults = {range: 'min', step: 50, min: 1000, max: 99999, value: 1000};
        else if (2500000 <= ins_sum && ins_sum < 5000000)
            sl_defaults = {range: 'min', step: 50, min: 1500, max: 199999, value: 1500};
        else if (5000000 <= ins_sum && ins_sum < 10000000)
            sl_defaults = {range: 'min', step: 50, min: 2000, max: 299999, value: 2000};
        else if (10000000 <= ins_sum && ins_sum <= 15000000)
            sl_defaults = {range: 'min', step: 50, min: 2500, max: 399999, value: 2500};
        return sl_defaults
    },

    /* Vehicle contracts calculation steps */
    workflow_steps: {
        /* Realty type selection */
        substep_1: {
            load: function(){
                $('#substep-1').find('.b-radio__wr label').unbind('click').click(
                    calculator.get_substep_callback(property_calculator.contract, 'realty_type', 'realty_type_text')
                );
            },
            init: function(){
                $(document).trigger('substep_1_loaded')
            },
            rollback: function(){
                var ct = property_calculator.contract;
                ct['realty_type'] = null;
                ct['realty_type_text'] = '';
            },
            next: function() { return 'substep_2' }
        },

        /* Realty placement city selection */
        substep_2: {
            load: function(){
                var ct = property_calculator.contract;
                $('#substep-2').find('.b-radio__wr label').unbind('click').click(function(){
                    ct['city'] = $(this).prev().val();
                    ct['city_text'] = $(this).prev().data('value');

                    if(ct.realty_type == '1') {
                        var $s_ins = $('#substep-4 input[name="s_insurance"]');
                        var $fran = $('#substep-5 input[name="franchise"]');
                        switch (ct.city) {
                            case '1':
                                ct['s_insurance'] = 25000;
                                ct['franchise'] = 250;
                                break;
                            case '2':
                            case '3':
                            case '4':
                                ct['s_insurance'] = 20000;
                                ct['franchise'] = 200;
                                break;
                            default:
                                ct['s_insurance'] = 15000;
                                ct['franchise'] = 150;
                                break;
                        }
                        $s_ins.val(ct['s_insurance']);
                        $fran.val(ct['franchise']);
                    }

                    if (ct.realty_type == '2' || ct.realty_type == '3')
                        calculator.calc_form('subst', $(this));
                    else {
                        calculator.calc_form('forward', $(this));
                    }
                    workflow.next_stage();
                });
            },
            init: function() {
                $(document).trigger('substep_2_loaded');
            },
            rollback: function(){
                var ct = property_calculator.contract;
                ct['city'] = null;
                ct['city_text'] = '';
            },
            next: function() {
                var ct = property_calculator.contract;
                switch(ct.realty_type) {
                    case '2': return 'substep_3';
                    case '3': return 'substep_3';
                    default: return 'step_3'
                }
            }
        },

        /* Realty branch selection */
        substep_3: {
            load: function(){
                var ct = property_calculator.contract;
                var $ui = $('#substep-3');

                $ui.find('.j-next__click').unbind('click').click(function(){
                    var $sel_opt = $ui.find('[name="branch"] :selected');
                    ct.branch = parseInt($sel_opt.val());
                    ct.branch_text = $sel_opt.text();
                    calculator.calc_form('subst', $(this));
                    workflow.next_stage();
                });
            },
            init: function() {
                $(document).trigger('substep_3_loaded');
            },
            rollback: function(){
                var ct = property_calculator.contract;
                ct['branch'] = null;
                ct['branch_text'] = '';
            },
            next: function() { return 'substep_4' }
        },

        /* Insurance sum selection */
        substep_4: {
            load: function(){
                var ct = property_calculator.contract;
                var $ui = $('#substep-4');

                $ui.find('.j-next__click').unbind('click').click(function(){
                    ct.s_insurance = parseInt($('input[name="s_insurance"]').val());
                    if(workflow.next_stage()) calculator.calc_form('subst', $(this));
                });
            },
            init: function(){
                $(document).trigger('substep_4_loaded')
            },
            rollback: function(){
                property_calculator.contract.s_insurance = null;
            },
            next: function() { return 'substep_5' }
        },

        /* Deductible selection */
        substep_5: {
            load: function(){
                var ct = property_calculator.contract;
                var $ui = $('#substep-5');

                // Deductible slider initialization
                $ui.find('.b-slider').slider(property_calculator.get_franchise_slider_params(ct.s_insurance));
                var $inp = $('input[name="franchise"]');
                calculator.slider_input_default_set($inp);
                calculator.slider_ui_blocks_init($ui.find('.b-style__slider'), ' AZN');

                // Next step button actions
                $ui.find('.j-next__click').unbind('click').click(function(){
                    ct.franchise = parseInt($inp.val());
                    if(workflow.next_stage()) calculator.calc_form('forward', $(this));
                });
            },

            init: function() {
                $(document).trigger('substep_5_loaded')
            },

            rollback: function(){
                property_calculator.contract.franchise = null;
            },

            next: function() { return 'step_3' }
        },

        step_3: {
            load: function(){

                calculator.show_spinner();
                var ct = property_calculator.contract;
                var $ui = $('#step-3');

                ct.csrfmiddlewaretoken = $ui.parents('.j-clr-calcform').find('input[name="csrfmiddlewaretoken"]').val();

                $.post('/calculator/modal/property/?m=ajax&cl=precalculate', ct, function(data){

                    $ui.find('.b-form__left').html(data).find('.insurance_product__btn').unbind('click').click(function () {
                        //var ct = vehicle_calculator.contract;
                        ct.main_product = $(this).data('product-id');
                        ct.main_product_text = $(this).data('product-title');
                        ct['p'+ct.main_product+'_selected'] = true;

                        $('#step-4 .b-sigorta__table').html($ui.find('#p'+ct.main_product+'_preloaded').html());
                        $ui.find('#product_preload_block').html('');

                        workflow.next_stage();
                        calculator.calc_form('forward', $(this));

                        return false;
                    });
                    calculator.hide_spinner();

                    $ui.find('.j-calculator__reset').click(calculator.reset_calculator);
                    $(document).trigger('step_3_loaded');

                }).fail(
                    calculator.ajax_fail_dialog_factory(property_calculator.workflow_steps.step_3.load)
                );
            },

            init: function(){
                var $ui = $('#step-3');
                var calc = property_calculator;
                // Display text description on the right
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());
            },

            next: function(){
                return 'step_4'
            }
        },

        step_4: {
            /*** Custom properties ***/
            validated_fields: ['p3_selected'],

            /* Load product matrix */
            load_product_matrix: function () {
                var calc = property_calculator;
                var step_obj = property_calculator.workflow_steps.step_4;

                calc.validate_contract(step_obj.validated_fields, function(has_errors){
                    if (!has_errors) {

                        calculator.show_spinner();
                        $.post('/calculator/modal/property/?m=ajax&cl=calculate&spr=3', calc.contract, function (data) {

                            var $tariff_table = $('.b-sigorta__table');

                            // Product - company selection controls
                            $tariff_table.html(data).find('input[type="radio"]').unbind('click').click(function () {
                                calc.contract[$(this).attr('name')] = $(this).val();
                                calculator.calculate_total_sum($('#step-4'));
                            });

                            // Auto select companies
                            [3].forEach(function (product_id) {
                                calculator.auto_select_companies(calc.contract, $tariff_table, product_id);
                            });

                            $('#step-4 .b-info__text').html(calc.get_description());
                            calculator.calculate_total_sum($('#step-4'));

                            calculator.hide_spinner();

                        }).fail(
                            calculator.ajax_fail_dialog_factory(property_calculator.workflow_steps.step_4.load_product_matrix)
                        );

                    }
                });
            },

            /*** Workflow properties ***/

            load: function(){
                var step_obj = this;
                var calc = property_calculator;

                calculator.show_spinner();
                $.get('/calculator/modal/property/?m=ajax&cl=options&pr='+calc.contract.main_product+'&realty_type='+calc.contract.realty_type, {},
                    function(data){
                        var $ui = $('#step-4');
                        var $step_options = $('.b-step-4__options').html(data);

                        /*** Контролы этапа (параметры продуктов) вызывают расчет матрицы продуктов ***/
                        $step_options.find('input').unbind('change').change(step_obj.load_product_matrix);

                        /*** Открыть подсказку ***/
                        $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                        /* Initialize sliders */
                        calc.init_step4_sliders($ui, step_obj);
                        if(calc.contract.realty_type == '1') {
                            $ui.find('.b-slider').slider("disable");
                            $ui.find('input[name="s_insurance_2"],input[name="franchise_2"]').prop("disabled", true);
                        } else {
                            $ui.find('.b-slider').slider("enable");
                            $ui.find('input[name="s_insurance_2"],input[name="franchise_2"]').prop("disabled", false);
                        }

                        calculator.hide_spinner();
                        $(document).trigger('step_4_loaded');

                    }).fail(calculator.ajax_fail_dialog_factory(property_calculator.workflow_steps.step_4.load));
            },

            init: function(){
                var step_obj = this;
                var $ui = $('#step-4');
                var $tariff_table = $ui.find('.b-sigorta__table');
                var calc = property_calculator;

                // Right infos
                $ui.find('.b-step__title h2').html(calc.contract.main_product_text);
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                // Insurance company selection
                $tariff_table.find('input[type="radio"]').unbind('click').click(function () {
                    calc.contract[$(this).attr('name')] = $(this).val();
                    calculator.calculate_total_sum($('#step-4'));
                });

                // Auto select company
                calculator.auto_select_companies(calc.contract, $tariff_table, calc.contract.main_product);

                // Calculate total sum
                calculator.calculate_total_sum($ui);

                $ui.find('.j-next__click').unbind('click').click(function(){
                    var $el = $(this);
                    calc.validate_contract(step_obj.validated_fields, function(has_errors){
                        if(!has_errors) {
                            if(workflow.next_stage()) calculator.calc_form('forward', $el);
                        }
                    });
                })
            },

            next: function(){ return 'step_5' }
        },

        step_5: {
            /*** Workflow properties ***/
            init: function(){
                var step = this;
                var $ui = $('#step-5');
                var calc = property_calculator;

                calculator.right_panel_scroll();

                /* Display text description on the right */
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                /* Using Method field display */
                if(calc.contract.realty_type != '1') $ui.find('#b-using_method').show();

                /* Field masks initialization */
                calc.init_field_masks();

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                /*** Открыть доп. поля ***/
                $ui.find('.j-block__scr input[type=checkbox],.j-block__scr .n-main__radio').unbind('click').click(calculator.additional_fields_control);

                /*** Выбор (замена текста) ***/
                $ui.find('.j-replace__value .b-radio__wr label').unbind('click').click(calculator.replace_selection_control);

                /* Блоки изменение блоков адресов при изменении страны */
                $ui.find('input[name="ins_country"]').unbind('change').change(function(){
                    var $el = $(this);
                    var $layer = $el.closest('.n-form__layer');
                    $layer.find('.resident-address__block').fadeOut(100);
                    $layer.find('.foreign-address__block').fadeOut(100);
                    if ($el.val() == '4') {
                        $layer.find('.resident-address__block').fadeIn(200);
                        $layer.find('.foreign-address__block').fadeOut(200);
                        $layer.find('.postal-index__block input').mask('AZ####');
                    } else {
                        $layer.find('.resident-address__block').fadeOut(200);
                        $layer.find('.foreign-address__block').fadeIn(200);
                        $layer.find('.postal-index__block input').mask('######');
                    }
                });

                /*** Copy selected products and total price from step 4 ***/
                calc.copy_right_info($('#step-4'), $ui);

                /* Обработка кнопок "следующий слой" и "следующий шаг" */
                $ui.find('.j-next__layer,.j-next__click').unbind('click').click(function () {
                    var $el = $(this);
                    var flds = {
                        'layer-1': ['n_reestr', 'document_reason', 'using_method', 'address', 'index'],
                        'layer-2': ['term_insurance', 'd_start'],
                        'layer-3': ['ins_person_pin', 'ins_person_fname', 'ins_person_lname', 'ins_person_mname', 'ins_person_gender',
                            'ins_person_birthday', 'ins_index', 'ins_country', 'ins_city', 'ins_city_custom', 'ins_address',
                            'ins_street', 'ins_house', 'ins_apartment', 'ins_phone', 'ins_email']
                    };

                    var curr_layer = $('input[name="layer"]').val();
                    calc.validate_contract(flds[curr_layer], function(has_errors){
                        if (!has_errors) {
                            if ($el.hasClass('j-next__layer')) {
                                calculator.calc_form('layer', $el);
                            } else if ($el.hasClass('j-next__click')) {
                                if(workflow.next_stage()) calculator.calc_form('forward', $el);
                            }
                        }
                    });
                    return false;
                });

                $(document).trigger('step_5_loaded');
            },

            rollback: function(){
                var $ui = $('#step-5');
                calculator.calc_form('layer_prev', $ui.find('#layer-1 .j-prev__layer'));
            },

            next: function() { return 'step_6' }
        },

        /* Delivery and payment */
        step_6: {
            /*** Workflow properties ***/
            init: function(){
                var calc = property_calculator;
                var $ui = $('#step-6');

                calc.init_field_masks();

                /* Controls events */
                $ui.find('.j-block__scr input[type=checkbox],.j-block__scr .n-main__radio').unbind('click').click(calculator.additional_fields_control);
                $ui.find('.j-replace__value .b-radio__wr label').unbind('click').click(calculator.replace_selection_control);
                $ui.find('input[name="delivery_city"]').change(function(){
                    var $el = $(this);
                    if($el.val() == '1')
                        $ui.find('#b-delivery_region').show();
                    else
                        $ui.find('#b-delivery_region').hide();
                });

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                /* Display text description on the right */
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                /*** Copy selected products and total price from step 4 ***/
                calc.copy_right_info($('#step-4'), $ui);

                /* Default delivery details */
                var ct = property_calculator.contract;
                if (ct.ins_country == '4' && (ct.ins_city == '1' || ct.ins_city == '2')) {
                    $ui.find('label[for="id_delivery_city_'+ct.ins_city+'"]').click();
                    if (ct.ins_city == '1') $ui.find('#b-delivery_region').show();
                    $ui.find('input[name="delivery_street"]').val(ct.ins_street);
                    $ui.find('input[name="delivery_house"]').val(ct.ins_house);
                    $ui.find('input[name="delivery_apartment"]').val(ct.ins_apartment);
                    $ui.find('input[name="delivery_phone"]').val(ct.ins_phone);
                }

                /* Takeout points map */
                //$ui.find('input[name="delivery_type"]').click(function(){
                //    if ($(this).val() == 'takeout') {
                //        var $t_point = $ui.find('input[name="delivery_takeout"]:checked');
                //        listMap($t_point.data('latitude'), $t_point.data('longitude'), $t_point.data('zoom'));
                //    }
                //});

                /* Takeout points */
                //$ui.find('input[name="delivery_takeout"]').unbind('click').click(function(){
                //    var $el = $(this);
                //    listMap($el.data('latitude'), $el.data('longitude'), $el.data('zoom'));
                //});

                /* Следующий этап (оформление) */
                $ui.find('.j-next__click').unbind('click').click(function(){
                    var $el = $(this);
                    // Валидируем указанные поля
                    var flds = ['delivery_type', 'delivery_date', 'delivery_time', 'delivery_city', 'delivery_region',
                        'delivery_street', 'delivery_house', 'delivery_phone', 'delivery_takeout', 'delivery_email',
                        'payment_type'];
                    calculator.show_spinner();
                    $el.attr('disabled', 'disabled');
                    calc.validate_contract(flds, function (has_errors) {
                        if(!has_errors) {
                            // Передаем данные о заказе
                            $.post('/calculator/modal/property/?m=json&cl=issue', property_calculator.contract, function(data){
                                if(!data.has_errors){
                                    workflow.next_stage();
                                    calculator.calc_form('forward', $el);
                                } else
                                    $.confirm({
                                        'title'		: $.t('titleWarning'),
                                        'message'	: $.t('msgTransferError'),
                                        'buttons'	: {
                                            'Ok'	: {
                                                'class'	: 'order confirm-btn confirm-yes',
                                                'action': function(){ }
                                            }
                                        }
                                    });
                                $el.removeAttr('disabled');
                            }).fail(function(){
                                $.confirm({
                                        'title'		: $.t('titleWarning'),
                                        'message'	: $.t('msgTransferError'),
                                        'buttons'	: {
                                            'Ok'	: {
                                                'class'	: 'order confirm-btn confirm-yes',
                                                'action': function(){ }
                                            }
                                        }
                                    });
                                $el.removeAttr('disabled');
                            });
                        }
                    });
                    $el.removeAttr('disabled');
                    calculator.hide_spinner();
                    return false;
                });
                $(document).trigger('step_6_loaded');
            },

            next: function(){
                return 'step_7';
            }
        },

        step_7: {
            init: function(){
                var $calc = $('.n-modal__calk');
                $calc.on('hidden.bs.modal', function(){
                    $calc.unbind('hidden.bs.modal').load('/calculator/modal/ .modal-dialog');
                });
                $(document).trigger('step_7_loaded');
            }
        }
    },

    workflow_restore: function(calculation_id) {
        var $cl = $('.b-calc__block');
        //$cl.find('.b-curtain__modal').show();
        //$cl.find('.b-spinner__modal').show();
        $cl.modal({backdrop: false}).modal('show');

        $.get('/calculator/modal/property/?m=json&cl=restore&id='+calculation_id, function(data){

            $('.j-clr-calcform input[name="id"]').val(data.id);

            // Prepare restoration procedure
            $(document).on('step_2_loaded', function(){
                $(document).off('step_2_loaded');

                setTimeout(function(){
                    $('label[for="realty_type_'+data.realty_type+'"]').trigger('click');
                }, 100);

            });

            $(document).on('substep_2_loaded', function(){
                $(document).off('substep_2_loaded');

                setTimeout(function(){
                    $('label[for="city['+data.city+']"]').trigger('click');
                }, 100);
            });

            $(document).on('substep_3_loaded', function(){
                $(document).off('substep_3_loaded');

                setTimeout(function(){
                    $('.j-clr-calcform').jCleverAPI('selectSetPosition', '[name="branch"]', data.branch);
                    $('#substep-3').find('.j-next__click').trigger('click');
                }, 100);
            });

            $(document).on('substep_4_loaded', function(){
                $(document).off('substep_4_loaded');

                setTimeout(function(){
                    $('.n-cost__realty').find('input[type="text"]').val(data.s_insurance).trigger('change');
                    $('#substep-4').find('.j-next__click').trigger('click');
                }, 100);

            });

            $(document).on('substep_5_loaded', function(){
                 $(document).off('substep_5_loaded');

                setTimeout(function(){
                    $('.n-deductible__realty').find('input[type="text"]').val(data.franchise).trigger('change');
                    $('#substep-5').find('.j-next__click').trigger('click');
                }, 100);
            });

            $(document).on('step_3_loaded', function(){
                $(document).off('step_3_loaded');

                setTimeout(function() {
                    if(data.main_product){
                        $('#step-3').find('.insurance_product__btn[data-product-id="'+data.main_product+'"]').trigger('click');
                    } else {
                        $(document).off('step_4_loaded');
                        $(document).off('step_5_loaded');
                    }
                }, 100);
            });

            $(document).on('step_4_loaded', function(){
                $(document).off('step_4_loaded');

                setTimeout(function() {
                    var $ui = $('#step-4');
                    var restored = false;
                    if(data.p3_inscompany){
                        $ui.find('#id_product_3_'+data.p3_inscompany).trigger('click');
                        property_calculator.workflow_steps.step_4.calculate_total_sum();
                        restored = true;
                    }
                    if(restored)
                        $ui.find('.j-next__click').trigger('click');
                    else
                        $(document).off('step_5_loaded');
                }, 100);
            });

            $(document).on('step_5_loaded', function(){
                $(document).off('step_5_loaded');

                setTimeout(function() {
                    var $ui = $('#step-5');
                    ['n_reestr', 'document_reason', 'address', 'index', 'ins_person_lname', 'ins_person_fname',
                        'ins_person_mname', 'ins_person_pin', 'ins_person_birthday', 'ins_index', 'ins_phone',
                        'ins_email'].forEach(function(name){
                          if(data.hasOwnProperty(name)){
                              $ui.find('input[name="'+name+'"]').val(data[name])
                          }
                        });
                    $ui.find('label[for="id_using_method_'+data.using_method+'"]').trigger('click');
                    $ui.find('label[for="id_ins_country_'+data.ins_country+'"]').trigger('click');
                    $ui.find('label[for="id_ins_person_gender_'+data.ins_person_gender+'"]').trigger('click');
                    if(data.ins_country == '4' || data.ins_country == 4) {
                        $ui.find('label[for="id_ins_city_'+data.ins_city+'"]').trigger('click');
                        $ui.find('input[name="ins_street"]').val(data.ins_street);
                        $ui.find('input[name="ins_house"]').val(data.ins_house);
                        $ui.find('input[name="ins_apartment"]').val(data.ins_apartment);
                    }
                    else {
                        $ui.find('input[name="ins_city_custom"]').val(data.ins_city_custom);
                        $ui.find('input[name="ins_address"]').val(data.ins_address);
                    }
                }, 100);
            });

            // Proceed restoration procedure
            $('.j-ins-type-sel__click[data-ins-type="property"]').trigger('click');
        });

    },

    property_save_click: function(){
        property_calculator.refresh_state();
        property_calculator.refresh_data();
        $.post('/calculator/modal/property/?m=json&cl=save', property_calculator.contract, function(data){
            console.log(data);
        })
    }
};