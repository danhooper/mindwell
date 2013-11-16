/* Mindwell's own JS */
function create_choice_modal_dialog(dialog_prefix, input_id) {
    var dialog_id = dialog_prefix + "_dlg";
    $( "#" + dialog_id ).dialog({
        autoOpen: false,
        width:650,
        modal: true,
        dialogClass: dialog_id,
        buttons: {
            "OK": {         
                text: 'OK',
                id: "OK_" + dialog_id,
                click: function() {
                    var checkboxes = [];
                    $('.multicheckbox', '#' + dialog_id).each(function () {
                        if (this.checked) {
                            checkboxes.push($(this).val());
                        }
                    });
                    choices_picked = checkboxes.join(", ");
                    if($("#" + dialog_prefix + "_choice_other").val()) {
                        if (choices_picked) {
                            choices_picked += ", ";
                        }
                        choices_picked += $("#" + dialog_prefix + "_choice_other").val();
                    }
                    $(input_id).val(choices_picked);
                    $( "#" + dialog_id ).dialog( "close" );
                }
            },
            Cancel: function() {
                $( "#" + dialog_id  ).dialog( "close" );
            }
        }
    });
    $( input_id )
        .click(function() {
            $( "#" + dialog_id ).dialog( "open" );
    });
}
