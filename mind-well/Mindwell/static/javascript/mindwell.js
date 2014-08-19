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
var MW = {};
MW.sessionCountInit = function(session_count) {
  $.plot($("#mw-session-count"), [
    { data: session_count, label: "Session Count" },
    ],
    {
      yaxis: {
        tickFormatter: function(v, axis) {
          return v.toFixed(axis.tickDecimals) + " clients";
        },
        tickDecimals: 0
      },
     xaxis: {
       tickDecimals: 0
     },
    }
  );
  // call the tablesorter plugin
  $("table#mw-session-table").tablesorter({
      sortList: [[0,0]],
      textExtraction: "complex",
    widgets : [ "uitheme", "filter", "zebra" ],

    widgetOptions : {

      // set the uitheme widget to use the bootstrap theme class names
      uitheme : "bootstrap"

    }
  });
};
MW.dosValueInit = function(dos_count, dos_value) {
  $.plot($("#placeholder"), [
    { data: dos_count, label: "DOS Count" },
    { data: dos_value, label: "DOS Value", yaxis: 2 }
    ],
    {
      yaxis: {
        tickFormatter: function(v, axis) {
          return v.toFixed(axis.tickDecimals) + " DOS";
        }
      },
      y2axis: {
        tickFormatter: function(v, axis) {
          return "$" + v.toFixed(axis.tickDecimals);
        }
      }
    }
  );
  // call the tablesorter plugin
  $("table").tablesorter({
      sortList: [[0,0]],
      textExtraction: "complex",
    widgets : [ "uitheme", "filter", "zebra" ],

    widgetOptions : {

      // set the uitheme widget to use the bootstrap theme class names
      uitheme : "bootstrap"

    }
  });
};
