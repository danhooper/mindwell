angular.module('mindwell').controller('CalendarCtrl',function($scope){

    $scope.calConfig = {
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        scrollTime: '{{calendar_start_time}}',
        defaultEventMinutes: 15,
        //defaultView: view,
        //weekends: show_weekends,
        editable: false,
        allDaySlot: false,
        slotDuration: '00:15:00',
        //defaultDate: date,
        weekMode: 'liquid',
        events: "/Mindwell/calendar_feed",
        displayEventEnd: {month: true, basicWeek: true, 'default': true},
        timeFormat: 'h:mm',
        //dayClick: function(date, allDay, jsEvent, view) {
        //    window.location='/Mindwell/' + FormatCalendarDate(date) + '/calendar/';
        //},
        eventRender: function(event, element) {
        //    element.qtip({
        //        content: event.description,
        //        style: 'cream'
        //    });
            $('.fc-event-title', element).html(event.title + '<br/>' + event.note);
        }
    };
    $scope.eventSources = [{url: '/Mindwell/calendar_feed'}];


});
