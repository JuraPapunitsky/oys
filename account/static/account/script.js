
var login = {
    phone: null,

    /**
    * Сгенерировать код
    */
    generate_code: function(phone) {
        login.phone = $('#login_generate_code_phone').val()
        result = ajax_result('/account/login/get_password/', {'phone': login.phone})
        
        if(result.error == null) {
            this.show_password_form()
        }
        else
            alert('Пользователь не найден')
    },

    /**
    * После отправки одноразового пароля
    * показать форму ввода высланного пароля
    */
    show_password_form: function() {
        $('.login2').modal('hide')
        $('.login3').modal('show')
    },

    /**
    * Войти в систему по логику и паролю
    */
    login_by_password: function() {
        var password = $('#login_pass1').val() 
                       + $('#login_pass2').val() 
                       + $('#login_pass3').val() 
                       + $('#login_pass4').val()
        if(password.length < 12)
            alert('Пароль введен не полностью')

        else {
            var params = {
                'phone': login.phone, 
                'password': password
            }
            res = ajax_result('/account/login/login_by_password/', params)
            if(res.result == 'success') {
                window.location.href = '/'
            }
            else if(res.result == 'not_found')
                alert('Пользователь не найден')
        }
    }
}