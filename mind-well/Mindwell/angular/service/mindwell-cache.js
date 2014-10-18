angular.module('mindwell').factory('mindwellCache', function(mindwellRest, $rootScope, $q) {

    var mindwellCache = {};

    mindwellCache._clientsDefer = $q.defer();
    mindwellCache.getClients = function(force) {
        if (force) {
            mindwellCache._clientsDefer = $q.defer();
        }
        if (mindwellCache.clients && !force) {
            mindwellCache._clientsDefer.resolve(mindwellCache.clients);
        } else if (!mindwellCache._clientsRunning || force) {
            mindwellCache._clientsRunning = true;
            mindwellRest.clients.getList().then(function(clients) {
                mindwellCache.clients = clients;
                $rootScope.$emit('mindwell.clientsUpdated');
                mindwellCache._clientsDefer.resolve(mindwellCache.clients);
            });
        }
        return mindwellCache._clientsDefer.promise;
    };

    mindwellCache._customFormDefer = $q.defer();
    mindwellCache.getCustomForm = function(force) {
        if (force) {
            mindwellCache._customFormDefer = $q.defer();
        }
        if (mindwellCache.customForm && !force) {
            mindwellCache._customFormDefer.resolve(mindwellCache.customForm);
        } else if (!mindwellCache._customFormRunning || force) {
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

    mindwellCache.getUserPerm = function() {
        mindwellCache._userPermDefer = $q.defer();
        if (mindwellCache.userPerm) {
            mindwellCache._userPermDefer.resolve(mindwellCache.userPerm);
        } else if (!mindwellCache._userPermRunning) {
            mindwellCache._userPermRunning = true;
            mindwellRest.userPerm.getList().then(function(userPerm) {
                mindwellCache.userPerm = userPerm;
                $rootScope.$emit('mindwell.userPermUpdated');
                mindwellCache._userPermDefer.resolve(mindwellCache.userPerm);
            });
        }
        return mindwellCache._userPermDefer.promise;
    };

    mindwellCache.getClients();
    mindwellCache.getCustomForm();
    mindwellCache.getUserPerm();

    return mindwellCache;
});
