angular.module('mindwell').controller('CalendarCtrl', function($scope, mindwellCache, uiCalendarConfig, mindwellRest, mindwellUtil, $timeout, $rootScope) {
    $scope.newDOS = {};

    $rootScope.linkActive = {calendar:  true};

    var getCalendar = function() {
        return uiCalendarConfig.calendars.mwCalendar;
    };
    $scope.$on('mw-dos-updated', function() {
        $scope.newDOS = {};
        getCalendar().fullCalendar('refetchEvents');
    });

    $scope.dayClick = function(date, jsEvent, view) {
        $scope.newDOS = {
            dos_datetime: date,
            dos_endtime: moment(date).add(45, 'minutes') // make copy
        };
        $scope.client = undefined;
    };

    $scope.eventClick = function(event, jsEvent) {
        mindwellCache.getClients().then(function() {
            $scope.client = _.find(mindwellCache.clients, {id: event.clientinfo});
            if ($scope.client.dosList) {
                return _.find($scope.client.dosList, {id: event.id});
            } else {
                return mindwellRest.dos.get(event.id);
            }
        }).then(function(dos) {
            $scope.newDOS = dos;
        });
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
        eventClick: $scope.eventClick,
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
        $scope.calConfig.weekends = calSettings.show_weekends;
        $scope.scrollTime = calSettings.calendar_start_time;
        $timeout(function() {
            $scope.eventSources.push(eventsFunc);
        });
    });
    var eventsFunc = function(start, end, timezone, callback) {
        start = start.format('YYYY-MM-DD');
        end = end.format('YYYY-MM-DD');
        mindwellRest.calEvents.getList({
            'start': start,
            'end': end
        }).then(function(events) {
            _.each(events, function(event) {
                delete event.url;
            });
            callback(events);
        });
    };
    $scope.eventSources = [];

    $scope.toggleWeekends = function() {
        $scope.calConfig.weekends = !$scope.calConfig.weekends;
    };


    $scope.generate = function() {
        var view = getCalendar().fullCalendar('getView');
        var start = view.intervalStart;
        var end = view.intervalEnd.subtract(1, 'days');
        if ($scope.generateChoice.type === 'Client Invoice') {
            mindwellUtil.generateClientInvoicesByDate(start, end);
        } else if ($scope.generateChoice.type === 'Provider Report') {
            mindwellUtil.generateProviderInvoicesByDate(start, end);
        }
    };

});
