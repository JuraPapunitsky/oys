var tree_widget = {
    
    /**
    * Текущий id поля (используется, чтобы не перезагружать дерево 
    * в модальном окне, если редактируется то же поле)
    */
    current_field_id: '',

    /**
    * Открыть окно редактирования
    */
    edit: function(field_id, ajax_url) {
        var modal_window = $('#tree_widget_modal')

        // Если не то же самое поле редактируется, то инициализируем плагин
        if(field_id != this.current_field_id) {
            this.current_field_id = field_id
            var modal_body = $('#tree_widget_modal .modal-body')
            
            var tree = modal_body.jstree({
                core: {
                    data: {
                        url: ajax_url,
                        data : function (n) {
                            var node_id = n.id == '#' ? '' : n.id 
                            return {'node_id': node_id}
                        }
                    }
                }
            })

            tree.bind("select_node.jstree", function (event, data) {

                    console.log(data.node.id)

                    var selected_node = data.node
                    var hidden_field = $("#" + field_id)

                    hidden_field.val(selected_node.id);
                    hidden_field.change()

                    $("#" + field_id + "_title").html(selected_node.text);

                    modal_window.modal('hide');
                }
            )

        }
        
        modal_window.modal('show');
    },

    /**
    * Очистить выбраное значение
    */
    clear: function(input_id) {
        $('#' + input_id).val('');
        $('#' + input_id + '_title').html('Не выбрано');
    }

}