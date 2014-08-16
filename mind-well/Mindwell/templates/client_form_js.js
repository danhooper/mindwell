create_choice_modal_dialog("referrer", "input#id_referrer");
create_choice_modal_dialog("reason_for_visit", "input#id_reason_for_visit");
$( "#id_referrer" ).autocomplete({
    source: "/Mindwell/referrer_autocomplete/",
});
$( "#id_dsm_code" ).autocomplete({
    source: "/Mindwell/dsm_code_autocomplete/",
});
$('input').addClass('form-control');
$('select').addClass('form-control');
