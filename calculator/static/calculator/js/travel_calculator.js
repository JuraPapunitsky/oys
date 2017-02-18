var travel_calculator = {

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
            p4_selected: false,
            p4_inscompany: null,
            d_start: null,
            d_end: null,
            rest_term_year: false,
            insured_days: null,
            shengen_add: null,

            /* ВЗР */
            countries: [],
            countries_text: '',
            rest_period_text: '',
            rest_type: null,
            rest_type_text: '',
            traveller_first_name: '',
            traveller_last_name: '',
            traveller_middle_name: '',
            traveller_gender: null,
            traveller_birthday: null,
            traveller_pin: '',
            traveller_city: null,
            traveller_address: '',

            ins_value: null,
            embassy: null,
            risk_group: null,
            country_of_departure: null,
            departure_type: null,
            rest_type_extended: null,

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
        return this.contract.countries_text
    },

    get_description: function(){
        var ct = this.contract;
        return ct.rest_type_text + ', ' + ct.rest_period_text + ' (' + ct.insured_days + ')' + ',<br/>' + $.t('birthdayTitle') + ' ' + ct.traveller_birthday;
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
        var calc = travel_calculator;
        var $form = $('.j-clr-calcform');

        // Product select from step-3
        calc.contract['p4_selected'] = false;
        if(calc.contract['main_product'] && calc.contract['main_product'] !== undefined)
            calc.contract['p'+calc.contract['main_product']+'_selected'] = true;

        calc.contract['countries'] = [];
        calc.contract['rest_term_year'] = false;
        var boolFields = ['p4_selected', 'rest_term_year'];
        $form.serializeArray().forEach(function(obj){
            if (obj.name == 'countries') {
                calc.contract['countries'].push(obj.value)
            } else if (boolFields.indexOf(obj.name) >= 0) {
                calc.contract[obj.name] = true
            } else {
                calc.contract[obj.name] = obj.value
            }
        });
    },

    /* Validates {contract} fields via ajax json request */
    validate_contract: function(fields, complete){
        travel_calculator.refresh_state();
        travel_calculator.refresh_data();

        /* Clean up previous errors (removes data-iserror classes and cleans .field-error block spans */
        fields.forEach(function(fld){
            $('.j-clr-calcform').find('input[name="'+fld+'"]').parents('.b-data__line').removeClass('data-iserror').find('.field-error span').html('');
        });

        /* Call 'validate' method via AJAX */
        $.post('/calculator/modal/travel/?m=json&cl=validate', travel_calculator.contract, function(result){
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
    travel_edit_click: function(){
        if(workflow.rollback_stage('substep_4')) {
            $('.n-form__step').removeClass('e-active');
            $('#step-2').addClass('e-active');
        }
    },

    /* Copy selected products and total price */
    copy_right_info: function($source_step, $target_step){
        ['.p4__detail', '.delivery__detail'].forEach(function(cls){
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
        $.mask.definitions['&'] = '[A-Za-z ]';

        $('#id_ins_person_pin, #id_traveller_pin').mask('*******');
        $('#id_ins_person_fname, #id_ins_person_lname').mask('?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@');
        $('#id_ins_person_mname').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_street, #id_delivery_street').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_phone, #id_delivery_phone').mask('?############');
        $('#id_index').mask('AZ####');
        $('#id_ins_index').mask(travel_calculator.contract.ins_country == '4' ? 'AZ####' : '######');
        $('#id_traveller_first_name, #id_traveller_last_name, #id_traveller_middle_name').mask('?&&&&&&&&&&&&&&&&&&&&&');
        $('#id_d_start, #id_d_end, #id_traveller_birthday, #id_ins_person_birthday, #id_delivery_date').mask('##.##.####');
    },

    /* Vehicle contracts calculation steps */
    workflow_steps: {
        /* Rest country selection */
        substep_1: {
            load: function(){
                var $ui = $('#substep-1');

                $ui.find('.b-radio__wr input').unbind('change').change(function () {
                    var countries = [];
                    var countries_text = [];
                    $ui.find('input:checked').each(function (index) {
                        countries.push($(this).val());
                        countries_text.push($(this).data('value'));
                    });

                    if (_.indexOf(countries, $(this).val()) >= 0) {
                        $(this).next().addClass('active')
                    } else {
                        $(this).next().removeClass('active')
                    }

                    travel_calculator.contract.countries = countries;

                    travel_calculator.contract.countries_text = countries_text.join(', ');
                    $ui.find('.badge-text').val(travel_calculator.contract.countries_text);
                });

                $ui.find('.j-next__click').unbind('click').click(function () {
                    var $el = $(this);
                    workflow.next_stage();
                    calculator.calc_form('subst', $el);
                });
            },
            init: function(){
                $(document).trigger('substep_1_loaded')
            },
            rollback: function(){
                var ct = travel_calculator.contract;
                ct['countries'] = [];
                ct['countries_text'] = '';
            },
            next: function() { return 'substep_2' }
        },

        /* Rest start date selection */
        substep_2: {
            next_step: function () {
                var calc = travel_calculator;
                var $ui = $('#substep-2');
                var $el = $(this);

                var $d_end = $ui.find('[name="d_end"]');
                var d_end_is_disabled = $d_end.attr('disabled') === 'disabled';
                if (d_end_is_disabled) $d_end.removeAttr('disabled');

                calc.validate_contract(['rest_term_year', 'd_start', 'd_end'], function (has_errors) {
                    if (!has_errors) {
                        calc.contract.rest_period_text = calc.contract.d_start + ' - ' + calc.contract.d_end;
                        $ui.find('.badge-text-wr input').val(calc.contract.rest_period_text);
                        workflow.next_stage();
                        calculator.calc_form('subst', $el);
                    } else {
                        if (d_end_is_disabled) $d_end.attr('disabled', 'disabled');
                    }
                });
            },

            load: function(){
                var $ui = $('#substep-2');
                var ct = travel_calculator.contract;

                ct.csrfmiddlewaretoken = $ui.parents('.j-clr-calcform').find('input[name="csrfmiddlewaretoken"]').val();
                $.post('/calculator/modal/travel/?m=json&cl=shengen_add', ct, function(data) {
                    ct.shengen_add = data.shengen_add
                })
            },
            init: function() {
                var $ui = $('#substep-2');

                travel_calculator.init_field_masks();
                var $d_start = $ui.find('[name="d_start"]');
                var $d_end = $ui.find('[name="d_end"]');
                var $rest_term_year = $ui.find('[name="rest_term_year"]');

                $d_start.datepicker('option', 'onSelect', function() {$d_start.trigger('change')});
                $d_end.datepicker('option', 'onSelect', function() {$d_end.trigger('change')});

                $d_start.on('change', function() {
                    var start_date = $d_start.datepicker('getDate');
                    var end_date = null;
                    if($rest_term_year.prop('checked')) {
                        end_date = moment(start_date).add(1, 'year').subtract(1, 'day');
                        $d_end.datepicker('setDate', end_date._d);
                    } else {
                        end_date = $d_end.datepicker('getDate');
                        if (moment.range(start_date, end_date).diff('days') > 90) {
                            $d_end.datepicker('setDate', moment(start_date).add(90, 'day')._d)
                        }
                    }
                });

                $d_end.on('change', function() {
                    var start_date = $d_start.datepicker('getDate');
                    var end_date = $d_end.datepicker('getDate');
                    console.log(start_date);
                    console.log(end_date);
                    console.log(moment.range(start_date, end_date).diff('days') > 90);
                    if(!$rest_term_year.prop('checked') && moment.range(start_date, end_date).diff('days') > 90) {
                        $d_end.datepicker('setDate', moment(start_date).add(90, 'day')._d)
                    }
                });

                $rest_term_year.on('change', function() {
                    if ($(this).prop('checked')) {
                        $d_end.attr('disabled', 'disabled');
                        $d_start.trigger('change');
                    } else {
                        $d_end.removeAttr('disabled');
                    }
                });
                $ui.find('.j-next__click').unbind('click').on('click', this.next_step);

                $(document).trigger('substep_2_loaded');
            },
            rollback: function(){
                var ct = travel_calculator.contract;
                ct.d_start = null;
                ct.d_end = null;
                ct.rest_term_year = false;
                ct.rest_period_text = '';
            },
            next: function() {
                return 'substep_3'
            }
        },

        substep_3: {
            load: function() {
                var ct = travel_calculator.contract;
                var $ui = $('#substep-3');

                // Insured days slider initialization
                var $inp = $('input[name="insured_days"]');
                var insured_days_opt = {};
                if (ct.rest_term_year) {
                    insured_days_opt = {range: 'min', step: 1, min: 15, max: 365, value: 90};
                    $inp.removeAttr('readonly');
                } else {
                    var insuredDays = moment.range(
                        $('[name="d_start"]').datepicker('getDate'),
                        $('[name="d_end"]').datepicker('getDate')
                    ).diff('days') + 1;
                    insured_days_opt = {range: 'min', step: insuredDays, min: insuredDays, max: insuredDays, value: insuredDays};
                    $inp.attr('readonly', 'readonly')
                }
                $ui.find('.b-slider').slider(insured_days_opt);
                calculator.slider_input_default_set($inp);
                calculator.slider_ui_blocks_init($ui.find('.b-style__slider'), '');

                // Next step button actions
                $ui.find('.j-next__click').unbind('click').click(function(){
                    ct.insured_days = parseInt($inp.val());
                    if(workflow.next_stage()) calculator.calc_form('subst', $(this));
                });
            },
            init: function() {
                $(document).trigger('substep_3_loaded');
            },
            rollback: function() {
                var ct = travel_calculator.contract;
                ct.insured_days = null;
            },
            next: function() {
                return 'substep_4'
            }
        },

        /* Rest type selection */
        substep_4: {
            load: function(){
                var ct = travel_calculator.contract;
                var $ui = $('#substep-4');

                $ui.find('.j-next__click').unbind('click').click(function(){
                    var $sel_opt = $ui.find('[name="rest_type"] :selected');
                    ct.rest_type = parseInt($sel_opt.val());
                    ct.rest_type_text = $sel_opt.text();
                    calculator.calc_form('subst', $(this));
                    workflow.next_stage();
                });
            },
            init: function(){
                $(document).trigger('substep_4_loaded')
            },
            rollback: function(){
                travel_calculator.contract.rest_type = null;
                travel_calculator.contract.rest_type_text = '';
            },
            next: function() { return 'substep_5' }
        },

        /* Deductible selection */
        substep_5: {
            load: function(){
                var $ui = $('#substep-5');

                travel_calculator.init_field_masks();
                $ui.find('.j-next__click').unbind('click').click(function () {
                    var $el = $(this);
                    travel_calculator.validate_contract(['traveller_birthday'], function (has_errors) {
                        if (!has_errors) {
                            workflow.next_stage();
                            calculator.calc_form('forward', $el);
                        }
                    });
                });
            },

            init: function() {
                $(document).trigger('substep_5_loaded')
            },

            rollback: function(){
                travel_calculator.contract.traveller_birthday = null;
            },

            next: function() { return 'step_3' }
        },

        step_3: {
            load: function(){

                calculator.show_spinner();
                var ct = travel_calculator.contract;
                var $ui = $('#step-3');

                ct.csrfmiddlewaretoken = $ui.parents('.j-clr-calcform').find('input[name="csrfmiddlewaretoken"]').val();

                $.post('/calculator/modal/travel/?m=ajax&cl=precalculate', ct, function(data){

                    $ui.find('.b-form__left').html(data).find('.insurance_product__btn').unbind('click')
                        .click(function() {
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
                    calculator.ajax_fail_dialog_factory(travel_calculator.workflow_steps.step_3.load)
                );
            },

            init: function(){
                var $ui = $('#step-3');
                var calc = travel_calculator;
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
            validated_fields: ['p4_selected'],

            /* Load product matrix */
            load_product_matrix: function () {
                var calc = travel_calculator;
                var step_obj = travel_calculator.workflow_steps.step_4;

                calc.validate_contract(step_obj.validated_fields, function(has_errors){
                    if (!has_errors) {

                        calculator.show_spinner();
                        $.post('/calculator/modal/travel/?m=ajax&cl=calculate&spr=4', calc.contract, function (data) {

                            var $tariff_table = $('.b-sigorta__table');

                            // Product - company selection controls
                            $tariff_table.html(data).find('input[type="radio"]').unbind('click').click(function () {
                                calc.contract[$(this).attr('name')] = $(this).val();
                                calculator.calculate_total_sum($('#step-4'))
                            });

                            // Auto select companies
                            [4].forEach(function (product_id) {
                                calculator.auto_select_companies(calc.contract, $tariff_table, product_id)
                            });

                            $('#step-4 .b-info__text').html(calc.get_description());
                            calculator.calculate_total_sum($('#step-4'));

                            calculator.hide_spinner();

                        }).fail(
                            calculator.ajax_fail_dialog_factory(travel_calculator.workflow_steps.step_4.load_product_matrix)
                        );

                    }
                });
            },

            /*** Workflow properties ***/

            init: function(){
                var step_obj = this;
                var $ui = $('#step-4');
                var $tariff_table = $ui.find('.b-sigorta__table');
                var calc = travel_calculator;

                /*** Контролы этапа (параметры продуктов) вызывают расчет матрицы продуктов ***/
                $ui.find('.b-step-4__options input').unbind('change').change(step_obj.load_product_matrix);

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                // Right infos
                $ui.find('.b-step__title h2').html(calc.contract.main_product_text);
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                // Insurance company selection
                $tariff_table.find('input[type="radio"]').unbind('click').click(function () {
                    calc.contract[$(this).attr('name')] = $(this).val();
                    calculator.calculate_total_sum($('#step-4'));
                });

                // Schengen warning
                if (calc.contract.shengen_add == 3 || calc.contract.shengen_add == 15) {
                    $ui.find('#schengen-warning').removeClass('hidden').find('span').html(calc.contract.shengen_add)
                } else {
                    $ui.find('#schengen-warning').addClass('hidden').find('span').html('')
                }

                // Auto select company
                calculator.auto_select_companies(calc.contract, $tariff_table, calc.contract.main_product);

                // Calculate total sum
                calculator.calculate_total_sum($ui);

                $ui.find('.j-next__click').unbind('click').click(function () {
                    var $el = $(this);
                    calc.validate_contract(step_obj.validated_fields, function(has_errors){
                        if(!has_errors) {
                            if(workflow.next_stage()) calculator.calc_form('forward', $el);
                        }
                    });
                });

                $(document).trigger('step_4_loaded');
            },

            next: function(){ return 'step_5' }
        },

        step_5: {
            /*** Workflow properties ***/
            init: function(){
                var step = this;
                var $ui = $('#step-5');
                var calc = travel_calculator;
                var insurance_company_id = calc.contract.p4_inscompany;

                calculator.right_panel_scroll();

                /* Display text description on the right */
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                /* Field masks initialization */
                calc.init_field_masks();

                /* Hide fields traveller fields (first name, last name, middle name) and fill insurer birthday */
                var $axa_traveller_inputs = $ui.find('#id_traveller_pin,#id_traveller_address,#id_traveller_city');
                if (insurance_company_id == '11') {
                    $axa_traveller_inputs.closest('.b-data__line').show();
                } else {
                    $axa_traveller_inputs.closest('.b-data__line').hide();
                }

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
                        'layer-1': ['embassy'],
                        'layer-2': ['ins_person_pin', 'ins_person_fname', 'ins_person_lname', 'ins_person_mname', 'ins_person_gender',
                            'ins_person_birthday', 'ins_index', 'ins_country', 'ins_city', 'ins_city_custom', 'ins_address',
                            'ins_street', 'ins_house', 'ins_apartment', 'ins_phone', 'ins_email'],
                        'layer-3': ['traveller_first_name', 'traveller_last_name', 'traveller_middle_name',
                            'traveller_gender', 'traveller_n_passport']
                    };

                    if (insurance_company_id == '11')
                        flds['layer-3'] = flds['layer-3'].concat(['traveller_pin', 'traveller_address', 'traveller_city']);

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
                var calc = travel_calculator;
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
                var ct = travel_calculator.contract;
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
                            $.post('/calculator/modal/travel/?m=json&cl=issue', travel_calculator.contract, function(data){
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
    }

};