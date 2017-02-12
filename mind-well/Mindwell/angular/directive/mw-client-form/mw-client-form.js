angular.module('mindwell').directive('mwClientForm', function(mindwellCache, $modal, $location, mindwellRest, mindwellUtil) {
    return {
        restrict: 'E',
        replace: true,
        require: 'ngModel',
        scope: {
            mwCompactForm: '='
        },
        templateUrl: 'directive/mw-client-form/mw-client-form.html',
        link: function(scope, element, attrs, ngModel) {
            ngModel.$render = function() {
                var defaultClient = {client_status: 'Active'};
                scope.client = ngModel.$modelValue;
                if (scope.client && scope.client.id) {
                    scope.client.dob_year = moment(scope.client.dob).year();
                    scope.client.dob_month = moment(scope.client.dob).month() + 1;
                    scope.client.dob_day = moment(scope.client.dob).date();
                } else if (scope.client) {
                    _.merge(scope.client, defaultClient);
                } else {
                    scope.client = {
                        client_status: 'Active'
                    };
                    scope.dob = {};
                }
                mindwellCache.getCustomForm().then(function(customForm) {
                    scope.customForm = customForm;
                });

                scope.messageOptions = [{
                    text: 'Message Not OK',
                    value: 'Message Not OK'
                }, {
                    text: 'Message OK',
                    value: 'Message OK'
                }];
                scope.usStates = [{
                    "name": "Alabama",
                    "abbreviation": "AL"
                }, {
                    "name": "Alaska",
                    "abbreviation": "AK"
                }, {
                    "name": "American Samoa",
                    "abbreviation": "AS"
                }, {
                    "name": "Arizona",
                    "abbreviation": "AZ"
                }, {
                    "name": "Arkansas",
                    "abbreviation": "AR"
                }, {
                    "name": "California",
                    "abbreviation": "CA"
                }, {
                    "name": "Colorado",
                    "abbreviation": "CO"
                }, {
                    "name": "Connecticut",
                    "abbreviation": "CT"
                }, {
                    "name": "Delaware",
                    "abbreviation": "DE"
                }, {
                    "name": "Florida",
                    "abbreviation": "FL"
                }, {
                    "name": "Georgia",
                    "abbreviation": "GA"
                }, {
                    "name": "Hawaii",
                    "abbreviation": "HI"
                }, {
                    "name": "Idaho",
                    "abbreviation": "ID"
                }, {
                    "name": "Illinois",
                    "abbreviation": "IL"
                }, {
                    "name": "Indiana",
                    "abbreviation": "IN"
                }, {
                    "name": "Iowa",
                    "abbreviation": "IA"
                }, {
                    "name": "Kansas",
                    "abbreviation": "KS"
                }, {
                    "name": "Kentucky",
                    "abbreviation": "KY"
                }, {
                    "name": "Louisiana",
                    "abbreviation": "LA"
                }, {
                    "name": "Maine",
                    "abbreviation": "ME"
                }, {
                    "name": "Maryland",
                    "abbreviation": "MD"
                }, {
                    "name": "Massachusetts",
                    "abbreviation": "MA"
                }, {
                    "name": "Michigan",
                    "abbreviation": "MI"
                }, {
                    "name": "Minnesota",
                    "abbreviation": "MN"
                }, {
                    "name": "Mississippi",
                    "abbreviation": "MS"
                }, {
                    "name": "Missouri",
                    "abbreviation": "MO"
                }, {
                    "name": "Montana",
                    "abbreviation": "MT"
                }, {
                    "name": "Nebraska",
                    "abbreviation": "NE"
                }, {
                    "name": "Nevada",
                    "abbreviation": "NV"
                }, {
                    "name": "New Hampshire",
                    "abbreviation": "NH"
                }, {
                    "name": "New Jersey",
                    "abbreviation": "NJ"
                }, {
                    "name": "New Mexico",
                    "abbreviation": "NM"
                }, {
                    "name": "New York",
                    "abbreviation": "NY"
                }, {
                    "name": "North Carolina",
                    "abbreviation": "NC"
                }, {
                    "name": "North Dakota",
                    "abbreviation": "ND"
                }, {
                    "name": "Ohio",
                    "abbreviation": "OH"
                }, {
                    "name": "Oklahoma",
                    "abbreviation": "OK"
                }, {
                    "name": "Oregon",
                    "abbreviation": "OR"
                }, {
                    "name": "Pennsylvania",
                    "abbreviation": "PA"
                }, {
                    "name": "Rhode Island",
                    "abbreviation": "RI"
                }, {
                    "name": "South Carolina",
                    "abbreviation": "SC"
                }, {
                    "name": "South Dakota",
                    "abbreviation": "SD"
                }, {
                    "name": "Tennessee",
                    "abbreviation": "TN"
                }, {
                    "name": "Texas",
                    "abbreviation": "TX"
                }, {
                    "name": "Utah",
                    "abbreviation": "UT"
                }, {
                    "name": "Vermont",
                    "abbreviation": "VT"
                }, {
                    "name": "Virginia",
                    "abbreviation": "VA"
                }, {
                    "name": "Washington",
                    "abbreviation": "WA"
                }, {
                    "name": "Washington DC",
                    "abbreviation": "DC"
                }, {
                    "name": "West Virginia",
                    "abbreviation": "WV"
                }, {
                    "name": "Wisconsin",
                    "abbreviation": "WI"
                }, {
                    "name": "Wyoming",
                    "abbreviation": "WY"
                }];
                scope.months = [{
                    name: "January",
                    value: 1
                }, {
                    name: "February",
                    value: 2
                }, {
                    name: "March",
                    value: 3
                }, {
                    name: "April",
                    value: 4
                }, {
                    name: "May",
                    value: 5
                }, {
                    name: "June",
                    value: 6
                }, {
                    name: "July",
                    value: 7
                }, {
                    name: "August",
                    value: 8
                }, {
                    name: "September",
                    value: 9
                }, {
                    name: "October",
                    value: 10
                }, {
                    name: "November",
                    value: 11
                }, {
                    name: "December",
                    value: 12
                }];
                scope.years = _.range(1900, moment().year() + 1);
                scope.days = _.range(1, 32);

                scope.statusOptions = [{
                    name: 'Active'
                }, {
                    name: 'Inactive'
                }];
                scope.saveChanges = function() {
                    return mindwellUtil.saveClient(scope.client).catch(function(resp) {
                        scope.errors = _.zipObject(resp.data.errors);
                    });
                };
                scope.referrerModal = function() {
                    $modal.open({
                        templateUrl: 'modals/multi-select/multi-select.html',
                        controller: 'MultiSelectCtrl',
                        resolve: {
                            choices: function() {
                                return scope.customForm.referrer_choices.split('\r\n');
                            },
                            currValue: function() {
                                return scope.client.referrer;
                            },
                            title: function() {
                                return 'Referrer';
                            }
                        }
                    }).result.then(function(result) {
                        scope.client.referrer = result;
                    });
                };
                scope.rfvModal = function() {
                    $modal.open({
                        templateUrl: 'modals/multi-select/multi-select.html',
                        controller: 'MultiSelectCtrl',
                        resolve: {
                            choices: function() {
                                return scope.customForm.reason_for_visit_choices.split('\r\n');
                            },
                            currValue: function() {
                                return scope.client.reason_for_visit;
                            },
                            title: function() {
                                return 'Reason for Visit';
                            }
                        }
                    }).result.then(function(result) {
                        scope.client.reason_for_visit = result;
                    });
                };


            };
        }
    };
});
