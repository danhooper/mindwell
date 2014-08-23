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
MW.getDefaultTablesorterOptions = function() {
    var defaultOptions = {
        sortList: [[0,0]],
        textExtraction: "complex",

        widgets : [ "uitheme", "filter", "zebra" ],
        theme: 'bootstrap',
        headerTemplate : '{content} {icon}'
    };
    return defaultOptions;
};
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
    $("table#mw-session-table").tablesorter(MW.getDefaultTablesorterOptions());
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
    $("table").tablesorter(MW.getDefaultTablesorterOptions());
};
MW.showClientsInit = function() {
    // call the tablesorter plugin
    $("table").tablesorter(MW.getDefaultTablesorterOptions());
    $('#content a[tooltip]').each(function()
    {
        $(this).qtip({content: $(this).attr('tooltip'), style: 'cream'});
    });
    $("#dialog-modal").dialog({autoOpen: false,
        width:450,
        modal: true,
        hide: { effect: 'fade',
            duration: 1000
        },
    });
    $('a.uimodal').bind('click', function() {
        var $this = $(this);
        $("#dialog-modal").dialog('open');
        $("#dialog-modal").load($this.attr("href"), null, function() {
        });
        return false;
    });
    function getBalanceSuccessFunc(client_obj) {
        var client_td = client_obj;
        // create a closure so we can access the client_td in the callback
        return function(data) {
            $(client_td).text(data['balance']);
        };
    };
    $('#calc_balances').click(function(event) {
        event.preventDefault();
        $('.client_balance').each(function(index) {
            client_td = $(this);
            $.getJSON($(this).data('balance-url'), getBalanceSuccessFunc(client_td));
        });
    });
};

MW.invoicesInit = function() {
    $("#invoice_table").tablesorter(MW.getDefaultTablesorterOptions());
};

MW.permissionSettingsInit = function() {
    var tblOptions = MW.getDefaultTablesorterOptions();
    tblOptions.sortList = [[1,0]];
    $(".tablesorter").tablesorter(tblOptions);
};

MW.showSpecificClientInit = function () {
    var tblOptions = MW.getDefaultTablesorterOptions();
    tblOptions.sortList = [[10,1]];
    tblOptions.headers = { 0: { sorter: false} };

    // call the tablesorter plugin
    $("table").tablesorter(tblOptions);
};

MW.dosFormJavascriptInit = function(blocked_time) {
    function hide_dos_duration() {
        $("label[for='id_dos_duration']").hide();
        $("#id_dos_duration").hide();
    }
    function show_or_hide_dos_repeat_end() {
        if( $("#id_dos_repeat").val() == "No") {
            $("label[for='id_dos_repeat_end_date']").hide();
            $("#id_dos_repeat_end_date").hide();
        }
        else {
            $("label[for='id_dos_repeat_end_date']").show();
            $("#id_dos_repeat_end_date").show();
        }
    }
    function set_endtime_to_starttime() {
        var startSelectedValue = $("#id_dos_datetime_1_time").val();
        $("#id_dos_endtime_time").val(startSelectedValue);
    }
    function on_change_session_result() {
        if( $("#id_session_result").val() == "Cancellation - Timely") {
            $("#id_dos_duration").val("0");
            set_endtime_to_starttime();
            $("#id_amt_due").val("0");
            $("#id_type_pay").val("");
            $("#id_session_type").val("");
        }
        if( $("#id_session_result").val() == "Cancellation - Late") {
            $("#id_dos_duration").val("0");
            set_endtime_to_starttime();
            $("#id_session_type").val("");
        }
        if( $("#id_session_result").val() == "No Show") {
            $("#id_dos_duration").val("0");
            set_endtime_to_starttime();
            $("#id_session_type").val("");
        }
    }
    function on_click_blocked_time() {
        var fields = ["id_clientinfo", "id_session_type", "id_session_result",
            "id_dsm_code", "id_type_pay", "id_amt_due", "id_amt_paid", "id_print_receipt"
        ];
        if( $("#id_blocked_time").is(":checked" )) {
            for( x in fields) {
                $("#" + fields[x]).hide();
                $("label[for='" + fields[x] + "']").hide();
            }
        }
        else {
            for( x in fields) {
                $("#" + fields[x]).show();
                $("label[for='" + fields[x] + "']").show();
            }
        }
    }
    function on_click_dos_datetime_1_time() {
        try {
            var start_hour = $("#id_dos_datetime_1_time").val().slice(0, 2);
        } catch(exception) {
            return;
        }
        var selectedValue = $("#id_dos_endtime_time").val();
        var start_minute = $("#id_dos_datetime_1_time").val().slice(3, 5);
        var start_meridiem = $("#id_dos_datetime_1_time").val().slice(6, 8);
        $("#id_dos_endtime_time").html("");
        var meridiem = 'am';
        var hourVals = ["12", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"];
        var minuteVals = ["00", "15", "30", "45"];
        var meridiemVals = ["am", "pm"];
        for( x in meridiemVals) {
            if( meridiemVals[x] == start_meridiem)
            {
                start_meridiem = x
                break;
            }
        }
        for( x in hourVals) {
            if( hourVals[x] == start_hour) {
                start_hour = x;
                break;
            }
        }
        for( x in minuteVals) {
            if( minuteVals[x] == start_minute) {
                start_minute = x;
                break;
            }
        }
        minute_counter = 0;
        for( start_meridiem; start_meridiem < meridiemVals.length; start_meridiem++)
        {
            for( start_hour; start_hour < hourVals.length; start_hour++) {
                for( start_minute; start_minute < minuteVals.length; start_minute++) {
                    output = "" + hourVals[start_hour] + ":" + minuteVals[start_minute] + " " + meridiemVals[start_meridiem];
                    $("#id_dos_endtime_time").append(
                        $("<option></option>").val(output).html(output + " (" + minute_counter + " mins)")
                    );
                    minute_counter += 15
                }
                start_minute = 0;
            }
            start_hour = 0;
        }
        // reselect option
        $("#id_dos_endtime_time").val(selectedValue);
    }

    show_or_hide_dos_repeat_end();
    hide_dos_duration();
    $("#id_dos_repeat").change( show_or_hide_dos_repeat_end);
    $("#id_session_result").change( on_change_session_result);
    $("#id_blocked_time").click( on_click_blocked_time);
    if(blocked_time) {
        $("#id_blocked_time").attr("checked", true);
        on_click_blocked_time()
    }
    $("#id_dos_datetime_1_time").change(on_click_dos_datetime_1_time);
    on_click_dos_datetime_1_time();
    $.datepicker.setDefaults({
        dateFormat: "yy-mm-dd"
    });
    $( "#id_dos_datetime_0" ).datepicker();
    $( "#id_dos_repeat_end_date" ).datepicker();
    create_choice_modal_dialog("session_type", "input#id_session_type");
};
