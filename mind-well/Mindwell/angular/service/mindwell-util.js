angular.module('mindwell').factory('mindwellUtil', function($location) {

    var mindwellUtil = {};

    mindwellUtil.onEditClient = function(client) {
        $location.path('/client-detail').search({
            'contentId': client.id
        });
    };

    return mindwellUtil;
});
