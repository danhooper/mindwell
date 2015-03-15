angular.module('mindwell').controller('CalendarCtrl',function($scope, mindwellCache, uiCalendarConfig, mindwellRest){
    $scope.newDOS = {};

    $scope.dayClick = function(date, jsEvent, view) {
        console.log('day clicked', arguments);
        $scope.newDOS = {dos_datetime: date};
    };

    $scope.calConfig = {
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultEventMinutes: 15,
        defaultView: 'agendaWeek',
        editable: false,
        allDaySlot: false,
        slotDuration: '00:15:00',
        weekMode: 'liquid',
        dayClick: $scope.dayClick,
        displayEventEnd: {month: true, basicWeek: true, 'default': true},
        timeFormat: 'h:mm',
            eventRender: function(event, element) {
                    $('.fc-event-title', element).html(event.title + '<br/>' + event.note);
            }
    };

    mindwellCache.getCalSettings().then(function(calSettings) {
        console.log(calSettings);
        $scope.calConfig.weekends = calSettings.show_weekends;
        $scope.scrollTime = calSettings.calendar_start_time;
    });
    var eventsFunc = function(start, end, timezone, callback) {
        console.log(arguments);
        start = start.format('YYYY-MM-DD');
        end = end.format('YYYY-MM-DD');
        mindwellRest.calEvents.getList({'start': start, 'end': end}).then(function(events) {
            callback(events);
        });
    };

    $scope.toggleWeekends = function() {
        $scope.calConfig.weekends = !$scope.calConfig.weekends;
    };

    $scope.eventSources = [eventsFunc];


});
