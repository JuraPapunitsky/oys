var vehicle_calculator = {

    contract: {},

    /* Init contract object */
    init_contract: function(){
        vehicle_calculator.contract = {
            csrfmiddlewaretoken:'',
            step: '',
            substep: '',
            layer: '',
            /**/
            main_product: null,
            main_product_text: '',
            p2_selected: false,
            p11_selected: false,
            p12_selected: false,
            d_start: null,
            term_insurance: null,
            /* ТС */
            auto_type: '',
            auto_type_text: '',
            auto_mark: '',
            auto_mark_text: '',
            auto_model: '',
            auto_model_text: '',
            auto_engine_capacity: '',
            auto_engine_capacity_text: '',
            auto_payload: '',
            auto_payload_text: '',
            cnt_seats: '',
            cnt_seats_text: '',
            auto_createyear: '',
            auto_createyear_text: '',
            auto_vin: '',
            auto_engine: '',
            auto_chassis: '',
            auto_number: '',
            auto_region: '',
            auto_region_text: '',
            auto_cost: '',
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
            /* Для проекта 2 */
            p2_inscompany: null,
            ateshgah_icbariplus: false,
            ateshgah_superkasko: false,
            ateshgah_beshlik: false,
            /* Для проекта 11 */
            p11_has_errors: false,
            p11_inscompany: null,
            p11_product_option: null,
            p11_beneficiary: null,
            p11_bank_beneficiary: null,
            /* Для проекта 12 */
            p12_has_errors: false,
            p12_inscompany: null,
            p12_beneficiary: null,
            p12_bank_beneficiary: null,
            p12_deductible: null,
            insurance_coverage: null,
            accidents_quantity: null,
            evacuation: false,
            cvi_extension_sum: null,
            accident_ins_sum: null,
            accident_ins_drivers: null,
            additional_drivers: false,
            additional_driver_2: false,
            /* Для 12 проекта - владелец */
            ins_owner: true,
            owner_pin: '',
            owner_fname: '',
            owner_lname: '',
            owner_mname: '',
            owner_gender: null,
            owner_birthday: null,
            owner_country: null,
            owner_city: null,
            owner_city_custom: '',
            owner_address: '',
            owner_index: '',
            owner_street: '',
            owner_house: '',
            owner_apartment: '',
            owner_phone: '',
            owner_email: '',
            /* Для 12 проекта - доп водитель 1 */
            ad1_pin: '',
            ad1_fname: '',
            ad1_lname: '',
            ad1_mname: '',
            ad1_gender: null,
            ad1_birthday: null,
            ad1_country: null,
            ad1_city: null,
            ad1_city_custom: '',
            ad1_address: '',
            ad1_index: '',
            ad1_street: '',
            ad1_house: '',
            ad1_apartment: '',
            ad1_phone: '',
            ad1_email: '',
            /* Для 12 проекта - доп водитель 2 */
            ad2_pin: '',
            ad2_fname: '',
            ad2_lname: '',
            ad2_mname: '',
            ad2_gender: null,
            ad2_birthday: null,
            ad2_country: null,
            ad2_city: null,
            ad2_city_custom: '',
            ad2_address: '',
            ad2_index: '',
            ad2_street: '',
            ad2_house: '',
            ad2_apartment: '',
            ad2_phone: '',
            ad2_email: '',
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
            payment_type: '',
            transaction_id: '',
            s_premium: null,
        };
    },

    get_title: function(){
        var ct = vehicle_calculator.contract;
        return ct.auto_mark_text + ' ' + ct.auto_model_text;
    },

    get_description: function(){
        var ct = vehicle_calculator.contract;
        var descr = ct.auto_createyear_text + ', '+ct.auto_type_text+', ';
        switch (ct.auto_type) {
            case '2': descr += ct.cnt_seats_text + ', '; break;
            case '4': descr += ct.auto_engine_capacity_text + ', '; break;
            case '6': descr += ct.auto_payload_text + ', '; break;
            default: break;
        }
        descr += '<br/>' + ct.auto_cost + '&nbsp;AZN';
        return descr;
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
        var calc = vehicle_calculator;
        var $form = $('.j-clr-calcform');

        // Product select from step-3
        calc.contract.p2_selected = false;
        calc.contract.p11_selected = false;
        calc.contract.p12_selected = false;
        if(calc.contract.main_product && calc.contract.main_product !== undefined)
            calc.contract['p'+calc.contract.main_product+'_selected'] = true;

        calc.contract['ins_owner'] = false;
        calc.contract['evacuation'] = false;
        calc.contract['additional_drivers'] = false;
        calc.contract['additional_driver_2'] = false;

        var boolFields = ['p2_selected', 'p11_selected', 'p12_selected', 'evacuation', 'ins_owner',
            'additional_drivers', 'additional_driver_2', 'ateshgah_beshlik', 'ateshgah_icbariplus',
            'ateshgah_superkasko'];
        $form.serializeArray().forEach(function(obj){
            if (boolFields.indexOf(obj.name) >= 0) {
                calc.contract[obj.name] = true;
            } else {
                calc.contract[obj.name] = obj.value;
            }
        });

        if ( !(calc.contract.p2_selected && calc.contract.p2_inscompany == '1') ) {
            ['ateshgah_beshlik', 'ateshgah_icbariplus', 'ateshgah_superkasko'].forEach(function(val) {
                calc.contract[val] = false
            })
        }
    },

    /* Validates {contract} fields via ajax json request */
    validate_contract: function(fields, complete){
        vehicle_calculator.refresh_state();
        vehicle_calculator.refresh_data();

        /* Clean up previous errors (removes data-iserror classes and cleans .field-error block spans */
        fields.forEach(function(fld){
            $('.j-clr-calcform').find('input[name="'+fld+'"]').parents('.b-data__line').removeClass('data-iserror').find('.field-error span').html('');
        });

        /* Call 'validate' method via AJAX */
        $.post('/calculator/modal/vehicle/?m=json&cl=validate', vehicle_calculator.contract, function(result){
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

    /* Get array of selected products ids */
    get_selected_products: function(){
        var sel_products = [];
        if(this.contract.main_product) this.contract['p'+this.contract.main_product+'_selected'] = true;
        if(this.contract.p2_selected) sel_products.push('2');
        if(this.contract.p11_selected) sel_products.push('11');
        if(this.contract.p12_selected) sel_products.push('12');
        return sel_products
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
        $('#id_ins_person_pin, #id_owner_pin, #id_ad1_pin, #id_ad2_pin').mask('*******');
        $('#id_ins_person_fname, #id_ins_person_lname, #id_owner_fname, #id_owner_lname, #id_ad1_fname, #id_ad1_lname, #id_ad2_fname, #id_ad2_lname').mask('?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@');
        $('#id_ins_person_mname,#id_owner_mname, #id_ad1_mname, #id_ad2_mname').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_street ,#id_owner_street, #id_ad1_street, #id_ad2_street, #id_delivery_street').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_phone, #id_owner_phone, #id_ad1_phone, #id_ad2_phone, #id_delivery_phone').mask('?############');
        //$('#id_ins_index, #id_owner_index, #id_ad1_index, #id_ad2_index').mask('######');
        $('#id_ins_index').mask(vehicle_calculator.contract.ins_country == '4' ? 'AZ####' : '######');
        $('#id_owner_index').mask(vehicle_calculator.contract.owner_country == '4' ? 'AZ####' : '######');
        $('#id_ad1_index').mask(vehicle_calculator.contract.ad1_country == '4' ? 'AZ####' : '######');
        $('#id_ad2_index').mask(vehicle_calculator.contract.ad2_country == '4' ? 'AZ####' : '######');
        $('#id_d_start, #id_owner_birthday, #id_ad1_birthday, #id_ad2_birthday, #id_ins_person_birthday, #id_delivery_date').mask('##.##.####');
    },

    /* Back to vehicle details edit (to last sub step) */
    vehicle_edit_click: function() {
        if(workflow.rollback_stage('substep_7')) {
            $('.n-form__step').removeClass('e-active');
            $('#step-2').addClass('e-active');
        }
    },

    /* Copy selected products and total price */
    copy_right_info: function($source_step, $target_step){
        ['.p2__detail', '.p11__detail', '.p12__detail', '.delivery__detail', '.ateshgah_icbariplus__detail',
            '.ateshgah_superkasko__detail', '.ateshgah_beshlik__detail'].forEach(function(cls){
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

    /* Vehicle contracts calculation steps */
    workflow_steps: {

        /* Vehicle type selection */
        substep_1: {

            load: function(){
                $('#substep-1').find('.b-radio__wr label').unbind('click').click(
                    calculator.get_substep_callback(vehicle_calculator.contract, 'auto_type', 'auto_type_text')
                );
            },

            init: function() {
                $(document).trigger('substep_1_loaded');
            },

            rollback: function(){
                var ct = vehicle_calculator.contract;
                ct['auto_type'] = null;
                ct['auto_type_text'] = '';
            },

            next: function() { return 'substep_2' }
        },

        /* Vehicle brand selection */
        substep_2: {
            load: function(){
                var ct = vehicle_calculator.contract;
                calculator.show_spinner();
                $.get('/calculator/modal/vehicle/?m=ajax&cl=auto_mark&vt='+ct.auto_type, {}, function(data){
                    $('#substep-2').html(data).find('.b-radio__wr label').unbind('click').click(
                        calculator.get_substep_callback(ct, 'auto_mark', 'auto_mark_text')
                    );
                    calculator.hide_spinner();
                    $(document).trigger('substep_2_loaded');
                });
            },

            rollback: function(){
                $('#substep-2').html('');
                var ct = vehicle_calculator.contract;
                ct['auto_mark'] = null;
                ct['auto_mark_text'] = '';
            },

            next: function() { return 'substep_3' }
        },

        /* Vehicle model selection */
        substep_3: {

            load: function() {
                var ct = vehicle_calculator.contract;
                calculator.show_spinner();
                $.get('/calculator/modal/vehicle/?m=ajax&cl=auto_model&vt='+ct.auto_type+'&vb='+ct.auto_mark, {}, function(data){
                    $('#substep-3').html(data).find('.b-radio__wr label').unbind('click').click(
                        calculator.get_substep_callback(ct, 'auto_model', 'auto_model_text')
                    );
                    calculator.hide_spinner();
                    $(document).trigger('substep_3_loaded');
                })
            },

            rollback: function() {
                $('#substep-3').html('');
                var ct = vehicle_calculator.contract;
                ct['auto_model'] = null;
                ct['auto_model_text'] = '';
            },

            next: function() {
                var ct = vehicle_calculator.contract;
                switch (ct.auto_type) {
                    case '2': return 'substep_4';
                    case '4': return 'substep_4';
                    case '6': return 'substep_4';
                    default: return 'substep_5'
                }
            }
        },

        /* Vehicle engine / seats / payload selection */
        substep_4: {

            load: function(){
                var ct = vehicle_calculator.contract;
                var source_name = null;
                switch(ct.auto_type){
                    case '2': source_name = 'cnt_seats'; break;
                    case '6': source_name = 'auto_payload'; break;
                    case '4': source_name = 'auto_engine_capacity'; break;
                    default: break;
                }
                if (source_name != null) {
                    calculator.show_spinner();
                    $.get('/calculator/modal/vehicle/?m=ajax&cl=' + source_name, {}, function (data) {
                        $('#substep-4').html(data).find('.b-radio__wr label').unbind('click').click(
                            calculator.get_substep_callback(ct, source_name, source_name + '_text')
                        );
                        calculator.hide_spinner();
                        $(document).trigger('substep_4_loaded');
                    });
                }

            },

            rollback: function(){
                $('#substep-4').html('');
                var ct = vehicle_calculator.contract;
                var source_name = null;
                switch(ct.auto_type){
                    case '2': source_name = 'cnt_seats'; break;
                    case '6': source_name = 'auto_payload'; break;
                    case '4': source_name = 'auto_engine_capacity'; break;
                    default: break;
                }
                if(source_name != null) {
                    ct[source_name] = null;
                    ct[source_name+'_text'] = '';
                }
            },

            next: function() { return 'substep_5' }
        },

        /* Vehicle create year selection */
        substep_5: {

            load: function(){
                var ct = vehicle_calculator.contract;
                calculator.show_spinner();
                $.get('/calculator/modal/vehicle/?m=ajax&cl=auto_year', {}, function(data){
                    $('#substep-5').html(data).find('.b-radio__wr label').unbind('click').click(
                        calculator.get_substep_callback(ct, 'auto_createyear', 'auto_createyear_text')
                    );
                    // Коррекция интерфейса (дополнительное переключение суб этапа) если тип ТС: мото, прицеп или спецтехника
                    if(ct.auto_type == '3' || ct.auto_type == '5' || ct.auto_type == '8') {
                        calculator.calc_form('subst', $('#substep-4').html('<div id="substep-4-dummy"></div>').find('#substep-4-dummy'));
                    }

                    calculator.hide_spinner();
                    $(document).trigger('substep_5_loaded');
                })
            },

            rollback: function(){
                $('#substep-5').html('');
                var ct = vehicle_calculator.contract;
                ct['auto_createyear'] = null;
                ct['auto_createyear_text'] = '';
            },

            next: function() { return 'substep_6' }
        },

        /* Vehicle cost selection */
        substep_6: {
            load: function(){
                var $ui = $('#substep-6');
                var $sl = $ui.find('.b-slider');
                var $inp = $('input[name="auto_cost"]');
                $inp.unbind('change').change(function(){
                    if(parseInt($inp.val()) > 200000 || parseInt($inp.val()) < 1000) {
                        $inp.val(parseInt($inp.val()) > 200000 ? '200000' : '1000');
                        $sl.slider('value', $inp.val());
                        var left_pos = $sl.find('.ui-slider-handle').position().left;
                        $inp.css({left: left_pos});
                    }
                });

                $ui.find('.j-next__click').unbind('click').click(function(){
                    if(workflow.next_stage()) calculator.calc_form('subst', $(this));
                });
            },

            init: function(){
                $(document).trigger('substep_6_loaded');
            },

            rollback: function(){
                vehicle_calculator.contract.auto_cost = null;
            },

            next: function(){
                return 'substep_7'
            }
        },

        /* Person FIN input */
        substep_7: {
            init: function () {
                var $ui = $('#substep-7');
                var calc = vehicle_calculator;

                $ui.find('.j-next__click').unbind('click').click(function () {
                    var $el = $(this);
                    calc.validate_contract(['ins_person_pin'], function (has_errors) {
                        if(!has_errors) {
                            if(workflow.next_stage()) calculator.calc_form('forward', $el);
                        }
                    });
                });

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                /* Field masks initialization */
                calc.init_field_masks();
                $(document).trigger('substep_7_loaded');
            },

            rollback: function () {
                vehicle_calculator.contract.ins_person_pin = null;
                $('.b-ins_person_pin').removeClass('data-iserror');
            },

            next: function(){
                return 'step_3'
            }
        },

        /* Vehicle insurance product selection */
        step_3: {
            load: function(){

                calculator.show_spinner();
                var ct = vehicle_calculator.contract;
                var $ui = $('#step-3');

                $.post('/calculator/modal/vehicle/?m=ajax&cl=precalculate', ct, function(data){

                    $ui.find('.b-form__left').html(data).find('.insurance_product__btn').unbind('click').click(function () {
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
                    calculator.ajax_fail_dialog_factory(vehicle_calculator.workflow_steps.step_3.load)
                );
            },

            init: function(){
                var $ui = $('#step-3');
                var calc = vehicle_calculator;
                // Display text description on the right
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());
            },

            rollback: function() {
                var $ui = $('#step-3');
                vehicle_calculator.contract.main_product = null;
                vehicle_calculator.contract.main_product_text = '';
                vehicle_calculator.contract.p2_selected = false;
                vehicle_calculator.contract.p11_selected = false;
                vehicle_calculator.contract.p12_selected = false;
            },

            next: function() { return 'step_4' }
        },

        /* Additional options selection */
        step_4: {

            /*** Custom properties ***/
            /* Init Ateshgah options block */
            init_ateshgah_options: function () {
                var $ui = $('#step-4');
                var calc = vehicle_calculator;
                if (calc.contract.p2_selected && calc.contract.p2_inscompany == '1') {
                    $ui.find('#ateshgah-options').show();
                } else {
                    $ui.find('#ateshgah-options').hide();
                    $ui.find('#ateshgah-options input').prop('checked', false);
                }
            },

            /* Load product matrix */
            load_product_matrix: function () {
                var calc = vehicle_calculator;
                var step_obj = vehicle_calculator.workflow_steps.step_4;

                var stage_flds = ['p2_selected', 'p11_selected', 'p12_selected', 'p11_product_option',
                        'p11_beneficiary', 'p11_bank_beneficiary', 'insurance_coverage', 'accidents_quantity', 'p12_deductible',
                        'p12_beneficiary', 'p12_bank_beneficiary', 'cvi_extension_sum', 'accident_ins_sum',
                        'accident_ins_drivers'];

                calc.validate_contract(stage_flds, function(has_errors){
                    if (!has_errors) {

                        var selected_pr = calc.get_selected_products();
                        calculator.show_spinner();
                        $.post('/calculator/modal/vehicle/?m=ajax&cl=calculate&spr=' + selected_pr.join(','), calc.contract, function (data) {
                            var $ui = $('#step-4');
                            var $tariff_table = $ui.find('.b-sigorta__table');

                            // Product - company selection controls
                            $tariff_table.html(data).find('input[type="radio"]').unbind('click').click(function () {
                                calc.contract[$(this).attr('name')] = $(this).val();
                                step_obj.init_ateshgah_options();
                                calculator.calculate_total_sum($('#step-4'));
                            });

                            // Auto select companies and calculate total sum
                            selected_pr.forEach(function(product_id) {
                                calculator.auto_select_companies(calc.contract, $tariff_table, product_id)
                            });

                            calculator.calculate_total_sum($ui);
                            calculator.hide_spinner();

                        }).fail(
                            calculator.ajax_fail_dialog_factory(vehicle_calculator.workflow_steps.step_4.load_product_matrix)
                        );

                    }
                });
            },

            /*** Workflow properties ***/

            load: function() {
                var step_obj = this;
                var calc = vehicle_calculator;
                calculator.show_spinner();
                $.get('/calculator/modal/vehicle/?m=ajax&cl=options&pr='+calc.contract.main_product+'&auto_type='+calc.contract.auto_type, {}, function(data){

                    var $ui = $('#step-4');
                    var $tariff_table = $ui.find('.b-sigorta__table');
                    var $step_options = $('.b-step-4__options').html(data);

                    /*** Контролы этапа (параметры продуктов) вызывают расчет матрицы продуктов ***/
                    $step_options.find('input').unbind('change').change(step_obj.load_product_matrix);

                    /*** Дополнительные опции продуктов ***/
                    $ui.find('input[name="p2_selected"],input[name="p11_selected"],input[name="p12_selected"]').unbind('click').click(function () {
                        $('.'+$(this).attr('name')+'__scr')[$(this).prop('checked') ? 'fadeIn' : 'fadeOut'](200);
                    });

                    /*** Количество застрахованных по НС ***/
                    $ui.find('input[name="accident_ins_sum"]').unbind('change').change(function () {
                        $('.b-accident_ins_drivers')[$(this).val() != '' ? 'fadeIn' : 'fadeOut'](200);
                        step_obj.load_product_matrix();
                    });

                    /*** Дополнительние опции ***/
                    $ui.find('.j-more__options-link').click(function () {
                        $(this).next('.b-more__options').fadeToggle();
                    });

                    /*** Открыть доп. поля ***/
                    $ui.find('.j-block__scr input[type=checkbox],.j-block__scr .n-main__radio').unbind('click').click(calculator.additional_fields_control);

                    /*** Выбор банка (замена текста) ***/
                    $ui.find('.j-replace__value .b-radio__wr label').unbind('click').click(calculator.replace_selection_control2);

                    /*** Открыть подсказку ***/
                    $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                    // TODO: это дублирующийся кусок кода, дубль в load_product_matrix()
                    // Product - company selection controls
                    $tariff_table.find('input[type="radio"]').unbind('click').click(function () {
                        calc.contract[$(this).attr('name')] = $(this).val();
                        step_obj.init_ateshgah_options();
                        calculator.calculate_total_sum($('#step-4'))
                    });

                    // Auto select companies and calculate total sum
                    calculator.auto_select_companies(calc.contract, $tariff_table, calc.contract.main_product);
                    step_obj.init_ateshgah_options();
                    calculator.calculate_total_sum($ui);

                    calculator.hide_spinner();
                    $(document).trigger('step_4_loaded');

                }).fail(
                    calculator.ajax_fail_dialog_factory(vehicle_calculator.workflow_steps.step_4.load)
                );


            },

            init: function(){
                var $ui = $('#step-4');
                var calc = vehicle_calculator;

                // Step title
                $ui.find('.b-step__title h2').html(calc.contract.main_product_text);

                // Display text description on the right
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                // Products compare
                $ui.find('.j-compare__click').unbind('click').click(function() {
                    var $ps = $('.b-calc__block #step-3');
                    var prices = {};
                    _.each([2, 11, 12], function (val) {
                        prices[val] = $ps.find('[data-product-id="'+val+'"]').data('product-price')
                    });
                    compare_box_show('vehicle', '?p2='+prices[2]+'&p11='+prices[11]+'&p12='+prices[12])
                });

                $ui.find('.j-next__click').unbind('click').click(function(){
                    var $el = $(this);
                    var stage_flds = ['p2_selected', 'p11_selected', 'p12_selected', 'p11_product_option',
                        'p11_beneficiary', 'p11_bank_beneficiary', 'insurance_coverage', 'accidents_quantity', 'p12_deductible',
                        'p12_beneficiary', 'p12_bank_beneficiary', 'cvi_extension_sum', 'accident_ins_sum',
                        'accident_ins_drivers'];

                    calc.validate_contract(stage_flds, function(has_errors){
                        if(!has_errors) {
                            if(workflow.next_stage()) calculator.calc_form('forward', $el);
                        }
                    });

                })
            },

            rollback: function(){
                $('#step-4 .b-step-4__options').html('')
            },

            next: function(){ return 'step_5' }
        },

        /* Insurer info, etc. */
        step_5: {
            /*** Custom properties ***/

            /*** Workflow properties ***/
            init: function(){
                var step = this;
                var $ui = $('#step-5');
                var calc = vehicle_calculator;

                calculator.right_panel_scroll();

                /* Display text description on the right */
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

                /* Field masks initialization */
                calc.init_field_masks();

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                /*** Открыть доп. поля ***/
                $ui.find('.j-block__scr input[type=checkbox],.j-block__scr .n-main__radio').unbind('click').click(calculator.additional_fields_control);

                /*** Выбор (замена текста) ***/
                $ui.find('.j-replace__value .b-radio__wr label').unbind('click').click(calculator.replace_selection_control);

                /* Блоки изменение блоков адресов при изменении страны */
                $ui.find('input[name="ins_country"],input[name="owner_country"],input[name="ad1_country"],input[name="ad2_country"]').unbind('change').change(function(){
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
                        'layer-1': ['auto_vin', 'auto_engine', 'auto_chassis', 'auto_number', 'auto_region'],
                        'layer-2': ['term_insurance', 'd_start'],
                        'layer-3': ['ins_person_fname', 'ins_person_lname', 'ins_person_mname', 'ins_person_gender',
                            'ins_person_birthday', 'ins_index', 'ins_country', 'ins_city', 'ins_city_custom', 'ins_address',
                            'ins_street', 'ins_house', 'ins_apartment', 'ins_phone', 'ins_email'],
                        'layer-4': ['owner_fname', 'owner_lname', 'owner_mname', 'owner_gender', 'owner_birthday',
                            'owner_pin', 'owner_country', 'owner_city', 'owner_city_custom', 'owner_address',
                            'owner_index', 'owner_street', 'owner_house', 'owner_apartment', 'owner_phone',
                            'owner_email'],
                        'layer-5': ['ad1_fname', 'ad1_lname', 'ad1_mname', 'ad1_gender', 'ad1_birthday',
                            'ad1_pin', 'ad1_country', 'ad1_city', 'ad1_city_custom', 'ad1_address', 'ad1_index',
                            'ad1_street', 'ad1_house', 'ad1_apartment', 'ad1_phone', 'ad1_email', 'ad2_fname',
                            'ad2_lname', 'ad2_mname', 'ad2_gender', 'ad2_birthday', 'ad2_pin', 'ad2_country',
                            'ad2_city', 'ad2_city_custom', 'ad2_address', 'ad2_index', 'ad2_street', 'ad2_house',
                            'ad2_apartment', 'ad2_phone', 'ad2_email']
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

                /* Определить, какой слой является последним на данном этапе */
                $ui.find('.j-next__layer').show();
                if (!calc.contract.p12_selected) {
                    $ui.find('.n-form__layer#layer-2 .j-next__layer').attr('data-last', 'true');
                    $ui.find('.n-form__layer#layer-3 .j-next__layer').unbind('click').hide();
                } else {
                    if (calc.contract.additional_drivers) {
                        $ui.find('.n-form__layer#layer-4 .j-next__layer').attr('data-last', 'true');
                        $ui.find('.n-form__layer#layer-5 .j-next__layer').unbind('click').hide();
                    } else {
                        $ui.find('.n-form__layer#layer-3 .j-next__layer').attr('data-last', 'true');
                        $ui.find('.n-form__layer#layer-4 .j-next__layer').unbind('click').hide();
                    }
                }

                /*** Страхователь - владелец авто ***/
                $ui.find('input[name="ins_owner"]').unbind('change').change(function () {
                    $ui.find('#ins_owner_fields')[$(this).prop('checked') ? 'fadeOut' : 'fadeIn'](200)
                });

                /* Второй дополнительный водитель */
                $ui.find('input[name="additional_driver_2"]').unbind('change').change(function () {
                    $ui.find('#additional_driver_2_fields')[$(this).prop('checked') ? 'fadeIn' : 'fadeOut'](200)
                });

                $(document).trigger('step_5_loaded');
            },

            rollback: function(){
                var $ui = $('#step-5');
                calculator.calc_form('layer_prev', $ui.find('#layer-1 .j-prev__layer'));
            },

            next: function(){
                return 'step_6'
            }
        },

        /* Delivery and payment */
        step_6: {
            /*** Workflow properties ***/
            init: function(){
                var calc = vehicle_calculator;
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
                var ct = vehicle_calculator.contract;
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
                    console.log('click');
                    var $el = $(this);
                    // Валидируем указанные поля
                    var flds = ['delivery_type', 'delivery_date', 'delivery_time', 'delivery_city', 'delivery_region',
                        'delivery_street', 'delivery_house', 'delivery_phone', 'delivery_takeout', 'delivery_email',
                        'payment_type'];
                    calculator.show_spinner();
                    $el.attr('disabled', 'disabled');
                    calc.validate_contract(flds, function (has_errors) {
                        if(!has_errors) {
                            vehicle_calculator.contract.s_premium = calculator.calculate_total_sum($('#step-4'));

                            // Выпускаем черновик полиса
                            $.post('/calculator/modal/vehicle/?m=json&cl=issue', vehicle_calculator.contract, function(data){
                                if(!data.has_errors) {
                                    vehicle_calculator.contract.transaction_id = data.transaction_id
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

                $('#step_7_pay_cash, #step_7_pay_online').hide();

                // В зависимости от типа оплаты, или финальное поздравление или предложение оплатить
                if($('#id_payment_type_cash').prop('checked') === true) {
                    $('#step_7_pay_cash').show();
                }
                else {
                    var total_sum = calculator.calculate_total_sum($('#step-4'));
                    online_payment.load_form(total_sum, vehicle_calculator.contract.transaction_id);

                    $('#step_7_pay_online').show();
                }

                $(document).trigger('step_7_loaded');
            }
        }
    }
};
