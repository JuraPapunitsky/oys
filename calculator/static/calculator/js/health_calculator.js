var health_calculator = {

    contract: {},

    products: {
        '9_1': {price: 0.0, error: ''},  // Urgent care
        '9_2': {price: 0.0, error: ''},  // Refund Pediatric
        '9_3': {price: 0.0, error: ''}, // Program 69
        '9_4': {price: 0.0, error: ''},  // Program 69+
        '9_5': {price: 0.0, error: ''}  // Refund Pediatric VIP
    },

    /* Init contract object */
    init_contract: function() {
        this.contract = {
            csrfmiddlewaretoken:'',
            step: '',
            substep: '',
            layer: '',
            /**/
            main_product: null,
            main_product_text: '',
            p9_1_selected: false,
            p9_2_selected: false,
            p9_3_selected: false,

            p9_1_payment: 0.0,
            p9_2_payment: 0.0,
            p9_3_payment: 0.0,

            p9_inscompany: null,

            d_start: null,

            /* Health */
            health_poll: [],
            deductible: 25,
            vac: false,
            massage: false,
            refund_vip: false,
            program69_extended: false,

            insured_lname: '',
            insured_fname: '',
            insured_mname: '',
            insured_birthday: '',

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
        return ''
    },

    get_description: function(){
        var ct = this.contract;
        return $.t('birthdayTitle') + ' ' + ct.insured_birthday;
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
        var calc = health_calculator;
        var $form = $('.j-clr-calcform');

        // Product select from step-3
        calc.contract['health_poll'] = [];
        calc.contract['p9_1_selected'] = false;
        calc.contract['p9_2_selected'] = false;
        calc.contract['p9_3_selected'] = false;
        calc.contract['refund_vip'] = false;
        calc.contract['vac'] = false;
        calc.contract['massage'] = false;
        calc.contract['program69_extended'] = false;
        if(calc.contract['main_product'] && calc.contract['main_product'] !== undefined)
            calc.contract['p'+calc.contract['main_product']+'_selected'] = true;

        var boolFields = ['p9_1_selected', 'p9_2_selected', 'p9_3_selected', 'refund_vip', 'program69_extended',
            'vac', 'massage'];
        $form.serializeArray().forEach(function(obj){
            if (obj.name == 'health_poll') {
                calc.contract['health_poll'].push(obj.value)
            } else if (boolFields.indexOf(obj.name) >= 0) {
                calc.contract[obj.name] = true
            } else {
                calc.contract[obj.name] = obj.value
            }
        });
    },

    /* Refresh product */
    refresh_products: function(success_callback) {
        health_calculator.refresh_state();
        health_calculator.refresh_data();
        $.post('/calculator/modal/health/?m=json&cl=products', this.contract, function(data) {
            health_calculator.products = data;
            if (success_callback) success_callback();
        })
    },

    /* Validates {contract} fields via ajax json request */
    validate_contract: function(fields, complete){
        health_calculator.refresh_state();
        health_calculator.refresh_data();

        /* Clean up previous errors (removes data-iserror classes and cleans .field-error block spans */
        fields.forEach(function(fld){
            $('.j-clr-calcform').find('input[name="'+fld+'"]').parents('.b-data__line').removeClass('data-iserror').find('.field-error span').html('');
        });

        /* Call 'validate' method via AJAX */
        $.post('/calculator/modal/health/?m=json&cl=validate', health_calculator.contract, function(result){
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
    health_edit_click: function(){
        var insured_birthday = moment(health_calculator.contract.insured_birthday, 'DD.MM.YYYY');
        var rollback_step = 'substep_1';
        if (moment.range(insured_birthday, new Date).diff('years') <= 14) rollback_step = 'substep_2';

        if(workflow.rollback_stage(rollback_step)) {
            $('.n-form__step').removeClass('e-active');
            $('#step-2').addClass('e-active');
        }
    },

    /* Calculates total sum and displays selected products */
    calculate_right_info: function () {
        health_calculator.refresh_data();
        var detailsAndPrices = [];
        var ct = health_calculator.contract;

        if (ct.p9_1_selected) {
            detailsAndPrices.push({
                sel: '.p9_1__detail',
                text: 'A-Group',
                price: health_calculator.products['9_1'].price
            });
            ct.p9_1_payment = health_calculator.products['9_1'].price;
        }


        if (ct.p9_2_selected) {
            if (ct.refund_vip) {
                detailsAndPrices.push({
                    sel: '.p9_5__detail',
                    text: 'A-Group',
                    price: health_calculator.products['9_5'].price
                });
                ct.p9_2_payment = health_calculator.products['9_5'].price;
            } else {
                detailsAndPrices.push({
                    sel: '.p9_2__detail',
                    text: 'A-Group',
                    price: health_calculator.products['9_2'].price
                });
                ct.p9_2_payment = health_calculator.products['9_2'].price;
            }
        }

        if (ct.p9_3_selected) {
            if (ct.program69_extended) {
                detailsAndPrices.push({
                    sel: '.p9_4__detail',
                    text: 'A-Group',
                    price: health_calculator.products['9_4'].price
                });
                ct.p9_3_payment = health_calculator.products['9_4'].price;
            } else {
                detailsAndPrices.push({
                    sel: '.p9_3__detail',
                    text: 'A-Group',
                    price: health_calculator.products['9_3'].price
                });
                ct.p9_3_payment = health_calculator.products['9_3'].price;
            }
        }

        // Free delivery
        detailsAndPrices.push({sel: '.delivery__detail', text: '', price: '0.0'});

        var $ui = $('#step-4');
        $ui.find('.b-right__detail').addClass('n-brd__btm-no').removeClass('n-brd__mrg').hide();

        var total_sum = 0;
        _.each(detailsAndPrices, function (detail) {
            var $detail = $ui.find(detail.sel).fadeIn(200, function () {
                $ui.find('.b-right__detail:visible').first().addClass('n-brd__mrg');
                $ui.find('.b-right__detail:visible').last().removeClass('n-brd__btm-no');
            });
            $detail.find('.b-detail__text span').html(detail.text);
            $detail.find('.b-detail__price span').html(detail.price);

            if (detail.sel != '.delivery__detail') {
                $ui.find('#product-table-company').html(detail.text);
                $ui.find('#product-table-product').html($detail.find('.b-detail__product').text());
                $ui.find('#product-table-price').html($detail.find('.b-detail__price').html());
            }

            total_sum += parseFloat(detail.price);
        });

        $ui.find('.b-total__summ').html(total_sum.toFixed(2) + '<span>AZN</span>');
    },

    /* Copy selected products and total price */
    copy_right_info: function($source_step, $target_step){
        ['.p9_1__detail', '.p9_2__detail', '.p9_3__detail', '.p9_4__detail', '.p9_5__detail', '.delivery__detail'].forEach(function(cls){
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

        $('#id_ins_person_pin').mask('*******');
        $('#id_ins_person_fname, #id_ins_person_lname').mask('?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@');
        $('#id_ins_person_mname').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_street, #id_delivery_street').mask('?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        $('#id_ins_phone, #id_delivery_phone').mask('?############');
        $('#id_index').mask('AZ####');
        $('#id_ins_index').mask(health_calculator.contract.ins_country == '4' ? 'AZ####' : '######');
        $('#id_d_start, #id_insured_birthday, #id_ins_person_birthday, #id_delivery_date').mask('##.##.####');
    },

    /* Vehicle contracts calculation steps */
    workflow_steps: {

        /* Insured birthday date selection */
        substep_1: {
            load: function(){
                var $ui = $('#substep-1');
                health_calculator.init_field_masks();
                $ui.find('.j-next__click').unbind('click').on('click',function () {
                    health_calculator.validate_contract(['insured_birthday'], function (has_errors) {
                        if (!has_errors) workflow.next_stage();
                    });
                });
            },
            init: function() {
                $(document).trigger('substep_2_loaded');
            },
            rollback: function(){
                var ct = health_calculator.contract;
                ct.insured_birthday = null;
            },
            next: function() {
                var $el = $('#substep-1').find('.j-next__click');
                var insured_birthday = moment(health_calculator.contract.insured_birthday, 'DD.MM.YYYY');
                if (moment.range(insured_birthday, new Date).diff('years') >= 14) {
                    calculator.calc_form('forward', $el);
                    return 'step_3';
                } else {
                    calculator.calc_form('subst', $el);
                    return 'substep_2';
                }
            }
        },

        substep_2: {
            init: function() {
                var $ui = $('#substep-2');
                $ui.find('.b-radio__wr input').unbind('change').change(function () {
                    var health_poll = [];
                    $ui.find('input:checked').each(function (index) {
                        health_poll.push($(this).val());
                    });

                    if (_.indexOf(health_poll, $(this).val()) >= 0) {
                        $(this).next().addClass('active')
                    } else {
                        $(this).next().removeClass('active')
                    }

                    health_calculator.contract.health_poll = health_poll;
                });

                $ui.find('.j-next__click').unbind('click').on('click', function () {
                    workflow.next_stage();
                    calculator.calc_form('forward', $(this));
                });
            },
            next: function() {
                return 'step_3'
            }
        },

        step_3: {
            load: function(){

                calculator.show_spinner();
                var ct = health_calculator.contract;
                var $ui = $('#step-3');

                ct.csrfmiddlewaretoken = $ui.parents('.j-clr-calcform').find('input[name="csrfmiddlewaretoken"]').val();

                $.post('/calculator/modal/health/?m=ajax&cl=precalculate', ct, function(data){

                    $ui.find('.b-form__left').html(data).find('.insurance_product__btn').unbind('click').click(function () {
                        ct.main_product = $(this).data('product-id');
                        ct.main_product_text = $(this).data('product-title');
                        ct['p'+ct.main_product+'_selected'] = true;

                        workflow.next_stage();
                        calculator.calc_form('forward', $(this));

                        return false;
                    });
                    health_calculator.refresh_products(function() {
                        calculator.hide_spinner();
                    });

                    $ui.find('.j-calculator__reset').click(calculator.reset_calculator);
                    $(document).trigger('step_3_loaded');

                }).fail(
                    calculator.ajax_fail_dialog_factory(health_calculator.workflow_steps.step_3.load)
                );


            },

            init: function(){
                var $ui = $('#step-3');
                var calc = health_calculator;
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
            validated_fields: ['p9_1_selected', 'p9_2_selected', 'p9_3_selected'],

            /*** Workflow properties ***/

            load: function() {
                var $ui = $('#step-4');
                var calc = health_calculator;

                calculator.show_spinner();
                $.get('/calculator/modal/health/?m=ajax&cl=options&pr=' + calc.contract.main_product, {}, function (data) {
                    $ui.find('.b-step-4__options').html(data);

                    $ui.find('input[name="p9_1_selected"],input[name="p9_2_selected"],input[name="p9_3_selected"]').unbind('click').click(function () {
                        $('.'+$(this).attr('name')+'__scr')[$(this).prop('checked') ? 'fadeIn' : 'fadeOut'](200);
                        calc.calculate_right_info();
                    });

                    $ui.find('[name="refund_vip"]').unbind('change').change(function(){
                        $ui.find('#refund__descr, #refund_vip__descr').toggle();
                        $ui.find('[name="massage"]').closest('.b-data__line').toggle();
                        calc.calculate_right_info();
                    });

                    $ui.find('[name="program69_extended"]').unbind('change').change(function(){
                        $ui.find('#p69__descr, #p69_ext__descr').toggle();
                        calc.calculate_right_info();
                    });

                    $ui.find('[name="vac"],[name="massage"],[name="deductible"]').unbind('change').change(function() {
                        calculator.show_spinner();
                        calc.refresh_products(function() {
                            calc.calculate_right_info();
                            calculator.hide_spinner();
                        })
                    });

                    calculator.hide_spinner();
                });
            },

            init: function(){
                var step_obj = this;
                var $ui = $('#step-4');
                var calc = health_calculator;

                calc.calculate_right_info();

                /*** Контролы этапа (параметры продуктов) вызывают расчет матрицы продуктов ***/
                $ui.find('.b-step-4__options input').unbind('change').change();

                /*** Открыть подсказку ***/
                $ui.find('.j-qw__link').unbind('click').click(calculator.help_layer_opener);

                // Right infos
                $ui.find('.b-step__title h2').html(calc.contract.main_product_text);
                $ui.find('.b-info__title').html(calc.get_title());
                $ui.find('.b-info__text').html(calc.get_description());

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
                var calc = health_calculator;

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
                        'layer-1': ['d_start'],
                        'layer-2': ['ins_person_pin', 'ins_person_fname', 'ins_person_lname', 'ins_person_mname', 'ins_person_gender',
                            'ins_person_birthday', 'ins_index', 'ins_country', 'ins_city', 'ins_city_custom', 'ins_address',
                            'ins_street', 'ins_house', 'ins_apartment', 'ins_phone', 'ins_email'],
                        'layer-3': ['insured_fname', 'insured_lname', 'insured_mname']
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
                var calc = health_calculator;
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
                var ct = health_calculator.contract;
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
                            $.post('/calculator/modal/health/?m=json&cl=issue', health_calculator.contract, function(data){
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