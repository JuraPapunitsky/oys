var utils = {
    
    /**
    *  Добавляет опции в виде GET-переменных к url-у
    */
    url_options: function(url, options) {
        if(typeof options == 'undefined')
            return url;
    
        var new_url = url + '?';
        var is_first = true;

        $.each(options, function (key, value) {
            if (is_first === false)
                new_url = new_url + '&';

            new_url = new_url + key + '=' + value;
            is_first = false;
        });

        return new_url
        
    },

    /**
    * Запросить данные по AJAX
    */
    get_ajax: function(p_path, options) {
        var url = utils.url_options(p_path, options);
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
    
};