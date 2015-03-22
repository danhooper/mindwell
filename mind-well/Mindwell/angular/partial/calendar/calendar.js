angular.module('mindwell').controller('CalendarCtrl', function($scope, mindwellCache, uiCalendarConfig, mindwellRest, mindwellUtil, $timeout) {
    $scope.newDOS = {};

    $scope.dayClick = function(date, jsEvent, view) {
        console.log('day clicked', arguments);
        $scope.newDOS = {
            dos_datetime: date
        };
    };

    $scope.viewRender = function(view, element) {
        $scope.currentView = view.name;
    };

    $scope.generateOptions = {
        month: [{
            type: 'Client Invoice',
            label: 'Current Month'
        }, {
            type: 'Provider Report',
            label: 'Current Month'
        }],
        agendaWeek: [{
            type: 'Client Invoice',
            label: 'Current Week'
        }, {
            type: 'Provider Report',
            label: 'Current Week'
        }, ],
        agendaDay: [{
            type: 'Provider Report',
            label: 'Current Day'
        }]
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
        viewRender: $scope.viewRender,
        displayEventEnd: {
            month: true,
            basicWeek: true,
            'default': true
        },
        timeFormat: 'h:mm',
        eventRender: function(event, element) {
            $('.fc-event-title', element).html(event.title + '<br/>' + event.note);
        }
    };

    mindwellCache.getCalSettings().then(function(calSettings) {
        console.log(calSettings);
        $scope.calConfig.weekends = calSettings.show_weekends;
        $scope.scrollTime = calSettings.calendar_start_time;
        $timeout(function() {
            $scope.eventSources.push(eventsFunc);
        });
    });
    var eventsFunc = function(start, end, timezone, callback) {
        console.log(arguments);
        start = start.format('YYYY-MM-DD');
        end = end.format('YYYY-MM-DD');
        mindwellRest.calEvents.getList({
            'start': start,
            'end': end
        }).then(function(events) {
            callback(events);
        });
    };
    $scope.eventSources = [];

    $scope.toggleWeekends = function() {
        $scope.calConfig.weekends = !$scope.calConfig.weekends;
    };


    $scope.generate = function() {
        var view = uiCalendarConfig.calendars.mwCalendar.fullCalendar('getView');
        var start = view.intervalStart;
        var end = view.intervalEnd.subtract(1, 'days');
        if ($scope.generateChoice.type === 'Client Invoice') {
            mindwellUtil.generateClientInvoicesByDate(start, end);
        } else if ($scope.generateChoice.type === 'Provider Report') {
            mindwellUtil.generateProviderInvoicesByDate(start, end);
        }
    };

});
