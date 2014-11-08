angular.module('mindwell').factory('mindwellCache', function(mindwellRest, $rootScope, $q) {

    var mindwellCache = {};

    mindwellCache._clientsPromise = undefined;
    mindwellCache.getClients = function() {
        if (!mindwellCache._clientsPromise) {
            mindwellCache._clientsPromise = mindwellRest.clients.getList().then(function(clients) {
                mindwellCache.clients = clients;
                $rootScope.$emit('mindwell.clientsUpdated');
                return mindwellCache.clients;
            });
        }
        return mindwellCache._clientsPromise;
    };

    mindwellCache.clearClientCache = function() {
        mindwellCache._clientsPromise = undefined;
    };

    mindwellCache.customFormPromise = undefined;
    mindwellCache.getCustomForm = function() {
        if (!mindwellCache.customFormPromise) {
            mindwellCache.customFormPromise = mindwellRest.customForm.getList().then(function(customForm) {
                if (customForm.length === 1) {
                    mindwellCache.customForm = customForm[0];
                } else {
                    mindwellCache.customForm = {referrer_choices: '', reason_for_visit_choices: ''};
                }
                $rootScope.$emit('mindwell.customFormUpdated');
                return mindwellCache.customForm;
            });
        }
        return mindwellCache.customFormPromise;
    };

    mindwellCache.clearCustomFormCache = function() {
        mindwellCache.customFormPromise = undefined;
    };

    mindwellCache._userPermPromise = undefined;
    mindwellCache.getUserPerm = function() {
        if (!mindwellCache._userPermPromise) {
            mindwellCache._userPermPromise = mindwellRest.userPerm.getList().then(function(userPerm) {
                mindwellCache.userPerm = userPerm;
                $rootScope.$emit('mindwell.userPermUpdated');
                return mindwellCache.userPerm;
            });
        }
        return mindwellCache._userPermPromise;
    };

    mindwellCache.clearUserPerm = function() {
        mindwellCache._userPermPromise = undefined;
    };

    mindwellCache._logoutUrlPromise = undefined;
    mindwellCache.getLogoutUrl = function() {
        if (!mindwellCache._logoutUrlPromise) {
            mindwellCache._logoutUrlPromise = mindwellRest.logoutUrl.customGET().then(function(logoutUrl) {
                mindwellCache.logoutUrl = logoutUrl;
                $rootScope.$emit('mindwell.logoutUrlUpdated');
                return mindwellCache.logoutUrl;
            });
        }
        return mindwellCache._logoutUrlPromise;
    };

    mindwellCache.clearLogoutUrl = function() {
        mindwellCache._logoutUrlPromise = undefined;
    };

    mindwellCache.getClients();
    mindwellCache.getCustomForm();
    mindwellCache.getUserPerm();
    mindwellCache.getLogoutUrl();

    return mindwellCache;
});
