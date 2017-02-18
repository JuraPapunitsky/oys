/**
* Вытаскиваем из ячейки td текст и преобразуем его в нужные типы для сравнения
*/
var tablesorter_convert = {

    get_compate_text: function(td_node) {
        var val = $(td_node).text()
        val = val.replace(/\s/g, "")

        if(/^\d+(\.\d+)$/i.test(val))
            val = tablesorter_convert.format_numeric(val)

        else if(/^\d{2}\.\d{2}\.\d{4}( \d{2}\:\d{2})?$/i.test(val))
            val = tablesorter_convert.format_date(val)

        return val
    },

    format_date: function(val) {
        try {
            return val.replace(/(\d{2})\.(\d{2})\.(\d{4})/, '$3-$2-$1')
        }
        catch(err) {
            return val
        }
    },

    format_numeric: function(val) {
        try {
            var fl = parseFloat(val)
            var fl_str = '0000000000000000' + fl.toFixed(4)
            fl_str = fl_str.slice(-20)
            return fl_str
        }
        catch(err) {
            return val
        }
    }
}

$(document).ready(function(){
    $("table.sortable").tablesorter({
        textExtraction: tablesorter_convert.get_compate_text
    });
    // $("table.sortable").tablesorter();
});
