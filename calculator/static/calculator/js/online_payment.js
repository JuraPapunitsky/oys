var online_payment = {
    refresh_interval: null,
    order: null,

    /**
    * Загрузить форму оплаты
    * Слушать нажатия на кнопку "Оплатить"
    * При ее нажатии, ждать поступления денег
    */
    load_form: function(amount, order_id) {
        var url = utils.url_options('/calculator/online_payment_form/', {'amount': amount, 'order': order_id});

        $('#online_payment_form').load(url, function() {
            $('#online_payment_form').show();

            $('#online_payment_submit').click(function() {
                online_payment.wait_payment(order_id);
                $('#online_payment_form').slideUp();
                $('#online_payment_progress').slideDown();
            });
        });
    },

    /**
    * При открытии на отдельной вкладке сайта оплаты,
    * Показываем спиннер ожидания завершения оплаты на сайте мерчанта
    * Время от времени проверяем, не пришли ли деньги.
    * Если деньги пришли, поздравляем
    */
    wait_payment: function(order) {
        $('#online_payment_form').slideUp();
        $('#online_payment_progress').slideDown();

        // Таймер
        online_payment.order = order;
        online_payment.refresh_interval = window.setInterval(online_payment.check_payment, 1024 * 4);
    },

    /**
    * Проверяет поступление денег.
    * Если поступили, показывает поздравление
    */
    check_payment: function() {
        response = utils.get_ajax('/calculator/check_payment/vehicle/'+ online_payment.order +'/');
        if(response.result === true) {
            $('#online_payment_progress').slideUp();
            $('#online_payment_success').slideDown();
            window.clearInterval(online_payment.refresh_interval);
        }
    }

};
