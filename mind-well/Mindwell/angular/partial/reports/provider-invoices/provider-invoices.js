angular.module('mindwell').controller('ProviderInvoicesCtrl', function($scope, mindwellRest, ngTableParams, mindwellCache, mindwellUtil, $rootScope) {


    $scope.startOpened = false;
    $scope.endOpened = false;

    mindwellCache.getClients().then(function() {
        // noop to ensure we get clients cached for display
    });
    $scope.dosList = [];
    $scope.generate = function() {
        var params = {
            start: moment($scope.genForm.start).format('YYYY-MM-DD'),
            end: moment($scope.genForm.end).format('YYYY-MM-DD'),
        };
        $rootScope.busy = mindwellRest.dos.getList(params).then(function(dosList) {
            $scope.dosList = dosList;
            var dosByCat = _.groupBy($scope.dosList, 'type_pay');
            $scope.dosSummary = {};
            $scope.total = 0;
            _.each(Object.keys(dosByCat), function(cat) {
                var sum = 0;
                $scope.dosSummary[cat] = _.reduce(dosByCat[cat], function(prevValue, dos) {
                    return prevValue + (parseFloat(dos.amt_paid) || 0);
                }, sum);
                $scope.total += $scope.dosSummary[cat];
            });
            $scope.tableParams.reload();
        });
    };

    $scope.genForm = {
        start: new Date(),
        end: new Date()
    };
    $scope.invoiceTableCols = [{
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
    }];
    $scope.tableParams = new ngTableParams({ //jshint ignore:line
        page: 1, // show first page
        count: 1000, // count per page
        sorting: {
            dos_datetime: 'desc' // initial sorting
        },
        filter: $scope.filters,
    }, {
        total: 1,
        counts: [],
        getData: function($defer, params) {
            $defer.resolve($scope.dosList);
        }
    });
    $scope.getClient = function(dos) {
        return _.find(mindwellCache.clients, {
            id: dos.clientinfo
        });
    };

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
});
