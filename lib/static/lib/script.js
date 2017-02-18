

function reload_page() {
    window.location.href=window.location.href;
}

function bind_time_input(time_input_id) {
    if(typeof time_input_id == 'undefined')
        time_input_id = 'input.time'
    $(time_input_id).mask("99:99");
}

function bind_date_input(date_input_id) {
    if(typeof date_input_id == 'undefined')
        date_input_id = 'input.date:not([readonly])'

    $(date_input_id).datepicker({
        'format': 'dd.mm.yyyy',
        'weekStart': 1,
        'autoclose': true,
        'language': 'ru',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'enableOnReadonly': false
    });
}

/**
* Слушаем клики на кнопках с классом disable_onclick
* и блокируем их для повторного нажатия,
* чтобы не отправлять запрос несколько раз и не выдать несколько договоров, например
*/
function bind_disable_btn_onclick() {
    $('.disable_onclick').click(function() {
        $(this).addClass('disabled')
    })
}

function bind_datepiker(date_input_id) {
    bind_date_input()
    bind_time_input()
}

function bind_popover() {
    $('.popovered-click').popover({html: true});
    $('.popovered-hover').popover({html: true, trigger: 'hover'});
    $('.popovered-manual').popover({html: true, trigger: 'manual'});

    $('.popovered-click, .popovered-hover, .popovered-manual').on('shown.bs.popover', function() {
        bind_datepiker()
    })
}

function bind_tooltip() {
    $('[data-toggle="tooltip"]').tooltip()
}

/**
 * Очистить форму.
 * Именно очистить, а не сбросить все значения на умолчальные.
 * @param form_selector jQuery selector формы
 */
function form_clear(form_selector) {
    $(form_selector + ' select').prop('selectedIndex', -1);
    $(form_selector + ' input:not(.btn):not([name=csrfmiddlewaretoken]):not([name=form_name])').val('');
}


var openWindowIndex = 0;
function open_window(path, width, height) {
    openWindowIndex++;
    window.open(path, 'NewWindow' + openWindowIndex, 'status=no,scrollbars=yes,resizable=yes,location=no,fullscreen=no,toolbar=no,directories=no,width=' + width + ',height=' + height);
}


/**
 * Пересечение двух списков. Возвращает true, если пересечение есть, иначе false
 * @param v_list1 list
 * @param v_list2 list
 * @returns {boolean}
 */
function list_intersection(v_list1, v_list2) {
    for (var i = 0; i < v_list1.length; i++) {
        if (v_list2.indexOf(v_list1[i]) != -1)
            return true;
    }
    return false;
}

function in_list(v_item, v_list) {
    if ($.inArray(v_item, v_list) !== -1)
        return true;
    return false;
}

function ajax_result(p_path, options) {
    var url = utils.url_options(p_path, options)
    var result = null;

    $.ajax({
        async: false,
        url: url,
        success: function (data, textStatus) {
            result = data
        }
    });

    return result;
}

function ajax_result_async(p_path, callback, options) {
    return $.ajax({
        async: true,
        url: utils.url_options(p_path, options),
        success: function (data, textStatus) {
            if(data.error == null)
                callback(data.result)
            else {
                alert(data.error)
            }
        }
    });
}

/**
* Установить значение списка, используя значение опции, а не ее id
*/
function select_set_by_text(p_select, p_text) {
    p_select.children().filter(function() {return $(this).text() == p_text;}).prop('selected', true);
}

/**
*
*/
function wordwrap(str, width, brk) {

    brk = brk || '\n';
    width = width || 75;

    if (!str) { return str; }

    var regex = '.{1,' +width+ '}(\\s|$)|\\S+?(\\s|$)';

    return str.match( RegExp(regex, 'g') ).join( brk );

}

function formset_row_delete_toggle(delete_icon, checkboxId) {
    var chb = $('#' + checkboxId)
    var row = $(delete_icon).parents('tr')

    if(chb.prop('checked')) {
        chb.prop('checked', false)
        row.css('background-color', 'white')
    }
    else {
        chb.prop('checked', true)
        row.css('background-color', '#f2dede')
    }
}


function addBusinessDays(d,n) {
    var day = d.getDay();

    d.setDate(
        d.getDate() + n +
        (day === 6 ? 2 : +!day) +
        (Math.floor((n - 1 + (day % 6 || 1)) / 5) * 2));
}

function setInputDateTime(p_name, p_date) {
    if(p_date == null) {
        $('#id_' + p_name + '_0').val('')
        $('#id_' + p_name + '_1').val('')
    }
    else {
        $('#id_' + p_name + '_0').val(p_date.format('dd.mm.yyyy'))
        $('#id_' + p_name + '_1').val(p_date.format('H:MM'))
    }

}

function strToDate(strDate) {
    if(typeof strDate == 'undefined')
        return strDate

    var dateParts = strDate.split(".");
    return new Date(dateParts[2], (dateParts[1] - 1), dateParts[0]);
}

/**
 * Заморозить состояние поля типа select
 * Блокирует выбор всех опций кроме выбранной
 * @param field_id
 */
function select_freeze(select_obj) {
    var val = select_obj.val()
    select_obj.children().each(function() {
        var current = $(this)
        if(current.attr('value') != val)
            $(this).attr('disabled','disabled')
    })
    select_obj.attr('readonly','readonly')
}

/**
 * Заморозить состояние поля типа select
 * @param field_id
 */
function select_unfreeze(select_obj) {
    select_obj.children().each(function() {
        $(this).removeAttr('disabled')
    })
    select_obj.removeAttr('readonly')
}
