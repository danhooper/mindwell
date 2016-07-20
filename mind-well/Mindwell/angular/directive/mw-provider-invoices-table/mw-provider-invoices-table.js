angular.module('mindwell').directive('mwProviderInvoicesTable', function(mindwellCache, ngTableParams) {
    return {
        restrict: 'E',
        replace: true,
        require: 'ngModel',
        scope: {

        },
        templateUrl: 'directive/mw-provider-invoices-table/mw-provider-invoices-table.html',
        link: function(scope, element, attrs, ngModel) {
            scope.clients = [];
            mindwellCache.getClients().then(function(clients) {
                scope.clients = clients;
            });
            scope.invoiceTableCols = [{
                title: 'Date of Service',
                field: 'dos_datetime',
                visible: true
            }, {
                title: 'Client',
                field: 'clientinfo',
                visible: true
            }, {
                title: 'Type of Payment',
                field: 'type_pay',
                visible: true
            }, {
                title: 'Amount Due',
                field: 'amt_due',
                visible: true
            }, {
                title: 'Amount Paid',
                field: 'amt_paid',
                visible: true
            }, {
                title: 'Adjustment',
                field: 'adjustment',
                visible: true
            }];

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
            scope.getClient = function(dos) {
                return _.find(mindwellCache.clients, {
                    id: dos.clientinfo
                });
            };


        }
    };
});

