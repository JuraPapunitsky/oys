var utils = {

    val: function(input_id, value) {
        var input = $('#'+input_id)
        if(typeof input == 'undefined' || input.length == 0) {
            return null
        }

        if(typeof value != 'undefined') {
            if(input.attr('type') == 'checkbox')
                input.prop('checked')
            else
                input.val(value)
            return
        }

        if(input.attr('type') == 'checkbox')
            return input.prop('checked')

        return $(input).val()
    },

    show: function(selector) {
        $(selector).show()
    },

    hide: function(selector) {
        $(selector).hide()
    },

    date_add_days: function(d, days) {
        d.setDate(d.getDate() + days)
        return d
    },

    date_add_months: function(d, months) {
        d.setMonth(d.getMonth() + months)
        return d
    },

    date_subtract_days: function(d, days) {
        d.setDate(d.getDate() - days)
        return d
    },

    disable: function (selector) {
        var input = $(selector)
        input.attr('readonly', 'readonly')
    },

    enable: function (selector) {
        var input = $(selector)
        input.removeAttr('readonly')
    },

    fill_if_none: function(input_id, value) {
        var input = $('#'+input_id)
        if(typeof input == 'undefined')
            return null

        if(input.val() != '')
            return

        if($('#s2id_' + input_id).length > 0)
            input.select2('val', value)
        else
            input.val(value)
    },

    /**
    * Получает другое поле из Formset-а,
    * которое находится на той же строке, что и input
    */
    other_formset_field: function(input, other_field) {

        var formset_prefix = input.parent().parent().parent().parent().attr('id')
        var row_num = input.parent().parent().attr('data-row_index')
        var other_field_selector = formset_prefix + '-' + row_num + '-' + other_field

        return $('#' + other_field_selector)
    },

    /**
    *  Добавляет опции в виде GET-переменных к url-у
    */
    url_options: function(url, options) {
        if(typeof options == 'undefined')
            return url

        var new_url = url + '?'
        var is_first = true;

        $.each(options, function (key, value) {
            if (is_first === false)
                new_url = new_url + '&';

            new_url = new_url + key + '=' + value;
            is_first = false;
        });

        return new_url

    },

    /*
    * Позиционно извлекает из строки день, месяц и год,
    * возвращает дату
    * */
    parse_date: function(input_id, date_pos, month_pos, year_pos, delim) {
        date_pos = date_pos ? date_pos : 0
        month_pos = month_pos ? month_pos : 1
        year_pos = year_pos ? year_pos : 2
        delim = delim ? delim : '.'
        var date_parts = $('#'+input_id).val().split(delim)
        return new Date(date_parts[year_pos], date_parts[month_pos] - 1, date_parts[date_pos])
    },

    /**
    * Текстовое значение выбраной опции
    */
    select_val_text: function(input_id) {
        return $('#'+ input_id +' option:selected').html()
    },

    /**
    * Проверяет наличие элемента в массиве
    */
    in_list: function(item, list) {
        return ($.inArray(item, list) !== -1)
    },

    /**
    * Преобразовать обычный select в select2
    */
    to_select2: function(input_id) {
        var element = $('#'+input_id)
        var bind_select2 = element.removeClass('form-control').select2()

        if(element.is('[readonly]')) {
            bind_select2.select2("readonly", true)
        }
    },

    set_field_tooltip: function(field_name, val) {
        var icon = $('.'+ field_name +'_tooltip')
        icon.attr('data-original-title', val)

        var field_group = $('.'+field_name)


        if(val != '') {
            icon.show()
            field_group.addClass('has-warning')
        }
        else {
            icon.hide()
            field_group.removeClass('has-warning')
        }
    },

    set_field_help: function(field_name, val, cb) {
        var block = $('.'+ field_name +'_info')
        block.html(val)

        if(typeof cb != 'undefined') {
            block.removeClass('pointer').off('click');
            block.addClass('pointer').click(cb);
        }
        else {
            block.removeClass('pointer').off('click');
        }

        if(val != '' && typeof val != 'undefined') {
            block.show()
        }
        else {
            block.hide()
        }
    },

    fill_select: function(obj, options, add_empty) {
        var value = obj.val();

        obj.empty();
        if(add_empty === true) {
            obj.append('<option value="">----</option>');
        }

        $.each(options, function (i, option) {
            obj.append('<option value="' + option.id + '">' + option.title + '</option>');
        });

        obj.val(value);  // Восстановим
    }
}
