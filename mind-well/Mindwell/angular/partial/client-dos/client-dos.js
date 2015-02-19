angular.module('mindwell').controller('ClientDosCtrl', function(
    $scope, $location, mindwellCache, mindwellRest, ngTableParams, $filter,
    $timeout, Restangular, prompt, $anchorScroll){

    var contentId = parseInt($location.search().contentId);

    var getDOS = function($defer, params) {
        if ($scope.client.dosList === undefined) {
            mindwellRest.dos.getList().then(function(dosList) {
                $scope.client.dosList = params.sorting() ? $filter('orderBy')(dosList, params.orderBy()) : dosList;

                $defer.resolve($scope.client.dosList);
            });
        } else {
            $scope.client.dosList = params.sorting() ? $filter('orderBy')($scope.client.dosList, params.orderBy()) : $scope.client.dosList;
            $defer.resolve($scope.client.dosList);
        }
    };

    mindwellCache.getClients().then(function() {
        $scope.client = _.find(mindwellCache.clients, function(client) {
            return contentId === client.id;
        });
        $scope.tableParams = new ngTableParams({ //jshint ignore:line
            page: 1, // show first page
            count: 1000, // count per page
            sorting: {
                dos_datetime: 'desc' // initial sorting
            },
            filter: $scope.filters,
        }, {
            total: 1,
            counts: [],
            getData: getDOS
        });
    });

    $scope.newDOS = {
        session_result: 'Scheduled',
        dos_repeat: 'No',
        clientinfo: contentId
    };

    $scope.editDos = function(dos) {
        $scope.newDOS = Restangular.copy(dos);
        $location.hash('dos-form');
        $anchorScroll();
    };

    $scope.deleteDOS = function(dos) {
        prompt({
            title: 'Delete DOS?',
            message: 'Are you sure you want to delete this DOS from ' + dos.dos_datetime + '?'
        }).then(function() {
            return dos.remove();
        }).then(function() {
            $scope.client.dosList = _.without($scope.client.dosList, dos);
            $scope.tableParams.reload();
        });
    };

    $scope.dosTableCols = [
        {title: 'DOS Date and Time',
         field: 'dos_datetime',
         visible: true
        },
        {title: 'Session Type',
         field: 'session_type',
         visible: true
        },
        {title: 'Session Result',
         field: 'session_result',
         visible: true
        },
        {title: 'DMS Code',
         field: 'dsm_code',
         visible: true
        },
        {title: 'Session Result',
         field: 'session_result',
         visible: true
        },
        {title: 'Type of Payment',
         field: 'type_pay',
         visible: true
        },
        {title: 'Amount Due',
         field: 'amt_due',
         visible: true
        },
        {title: 'Amount Paid',
         field: 'amt_paid',
         visible: true
        },
        {title: 'Note',
         field: 'note',
         visible: true
        },
        {title: 'DOS Repeat',
         field: 'dos_repeat',
         visible: true
        },
        {title: 'Repeat End Date',
         field: 'dos_repeat_end_date',
         visible: true
        },
        {title: 'Actions',
         visible: true
        }
    ];
    $scope.getTitle = function(col) {
        return col.title;
    };

    $scope.otherFields = [
        {key: 'dob', display: 'DOB'},
        {key: 'dsm_code', display: 'DSM Code'},
        {key: 'client_status', display: 'Client Status'},
        {key: 'referrer', display: 'Referrer'},
        {key: 'guardians_name', display: 'Guardians Name'},
        {key: 'guardians_phone_number', display: 'Guardians Phone Number'},
        {key: 'emergency_contact', display: 'Emergency Contact'},
        {key: 'emergency_contact_phone_number', display: 'Emergency Contact Phone Number'},
        {key: 'reason_for_visit', display: 'Reason For Visit'},

    ];


});
