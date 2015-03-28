angular.module('mindwell').controller('MwClientModalCtrl', function($scope, mindwellUtil, $modalInstance) {
    $scope.client = {};

    $scope.saveClient = function() {
        mindwellUtil.saveClient($scope.client).then(function(client) {
            $modalInstance.close(client);
        });
    };

});
