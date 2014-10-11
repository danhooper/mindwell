angular.module('mindwell').factory('mindwellCache', function(mindwellRest, $rootScope, $q) {

    var mindwellCache = {};


    mindwellCache.getClients = function() {
        mindwellCache._clientsDefer = $q.defer();
        if (mindwellCache.clients) {
            mindwellCache._clientsDefer.resolve(mindwellCache.clients);
        } else if (!mindwellCache._clientsRunning) {
            mindwellCache._clientsRunning = true;
            mindwellRest.clients.getList().then(function(clients) {
                mindwellCache.clients = clients;
                $rootScope.$emit('mindwell.clientsUpdated');
                mindwellCache._clientsDefer.resolve(mindwellCache.clients);
            });
        }
        return mindwellCache._clientsDefer.promise;

    };


    return mindwellCache;
});
