angular.module('mindwell').directive('mwDosForm', function(mindwellRest, mindwellCache, $modal, prompt, mindwellUtil, $q) {
    var timeFormat = 'hh:mm a';
    var mwEndTimeFormat = 'hh:mm:ss';
    return {
        restrict: 'E',
        replace: true,
        require: 'ngModel',
        scope: {
            mwClient: '=',
            mwShowAddNewClient: '=',
            mwShowReceipt: '=',
            mwShowClientList: '='
        },
        templateUrl: 'directive/mw-dos-form/mw-dos-form.html',
        link: function(scope, element, attrs, ngModel) {
            ngModel.$render = function() {
                scope.newDOS = ngModel.$modelValue;
                if (!scope.newDOS.id) {
                    _.merge(scope.newDOS, {
                        session_result: 'Scheduled',
                        dos_repeat: 'No',
                    });
                }
                scope.blockedTime = false;
                scope.blockedTimeChange = function() {
                    scope.blockedTime = !scope.blockedTime;
                };
                mindwellCache.getClients().then(function() {
                    scope.clients = mindwellCache.clients;
                    if (scope.mwClient) {
                        scope.client = _.find(mindwellCache.clients, {
                            id: scope.mwClient.id
                        });
                    } else if (scope.mwShowClientList && scope.newDOS.id) {
                        scope.blockedTime = true;
                    }
                });
                scope.date = moment(scope.newDOS.dos_datetime).toDate();
                if (scope.newDOS.dos_datetime) {
                    scope.starttime = moment(scope.newDOS.dos_datetime).format(timeFormat);
                    scope.endtime = moment(scope.newDOS.dos_endtime, mwEndTimeFormat).format(timeFormat);
                } else {
                    scope.starttime = '08:00 am';
                    scope.endtime = '08:45 am';
                }

                scope.resultChoices = [
                    'Scheduled',
                    'Attended',
                    'No Show',
                    'Cancellation - Late',
                    'Cancellation - Timely',
                    'Payment Received'
                ];
                scope.dosRepeatChoices = [
                    'No',
                    'One Day',
                    'One Week',
                    'Two Weeks',
                    'Three Weeks',
                    'Four Weeks'
                ];


                var getEndDisplay = function(value) {
                    var end = moment(value, timeFormat);
                    var start = moment(scope.starttime, timeFormat);
                    return value + ' (' + end.diff(start, 'minutes') + ' mins)';
                };

                var buildTimeChoices = function() {
                    var minutes = _.range(0, 24 * 60, 15);
                    scope.timeChoices = _.map(minutes, function(minute) {
                        var day = moment('2013-02-08');
                        return day.add(minute, 'minutes').format(timeFormat);
                    });
                    scope.endTimeChoices = _.map(scope.timeChoices, function(choice) {
                        return [choice, getEndDisplay(choice)];
                    });
                    var end = moment(scope.endtime, timeFormat);
                    var start = moment(scope.starttime, timeFormat);
                    if (end < start) {
                        scope.endtime = scope.starttime;
                    }
                };
                buildTimeChoices();

                scope.updateEndTime = function() {
                    buildTimeChoices();
                };

                scope.open = function($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    scope.opened = true;
                };
                scope.endOpen = function($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    scope.endOpened = true;
                };
                mindwellCache.getCustomForm().then(function(customForm) {
                    scope.customForm = customForm;
                });
                scope.sessionTypeModal = function() {
                    $modal.open({
                        templateUrl: 'modals/multi-select/multi-select.html',
                        controller: 'MultiSelectCtrl',
                        resolve: {
                            choices: function() {
                                return scope.customForm.session_type_choices.split('\r\n');
                            },
                            currValue: function() {
                                return scope.newDOS.session_type;
                            },
                            title: function() {
                                return 'Session Type';
                            }
                        }
                    }).result.then(function(result) {
                        scope.newDOS.session_type = result;
                    });
                };

                scope.updateDOS = function(newDOS) {
                    var client = {};
                    newDOS.dos_datetime_0 = moment(scope.date).format('YYYY-MM-DD');
                    newDOS.dos_datetime_1_time = scope.starttime;
                    newDOS.dos_endtime_time = scope.endtime;
                    if (scope.client) {
                        newDOS.clientinfo = scope.client.id;
                    }
                    var savedDOS;

                    $q.when(newDOS).then(function(newDOS) {
                        if (newDOS.id) {
                            return newDOS.put();
                        } else {
                            return mindwellRest.dos.post(newDOS);
                        }
                    }).then(function(dos) {
                        savedDOS = dos;
                        return mindwellUtil.updateDOSCache(dos, newDOS.id && newDOS.id > 0);
                    }).then(function() {
                        if (newDOS.print_receipt) {
                            mindwellUtil.printReceipt(savedDOS);
                        }
                        scope.$emit('mw-dos-updated', savedDOS);
                    });
                };

                scope.cancel = function() {
                    scope.$emit('mw-dos-form-cancel');
                };

                scope.delete = function() {
                    mindwellUtil.deleteDOS(scope.newDOS, scope.client);
                };


                scope.addNewClient = function() {
                    $modal.open({
                        templateUrl: 'modals/mw-client-modal/mw-client-modal.html',
                        controller: 'MwClientModalCtrl'
                    }).result.then(function(client) {
                        scope.client = _.find(mindwellCache.clients, {
                            id: client.id
                        });
                    });

                };

                scope.cancelRecurr = function() {
                    var savedDOS, date, starttime, endtime;
                    mindwellRest.dos.get(scope.newDOS.recurrId).then(function(dos) {
                        dos.dos_repeat = 'No';
                        date = moment(dos.dos_datetime).toDate();
                        starttime = moment(dos.dos_datetime).format(timeFormat);
                        endtime = moment(dos.dos_endtime, mwEndTimeFormat).format(timeFormat);
                        dos.dos_datetime_0 = moment(date).format('YYYY-MM-DD');
                        dos.dos_datetime_1_time = starttime;
                        dos.dos_endtime_time = endtime;
                        return dos.put();
                    }).then(function(dos) {
                        savedDOS = dos;
                        return mindwellUtil.updateDOSCache(dos, true);
                    }).then(function() {
                        scope.$emit('mw-dos-updated', savedDOS);
                    });
                };
            };


        }
    };
});
