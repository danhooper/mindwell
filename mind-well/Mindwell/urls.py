from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('Mindwell.Client.view_common',
    (r'^$', 'greetings'),
    url(r'^Mindwell/UserNotAllowed$', 'usernotallowed', name='usernotallowed')
)

urlpatterns += patterns('Mindwell.Client.views',
    (r'^Mindwell/$', 'redirect_to_base'),
    (r'^administrator/$', 'administrator'),
    (r'^administrator/clear_memcache/$', 'clear_memcache'),
    (r'^administrator/update_all_dos/$', 'admin_update_all_dos'),
    (r'^administrator/admin_update_some_dos/$', 'admin_update_some_dos'),
    (r'^administrator/(?P<num_entities>\d+)/admin_update_some_dos/$', 'admin_update_some_dos'),
    (r'^administrator/admin_change_email/(?P<old_email>.*)/(?P<new_email>.*)/$', 'admin_change_email'),

    #Invoices and Reports
    url(r'^Mindwell/reports/$', 'reports', name='reports'),
    (r'^Mindwell/invoices/$', 'invoices'),
    (r'^Mindwell/(?P<invoice_id>\d+)/(?P<all_dos>all_dos)/invoice_display/$', 'invoice_display'),
    (r'^Mindwell/(?P<invoice_id>\d+)/(?P<attended_only>attended_only)/invoice_display/$', 'invoice_display'),
    (r'^Mindwell/(?P<invoice_id>\d+)/(?P<all_dos>all_dos)/html/invoice_display/$', 'invoice_display', {'html':True}),
    (r'^Mindwell/(?P<invoice_id>\d+)/(?P<attended_only>attended_only)/html/invoice_display/$', 'invoice_display', {'html':True}),
    (r'^Mindwell/provider_invoices/$', 'provider_invoices'),
    url(r'^Mindwell/(?P<start_year>\d{4})/(?P<start_month>\d{2})/(?P<start_day>\d{2})/(?P<end_year>\d{4})/(?P<end_month>\d{2})/(?P<end_day>\d{2})/provider_invoices/$',
        'provider_invoices_display', name='provider_invoices_display'),
    (r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/generate_client_invoices/$', 'generate_client_invoices'),
    (r'^Mindwell/(?P<start_year>\d{4})/(?P<start_month>\d{2})/(?P<start_day>\d{2})/(?P<end_year>\d{4})/(?P<end_month>\d{2})/(?P<end_day>\d{2})/generate_client_invoices_by_date/$', 'generate_client_invoices_by_date'),
    (r'^Mindwell/provider_statistics/$', 'provider_statistics'),
    (r'^Mindwell/provider_stats_all_time/$', 'provider_stats_all_time'),
    (r'^Mindwell/(?P<year>\d{4})/provider_statistics/$', 'provider_statistics_display'),
    (r'^Mindwell/export_provider_data/$', 'export_provider_data'),
    (r'^Mindwell/run/export_provider_data/$', 'run_export_provider_data'),


    # Settings
    url(r'^Mindwell/settings/$', 'settings', name='settings'),
    url(r'^Mindwell/settings/invoice/$', 'invoice_settings',
        name='invoice_settings'),
    url(r'^Mindwell/settings/(?P<update>\w+)/invoice/$', 'invoice_settings',
        name='updated_invoice_settings'),
    url(r'^Mindwell/settings/calendar/$', 'calendar_settings',
        name='calendar_settings'),
    url(r'^Mindwell/settings/(?P<update>\w+)/calendar/$', 'calendar_settings',
        name='updated_calendar_settings'),
    url(r'^Mindwell/settings/custom_form_settings/$', 'custom_form_settings',
        name='custom_form_settings'),
    url(r'^Mindwell/settings/(?P<update>\w+)/custom_form_settings/$',
        'custom_form_settings', name='updated_custom_form_settings'),
    (r'^Mindwell/settings/permission/$', 'permission_settings'),
    url(r'^Mindwell/settings/(?P<update>\w+)/permission/$',
        'permission_settings', name='updated_permission_settings'),
    url(r'^Mindwell/settings/(?P<permission_id>\d+)/delete_permission/$', 'delete_permission',
        name='delete_permission'),
    (r'^Mindwell/settings/update_permission/$', 'update_permission_settings'),
    url(r'^Mindwell/settings/(?P<request_permission_id>\d+)/update_permission_requests/$',
        'update_permission_requests', name='update_permission_requests'),
    (r'^Mindwell/settings/(?P<request_permission_id>\d+)/update_request/$', 'update_request_settings'),

    (r'^Mindwell/(?P<change_user>.*)/change_user/$', 'change_user'),

)

urlpatterns += patterns('Mindwell.Client.client_views',
    url(r'^Mindwell/add_client/$', 'add_client_form', name="add_client"),
    url(r'^Mindwell/add_client_standalone/$', 'add_client_standalone', name="add_client_standalone"),
    url(r'^Mindwell/(?P<client_id>\d+)/update_client/$', 'update_client', name='update_client'),
    url(r'^Mindwell/show_client/$', 'show_client', name='show_client'),
    url(r'^Mindwell/(?P<client_id>\d+)/show_specific_client/$', 'show_specific_client',
        name='show_specific_client'),
    url(r'^Mindwell/(?P<dos_id>\d+)/update_dos/$', 'update_dos', name='update_dos'),
    url(r'^Mindwell/(?P<dos_id>\d+)/dos_receipt/$', 'dos_receipt', name='dos_receipt'),
    (r'^Mindwell/(?P<letter>\w+)/show_client_letter/$', 'show_client_letter'),
    url(r'^Mindwell/(?P<search_input>[\s\w-]+)/search_result/$', 'search_result', name='search_result'),
    (r'^Mindwell/search/$', 'search'),
    url(r'^Mindwell/referrer_autocomplete/$', 'referrer_autocomplete',
        name='referrer_autocomplete'),
    url(r'^Mindwell/dsm_code_autocomplete/$', 'dsm_code_autocomplete',
        name='dsm_code_autocomplete'),
    url(r'^Mindwell/(?P<client_id>\d+)/delete_client/$', 'delete_client',
        name='delete_client'),
    url(r'Mindwell/(?P<client_id>\d+)/balance/$', 'client_balance',
        name='client_balance')
)

urlpatterns += patterns('Mindwell.Client.calendar_views',
    #Calendar
    url(r'^Mindwell/calendar/$', 'calendar_display', name='calendar'),
    (r'^Mindwell/calendar_feed', 'calendar_feed'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/calendar/$', 'calendar_display',
        name='calendar_date'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<receipt_dos>\d+)/calendar_print_receipt/$',
        'calendar_display', name='calendar_print_receipt'),
    (r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<minute>\d{2})/calendar/$', 'calendar_display'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<minute>\d{2})/(?P<dos_id>\d+)/calendar_dos/$', 'calendar_display', name='calendar_dos'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<hour>\d{2})/(?P<minute>\d{2})/(?P<dos_recurr_id>\d+)/calendar_dos_recurr/$', 'calendar_display', name='calendar_dos_recurr'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<dos_id>\d+)/calendar/$', 'calendar_update_dos', name='calendar_update_dos'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<dos_id>\d+)/calendar_delete_dos/$', 'calendar_delete_dos', name='calendar_delete_dos'),
    url(r'^Mindwell/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<dos_id>\d+)/calendar_cancel_all_series_dos/$', 'calendar_cancel_all_series_dos', name='calendar_cancel_all_series_dos')
)

