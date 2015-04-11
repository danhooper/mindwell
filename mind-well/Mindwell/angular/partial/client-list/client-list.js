angular.module('mindwell').controller('ClientListCtrl', function($scope, $rootScope, $location, mindwellRest, $filter, ngTableParams, prompt, $timeout, mindwellCache, mindwellUtil) {

    $rootScope.linkActive = {
        clients: true
    };
    $scope.mindwellCache = mindwellCache;
    $scope.currentLetter = {};
    var letterMatchesLastname = function(client, letter) {
        return client.lastname && client.lastname.length > 1 && client.lastname[0].toUpperCase() === letter;
    };
    var buildClientLetters = function() {
        var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $scope.clientLetters = _.map(letters, function(letter) {
            var clientLetter = {
                letter: letter
            };
            clientLetter.link = _.find(mindwellCache.clients, function(client) {
                return letterMatchesLastname(client, letter);
            });
            return clientLetter;

        });
    };
    $scope.clientFilter = {text: $location.search().search};
    $rootScope.$on('mindwell.clientsUpdated', function() {
        buildClientLetters();
        $scope.tableParams.reload();
    });
    mindwellCache.getClients().then(function() {

        buildClientLetters();
    });
    $scope.clientLetters = [];

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
            mindwellCache.getClients().then(function() {
                var orderedData = mindwellCache.clients;
                orderedData = params.sorting() ?
                    $filter('orderBy')(orderedData, params.orderBy()) :
                    orderedData;
                if ($scope.currentLetter.letter) {
                    orderedData = _.filter(orderedData, function(client) {
                        return letterMatchesLastname(client, $scope.currentLetter.letter);
                    });
                }
                $scope.calcBalance(true);
                $defer.resolve(orderedData);
                $timeout(function() {
                    $scope.$apply();
                });
            });
        }
    });

    $scope.onDelete = function(client) {
        prompt({
            title: 'Delete ' + client.firstname + ' ' + client.lastname,
            message: 'Are you sure you want to delete ' + client.firstname + ' ' + client.lastname + ' and all of their dates of service?'
        }).then(function() {
            return client.remove();
        }).then(function() {
            mindwellCache.clients = _.without(mindwellCache.clients, client);
            $scope.tableParams.reload();
        });
    };

    $scope.addClient = function() {
        $location.path('/client-detail');
    };
    $scope.calcBalance = function(cachedOnly) {
        _.forEach(mindwellCache.clients, function(client) {
            if (client.dosList) {
                var balances = mindwellUtil.calcBalances(client.dosList);
                client.balance = balances.length > 0 ? balances[0].balance : 0;
            } else if (!cachedOnly){
                mindwellRest.balance.get(client.id).then(function(balance) {
                    client.balance = balance.balance;
                });
            }
        });
    };
    $scope.filterByLetter = function(letter) {
        $scope.currentLetter = letter;
        $scope.tableParams.reload();
    };
    $scope.showAll = function() {
        $location.search('search', null);
        $scope.filterByLetter({});
        $scope.clientFilter.text = '';
    };

    $scope.clientDos = function(client) {
        $location.path('client-dos').search('contentId', client.id);
        //window.location = '/Mindwell/' + client.id + '/show_specific_client/';
    };
});
