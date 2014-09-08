angular.module('mindwell').controller('ClientDetailCtrl',function($scope, $location, mindwellRest, Restangular){
    var search = $location.search();
    $scope.contentId = search['contentId'];

    if ($scope.contentId === -1 || !$scope.contentId) {
        $scope.client = {};
    } else {
       mindwellRest.clients.get($scope.contentId).then(function(client) {
       //Restangular.one('clientinfo', $scope.contentId).then(function(client) {
            $scope.client = client;
        });
    }

    $scope.messageOptions = [
        {text: 'Message Not OK', value: 'Message Not OK'},
        {text: 'Message OK', value: 'Message OK'}
    ];


});
