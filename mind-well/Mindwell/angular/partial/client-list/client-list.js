angular.module('mindwell').controller('ClientListCtrl', function($scope, mindwellRest, $filter, ngTableParams) {


    $scope.clients = [];
    mindwellRest.clients.getList().then(function(clients) {
        $scope.clients = clients;
    });

    $scope.filters = {
        lastname: ''
    };

    $scope.tableParams = new ngTableParams({ //jshint ignore:line
        page: 1, // show first page
        count: 1000, // count per page
        sorting: {
            lastname: 'asc' // initial sorting
        },
        filter: $scope.filters,
    }, {
        total: 1,
        counts: [],
        getData: function($defer, params) {
            var orderedData = params.filter() ?
                $filter('filter')($scope.clients, params.filter()) :
                $scope.clients;
            orderedData = params.sorting() ?
                $filter('orderBy')(orderedData, params.orderBy()) :
                orderedData;
            $defer.resolve(orderedData);
        }
    });


});
