angular.module('mindwell').controller('CalendarCtrl', function(
    $scope, mindwellCache, uiCalendarConfig, mindwellRest, mindwellUtil,
    $timeout, $rootScope, $location) {

    $scope.newDOS = {};

    $rootScope.linkActive = {calendar:  true};

    var getCalendar = function() {
        return uiCalendarConfig.calendars.mwCalendar;
    };
    $scope.$on('mw-dos-updated', function() {
        $scope.newDOS = {};
        getCalendar().fullCalendar('refetchEvents');
    });
    $scope.$on('mw-dos-deleted', function() {
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
            if ($scope.client && $scope.client.dosList) {
                return _.find($scope.client.dosList, {id: event.id});
            } else if (event.id !== -1){
                return mindwellRest.dos.get(event.id);
            }
        }).then(function(dos) {
            if (!dos) {
                dos = {dos_datetime: event.start, dos_endtime: event.end, clientinfo: event.clientinfo, recurrId: event.recurrId};
            }
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
        defaultDate: $location.search().date,
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        height: 'auto',
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
            var fields = [];
            if (event.title && event.title.length > 0) {
                fields.push(event.title);
            }
            if (event.note && event.note.length > 0) {
                fields.push(event.note);
            } else {
                fields.push('&nbsp;');
            }
            $('.fc-title', element).html(fields.join('<br>'));
        }
    };

    mindwellCache.getCalSettings().then(function(calSettings) {
        $scope.calConfig.weekends = calSettings.show_weekends === 'Yes';
        $scope.calConfig.scrollTime = moment(calSettings.calendar_start_time, 'h a').format('HH:mm:ss');
        $timeout(function() {
            $scope.eventSources.push(eventsFunc);
        });
    });
    var eventsFunc = function(start, end, timezone, callback) {
        start = start.format('YYYY-MM-DD');
        end = end.format('YYYY-MM-DD');
        $rootScope.busy = mindwellRest.calEvents.getList({
            'start': start,
            'end': end
        }).then(function(events) {
            _.each(events, function(event) {
                // otherwise events look too long on the calendar
                if (event.start === event.end) {
                    event.end = moment(event.end).add(1, 'minute');
                }
                // force cancelled and no show to 1 minute
                // TODO: Add session_result to dos dictionary returned
                if (event.backgroundColor === 'gray' || event.backgroundColor === 'red') {
                    event.end = moment(event.start).add(1, 'minute');
                }
                delete event.url;
            });
            callback(events);
        });
    };
    $scope.eventSources = [];

    $scope.toggleWeekends = function() {
        $scope.calConfig.weekends = !$scope.calConfig.weekends;
        $scope.calConfig.defaultView = getCalendar().fullCalendar('getView').name;
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

    $scope.$on('mw-dos-form-cancel', function() {
        $scope.newDOS = {};
    });
    $scope.$on('mw.calendarMenuClicked', function() {
        $scope.newDOS = {};
    });

    $scope.$on('mw-change-user', function() {
        getCalendar().fullCalendar('refetchEvents');
    });

    $scope.$on('$locationChangeStart', function(event) {
        if (!_.isEmpty($scope.newDOS)) {
            event.preventDefault();
            $scope.newDOS = {};
        }
    });

});
