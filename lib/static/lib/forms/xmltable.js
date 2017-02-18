function xmltable_mark_deleted(p_a, p_checkbox_id) {
    
    var chb = $('#' + p_checkbox_id)
    var row = $(p_a).parents('tr')

    if(chb.prop('checked')) {
        chb.prop('checked', false)
        row.css('background-color', 'white')
    }
    else {
        chb.prop('checked', true)
        row.css('background-color', '#f2dede')
    }
}