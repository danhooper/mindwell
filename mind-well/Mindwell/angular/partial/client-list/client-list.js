angular.module('mindwell').controller('ClientListCtrl',function($scope, mindwellRest){

    mindwellRest.clients.getList().then(function(clients) {
        $scope.clients = clients;
    });


});
