angular.module('mindwell').factory('mindwellRest', function(Restangular) {

    var mindwellRest = {};

    mindwellRest.clients = Restangular.all('clientinfo');

    mindwellRest.dos = Restangular.all('dos');

    mindwellRest.invoice = Restangular.all('invoice');

    mindwellRest.calEvents = Restangular.all('calendar_feed');

    mindwellRest.balance = Restangular.all('balance');

    mindwellRest.customForm = Restangular.all('custom_form');

    mindwellRest.calSettings = Restangular.all('calendar_settings');

    mindwellRest.invoiceSettings = Restangular.all('invoice_settings');

    mindwellRest.userPerm = Restangular.all('userperm');

    mindwellRest.whoami = Restangular.one('whoami');

    mindwellRest.logoutUrl = Restangular.all('logouturl');

    return mindwellRest;
});
