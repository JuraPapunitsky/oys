$(document).ready(function() {
    $('.autocomplete_multiple_widget').each(function() {
        bind_autocomplete_multiple_widget(this);
    });
});

function bind_autocomplete_multiple_widget(element) {
    
    var j_element = $(element)
    var url = '/forms_widget_autocomplete/'
    var handler_path = j_element.attr('data-handler_path')
    var related_fields = j_element.attr('data-related_fields')
    var handler_params = j_element.attr('data-handler_params')
    var readonly = j_element.attr('data-readonly')

    function data_for_ajax(term, page, is_init) {
        params = {q: term, handler_path: handler_path};
        
        if(related_fields != '') {
            $.each(related_fields.split(','), function(k,v) {
                params[v] = utils.val('id_' + v)
            })
        }

        if(handler_params != '') {
            $.each($.parseJSON(handler_params), function(k,v) {
                params[k] = v
            })
        }
        
        if(is_init === true)
            params['is_init'] = true
        
        return params
    }

    var binded_select2 = $(element).select2({
        placeholder: "Поиск элемента",
        minimumInputLength: 3,
        multiple: true,
        ajax: {
            url: url,
            quietMillis: 1000,
            dataType: 'json',
            data: data_for_ajax,
            results: function (data, page) {
                return {results: data.result}
            }
        },
        initSelection: function(element, callback) {
            var id = $(element).val();
            if (id !== "") {
                $.ajax(url, {
                    data: data_for_ajax(id, 1, true),
                    dataType: "json"
                }).done(function(data) {
                    callback(data.result);
                });
            }
        },
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    });

    if(readonly == 'True')
        binded_select2.select2("readonly", false)

}