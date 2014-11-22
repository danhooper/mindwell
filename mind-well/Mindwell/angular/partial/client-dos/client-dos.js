angular.module('mindwell').controller('ClientDosCtrl',function($scope, $location, mindwellCache){
    var contentId = parseInt($location.search().contentId);
    mindwellCache.getClients().then(function() {
        $scope.client = _.find(mindwellCache.clients, function(client) {
            return contentId === client.id;
        });
    });

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
