angular.module('mindwell').controller('ClientListCtrl', function($scope, $location, mindwellRest, $filter, ngTableParams, prompt, $timeout) {

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

    $scope.onDelete = function(client) {
        prompt({
            title: 'Delete ' + client.firstname + ' ' + client.lastname,
            message: 'Are you sure you want to delete ' + client.firstname + ' ' + client.lastname + ' and all of their dates of service?'
        }).then(function() {
            return client.remove();
        }).then(function() {
            $scope.clients = _.without($scope.clients, client);
            $scope.tableParams.reload();
        });
    };

    $scope.onEdit = function(client) {
        $location.path('/client-detail') .search({'contentId': client.id});
    };
});
