angular.module('mindwell').factory('mindwellCache', function(mindwellRest, $rootScope, $q, Restangular) {

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

    mindwellCache._customFormPromise = undefined;
    mindwellCache.getCustomForm = function() {
        if (!mindwellCache._customFormPromise) {
            mindwellCache._customFormPromise = mindwellRest.customForm.getList().then(function(customForm) {
                var defaultForm = {referrer_choices: '', reason_for_visit_choices: ''};
                mindwellCache.customForm = defaultForm;
                if (customForm.length === 1) {
                    mindwellCache.customForm = customForm[0];
                }
                $rootScope.$emit('mindwell.customFormUpdated');
                return mindwellCache.customForm;
            });
        }
        return mindwellCache._customFormPromise;
    };

    mindwellCache.clearCustomFormCache = function() {
        mindwellCache._customFormPromise = undefined;
    };

    mindwellCache._calSettingsPromise = undefined;
    mindwellCache.getCalSettings = function() {
        if (!mindwellCache._calSettingsPromise) {
            mindwellCache._calSettingsPromise = mindwellRest.calSettings.getList().then(function(calSettings) {
                var defaultCalSettings = {display_weekends: 'No', calendar_start_time: '6 am'};
                if (calSettings.length === 1) {
                    if (calSettings[0].display_weekends) {
                        defaultCalSettings.display_weekends = calSettings[0].display_weekends;
                    }
                    if (calSettings[0].calendar_start_time) {
                        defaultCalSettings.calendar_start_time = calSettings[0].calendar_start_time;
                    }
                }

                mindwellCache.calSettings = Restangular.restangularizeElement(null, defaultCalSettings, 'calendar_settings');
                $rootScope.$emit('mindwell.calSettingsUpdated');
                return mindwellCache.calSettings;
            });
        }
        return mindwellCache._calSettingsPromise;
    };

    mindwellCache.clearCalSettingsCache = function() {
        mindwellCache._calSettingsPromise = undefined;
    };

    mindwellCache._invoiceSettingsPromise = undefined;
    mindwellCache.getInvoiceSettings = function() {
        if (!mindwellCache._invoiceSettingsPromise) {
            mindwellCache._invoiceSettingsPromise = mindwellRest.invoiceSettings.getList().then(function(invoiceSettings) {
                if (invoiceSettings.length === 1) {
                    mindwellCache.invoiceSettings = invoiceSettings[0];
                } else {
                    mindwellCache.invoiceSettings = Restangular.restangularizeElement(null, {}, 'invoice_settings');
                }
                $rootScope.$emit('mindwell.invoiceSettingsUpdated');
                return mindwellCache.invoiceSettings;
            });
        }
        return mindwellCache._invoiceSettingsPromise;
    };

    mindwellCache.clearInvoiceSettingsCache = function() {
        mindwellCache._calSettingsPromise = undefined;
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

    mindwellCache._invoicesPromise = undefined;
    mindwellCache.getInvoices = function() {
        if (!mindwellCache._invoicesPromise) {
            mindwellCache._invoicesPromise = mindwellRest.invoice.getList().then(function(invoices) {
                mindwellCache.invoices = invoices;
                $rootScope.$emit('mindwell.invoicesUpdated');
                return mindwellCache.invoices;
            });
        }
        return mindwellCache._invoicesPromise;
    };

    mindwellCache.clearinvoiceCache = function() {
        mindwellCache._invoicesPromise = undefined;
    };

    mindwellCache.getWhoami = function() {
        if (!mindwellCache._whoamiPromise) {
            mindwellCache._whoamiPromise = mindwellRest.whoami.get().then(function(whoami) {
                mindwellCache.whoami = whoami;
                $rootScope.$emit('mindwell.whoamiUpdated');
                return mindwellCache.whoami;
            });
        }
        return mindwellCache._whoamiPromise;
    };

    mindwellCache.getUserPerm();
    mindwellCache.getLogoutUrl();
    mindwellCache.getWhoami();

    return mindwellCache;
});
