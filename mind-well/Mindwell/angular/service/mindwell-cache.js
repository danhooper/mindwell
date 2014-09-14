angular.module('mindwell').factory('mindwellCache', function(mindwellRest, $rootScope) {

    var mindwellCache = {};

    mindwellRest.clients.getList().then(function(clients) {
        mindwellCache.clients = clients;
        $rootScope.$emit('mindwell.clientsUpdated');
    });

    return mindwellCache;
});
