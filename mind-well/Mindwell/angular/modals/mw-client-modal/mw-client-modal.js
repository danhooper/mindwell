angular.module('mindwell').controller('MwClientModalCtrl', function($scope, mindwellUtil, $modalInstance, mindwellCache) {
    $scope.client = {};

    $scope.closeModal = function() {
        $modalInstance.close($scope.client);
    };

    $scope.saveClient = function() {
        mindwellUtil.saveClient($scope.client).then(function(client) {
            $scope.client = client;
            return mindwellCache.getCustomForm();
        }).then(function(customForm) {
            $scope.customForm = customForm;
            if (customForm.new_client_script) {
                $scope.showScript = true;
            } else {
                $scope.closeModal();
            }
        });
    };

});
