angular.module('mindwell').directive('mwInvoicesTable', function(ngTableParams, mindwellCache, $filter, mindwellUtil) {
    return {
        restrict: 'E',
        replace: true,
        require: 'ngModel',
        scope: {

        },
        templateUrl: 'directive/mw-invoices-table/mw-invoices-table.html',
        link: function(scope, element, attrs, ngModel) {
            scope.filter = {text: ''};
            scope.invoiceFilter = function(invoice) {
                return $filter('filter')([scope.getClient(invoice)], {$: scope.filter.text}).length === 1;
            };
            scope.invoiceTableCols = [{
                title: 'Client',
                field: 'clientinfo',
                visible: true
            }, {
                title: 'Invoice (Attended DOS Only)',
                field: 'attended_only',
                visible: true
            }, {
                title: 'Invoice (All DOS)',
                field: 'all_dos',
                visible: true
            }, {
                title: 'Invoice Start Date',
                field: 'start_date',
                visible: true
            }, {
                title: 'Invoice End Date',
                field: 'end_date',
                visible: true
            }];
            scope.clients = [];
            mindwellCache.getClients().then(function(clients) {
                scope.clients = clients;
            });
            scope.getClient = function(invoice) {
                return _.find(scope.clients, {
                    id: invoice.clientinfo
                });
            };

            ngModel.$render = function() {
                if (scope.tableParams) {
                    scope.tableParams.reload();
                    return;
                }
                scope.tableParams = new ngTableParams({ //jshint ignore:line
                    page: 1, // show first page
                    count: 1000, // count per page
                    sorting: {
                        dos_datetime: 'desc' // initial sorting
                    },
                    filter: scope.filters,
                }, {
                    total: 1,
                    counts: [],
                    getData: function($defer, params) {
                        $defer.resolve(ngModel.$modelValue);
                    }
                });
            };
            scope.getInvoiceURL = function(invoice, type) {
                return mindwellUtil.getInvoiceURL(invoice, type);
            };
        }
    };
});
