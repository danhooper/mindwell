angular.module('mindwell').controller('ClientDosFormCtrl',function($scope, $modal, mindwellCache){
    $scope.resultChoices = [
        'Scheduled',
        'Attended',
        'No Show',
        'Cancellation - Late',
        'Cancellation - Timely',
        'Payment Received'
    ];
    $scope.dosRepeatChoices = [
        'No',
        'One Day',
        'One Week',
        'Two Weeks',
        'Three Weeks',
        'Four Weeks'
    ];
    var buildTimeChoices = function() {
        var minutes = _.range(0, 24 * 60, 15);
        $scope.timeChoices = _.map(minutes, function(minute) {
            var day = moment('2013-02-08');
            return day.add(minute, 'minutes').format('hh:mm a');
        });
        console.log(minutes);
    };
    buildTimeChoices();
    $scope.getEndDisplay = function(value) {
        var end = moment(value, 'hh:mm a');
        var start = moment($scope.starttime, 'hh:mm a');
        return value + ' (' + end.diff(start, 'minutes') + ' mins)';
    };
    $scope.starttime = '12:00 am';
    $scope.endtime = '12:00 am';
    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };
    $scope.newDos = {
        session_result: 'Scheduled',
        dos_repeat: 'No'
    };
    mindwellCache.getCustomForm().then(function(customForm) {
        $scope.customForm = customForm;
    });
    $scope.sessionTypeModal = function() {
        $modal.open({
            templateUrl: 'modals/multi-select/multi-select.html',
            controller: 'MultiSelectCtrl',
            resolve: {
                choices: function() {
                    return $scope.customForm.session_type_choices.split('\r\n');
                },
                currValue: function() {
                    return $scope.newDos.session_type;
                },
                title: function() {
                    return 'Session Type';
                }
            }
        }).result.then(function(result){
            $scope.newDos.session_type = result;
        });
    };


});
