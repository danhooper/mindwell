angular.module('mindwell').controller('ClientDosFormCtrl',function($scope, $timeout, $modal, mindwellCache, mindwellRest){
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

    $scope.dosList = [];
    mindwellRest.dos.getList().then(function(dosList) {
        $scope.dosList = dosList;
    });

    var timeFormat = 'hh:mm a';

    $scope.starttime = '12:00 am';
    $scope.endtime = '12:00 am';

    var getEndDisplay = function(value) {
        var end = moment(value, timeFormat);
        var start = moment($scope.starttime, timeFormat);
        return value + ' (' + end.diff(start, 'minutes') + ' mins)';
    };

    var buildTimeChoices = function() {
        var minutes = _.range(0, 24 * 60, 15);
        $scope.timeChoices = _.map(minutes, function(minute) {
            var day = moment('2013-02-08');
            return day.add(minute, 'minutes').format(timeFormat);
        });
        $scope.endTimeChoices = _.map($scope.timeChoices, function(choice) {
            return [choice, getEndDisplay(choice)];
        });
        var end = moment($scope.endtime, timeFormat);
        var start = moment($scope.starttime, timeFormat);
        if (end < start) {
            $scope.endtime = $scope.starttime;
        }
    };
    buildTimeChoices();

    $scope.updateEndTime = function() {
        buildTimeChoices();
    };

    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };
    $scope.endOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.endOpened = true;
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

    $scope.addNewDOS = function() {
        $scope.newDos.dos_datetime = $scope.date + $scope.starttime;
        $scope.newDos.dos_endtime = $scope.endtime;
        mindwellRest.dos.post($scope.newDos).then(function(dos) {
            $scope.dosList.push(dos);
        });
    };

});
