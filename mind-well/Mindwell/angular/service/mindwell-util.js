angular.module('mindwell').factory('mindwellUtil', function($location) {

    var mindwellUtil = {};

    mindwellUtil.onEditClient = function(client) {
        $location.path('/client-detail').search({
            'contentId': client.id
        });
    };

    mindwellUtil.generateClientInvoicesByDate = function(start, end) {
        var dateFormat = 'YYYY/MM/DD';
        window.location = '/Mindwell/' + start.format(dateFormat) + '/' + end.format(dateFormat) + '/generate_client_invoices_by_date';
    };

    mindwellUtil.generateProviderInvoicesByDate = function(start, end) {
        var dateFormat = 'YYYY/MM/DD';
        window.location = '/Mindwell/' + start.format(dateFormat) + '/' + end.format(dateFormat) + '/provider_invoices';
    };


    return mindwellUtil;
});
