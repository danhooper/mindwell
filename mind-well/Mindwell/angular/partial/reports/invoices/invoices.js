angular.module('mindwell').controller('InvoicesCtrl', function(
    $scope, mindwellCache, mindwellRest, mindwellUtil, $location, $http) {

    $scope.generatedInvoices = [];
    $scope.allInvoices = [];

    mindwellCache.getInvoices().then(function(invoices) {
        $scope.allInvoices = invoices;
        var search = $location.search();
        if (search.start && search.end) {
            $http.post('/Mindwell/rest/invoice/by_date', {
                start: search.start,
                end: search.end
            }).then(function(response) {
                _.each(response.data, function(invoice) {
                    $scope.allInvoices.push(invoice);
                    $scope.generatedInvoices.push(invoice);
                });
                $scope.allInvoices = _.uniq($scope.allInvoices, 'id');
            });
        }

    });
    mindwellCache.getClients().then(function() {
        $scope.clients = mindwellCache.clients;
    });
    $scope.startOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.startOpened = true;
    };
    $scope.endOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.endOpened = true;
    };

    var createFormDate = function(form, prefix, value) {
        value = moment(value);
        form[prefix + 'year'] = value.year();
        form[prefix + 'month'] = value.month() + 1; // python has 1 based months
        form[prefix + 'day'] = value.date();
    };

    $scope.generate = function() {
        $scope.genForm.clientinfo = $scope.client.id;
        createFormDate($scope.genForm, 'start_date_', $scope.genForm.start_date);
        createFormDate($scope.genForm, 'end_date_', $scope.genForm.end_date);
        mindwellRest.invoice.post($scope.genForm).then(function(invoice) {
            $scope.allInvoices.push(invoice);
            $scope.generatedInvoices.push(invoice);
            mindwellUtil.openInvoice(invoice, 'attended_only');
        });
    };

    $scope.genForm = {start_date: new Date(), end_date: new Date()};
    $scope.client = {};

});
