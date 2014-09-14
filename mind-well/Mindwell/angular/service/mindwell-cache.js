angular.module('mindwell').factory('mindwellCache', function(mindwellRest) {

    var mindwellCache = {};

    mindwellRest.clients.getList().then(function(clients) {
        mindwellCache.clients = clients;
    });

    return mindwellCache;
});
