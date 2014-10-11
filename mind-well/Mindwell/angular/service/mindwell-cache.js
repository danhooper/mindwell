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

    mindwellCache.getCustomForm = function() {
        mindwellCache._customFormDefer = $q.defer();
        if (mindwellCache.customForm) {
            mindwellCache._customFormDefer.resolve(mindwellCache.customForm);
        } else if (!mindwellCache._customFormRunning) {
            mindwellCache._customFormRunning = true;
            mindwellRest.customForm.getList().then(function(customForm) {
                if (customForm.length === 1) {
                    mindwellCache.customForm = customForm[0];
                } else {
                    mindwellCache.customForm = {referrer_choices: '', reason_for_visit_choices: ''};
                }
                $rootScope.$emit('mindwell.customFormUpdated');
                mindwellCache._customFormDefer.resolve(mindwellCache.customForm);
            });
        }
        return mindwellCache._customFormDefer.promise;
    };

    mindwellCache.getClients();
    mindwellCache.getCustomForm();


    return mindwellCache;
});
