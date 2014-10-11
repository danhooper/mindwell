angular.module('mindwell').factory('mindwellRest', function(Restangular) {

    var mindwellRest = {};

    mindwellRest.clients = Restangular.all('clientinfo');

    mindwellRest.balance = Restangular.all('balance');

    mindwellRest.customForm = Restangular.all('custom_form');

    return mindwellRest;
});
