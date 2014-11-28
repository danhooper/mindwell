angular.module('mindwell').factory('mindwellRest', function(Restangular) {

    var mindwellRest = {};

    mindwellRest.clients = Restangular.all('clientinfo');

    mindwellRest.dos = Restangular.all('dos');

    mindwellRest.balance = Restangular.all('balance');

    mindwellRest.customForm = Restangular.all('custom_form');

    mindwellRest.userPerm = Restangular.all('userperm');

    mindwellRest.logoutUrl = Restangular.all('logouturl');

    return mindwellRest;
});
