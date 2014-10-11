angular.module('mindwell').controller('ReferrerCtrl',function($scope, customForm, client, $modalInstance){
    $scope.customForm = customForm;
    $scope.referralChoices = _.map(customForm.referrer_choices.split('\r\n'), function(referrer) {
        return {value: false, name: referrer};
    });

    $scope.other = '';

    _.forEach(client.referrer.split(', '), function(referrer) {
        console.log(referrer);
        var choice = _.find($scope.referralChoices, function(choice) {
            return choice.name === referrer;
        });
        if (choice) {
            choice.value = true;
        } else {
            $scope.other += referrer;
        }
    });


    $scope.updateReferrer = function() {
        var selected = _.filter($scope.referralChoices, function(choice) {
            return choice.value;
        });
        var selectedNames = _.map(selected, function(choice) {
            return choice.name;
        });
        if ($scope.other) {
            selectedNames.push($scope.other);
        }
        client.referrer = selectedNames.join(', ');
        $modalInstance.close(client.referrer);
    };


});
