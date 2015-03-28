angular.module('mindwell').controller('ClientDetailCtrl', function($scope, $location, mindwellRest, Restangular, mindwellCache, $modal) {
    var search = $location.search();
    $scope.contentId = search['contentId'];

    if ($scope.contentId === -1 || !$scope.contentId) {
        $scope.client = {
            client_status: 'Active'
        };
    } else {
        mindwellRest.clients.get($scope.contentId).then(function(client) {
            $scope.client = client;
        });
    }

    $scope.$on('mw-client-updated', function() {
        $location.path('client-list').search({
            'contentId': null
        });
    });


});
