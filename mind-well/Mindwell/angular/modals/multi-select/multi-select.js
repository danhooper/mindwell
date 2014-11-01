angular.module('mindwell').controller('MultiSelectCtrl',function($scope, choices, currValue, $modalInstance, title){
    $scope.choices = _.map(choices, function(choice) {
        return {value: false, name: choice};
    });
    $scope.choices = _.filter($scope.choices, function(choice) {
        return choice.name;
    });

    $scope.other = '';
    $scope.title = title;

    if (!currValue) {
        currValue = '';
    }

    _.forEach(currValue.split(', '), function(value) {
        var choice = _.find($scope.choices, function(choice) {
            return choice.name === value;
        });
        if (choice) {
            choice.value = true;
        } else {
            $scope.other += value;
        }
    });

    var partition = function(arr, size) {
        var newArr = [];
        for (var i=0; i<arr.length; i+=size) {
            newArr.push(arr.slice(i, i+size));
        }
        return newArr;
    };

    $scope.choiceRows = partition($scope.choices, 3);


    $scope.updateMultiSelect = function() {
        var selected = _.filter($scope.choices, function(choice) {
            return choice.value;
        });
        var selectedNames = _.map(selected, function(choice) {
            return choice.name;
        });
        if ($scope.other) {
            selectedNames.push($scope.other);
        }
        currValue = selectedNames.join(', ');
        $modalInstance.close(currValue);
    };


});
