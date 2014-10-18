angular.module('mindwell', ['ui.bootstrap','ui.utils','ngRoute','ngAnimate', 'restangular', 'ngTable', 'cgPrompt', 'ngCookies', 'cgBusy']);

angular.module('mindwell').config(function($routeProvider, RestangularProvider) {

    $routeProvider.when('/client-list',{templateUrl: 'partial/client-list/client-list.html'});
    $routeProvider.when('/client-detail',{templateUrl: 'partial/client-detail/client-detail.html'});
    /* Add New Routes Above */
    $routeProvider.otherwise({redirectTo:'/client-list'});

    RestangularProvider.setBaseUrl('/Mindwell/rest');

});

angular.module('mindwell').run(function($rootScope, mindwellCache, $cookies, $timeout) {

    $rootScope.safeApply = function(fn) {
        var phase = $rootScope.$$phase;
        if (phase === '$apply' || phase === '$digest') {
            if (fn && (typeof(fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

    $rootScope.getCalendarURL = function() {
        return 'Mindwell/' + moment().format('YYYY/MM/DD') + '/calendar/';
    };

    $rootScope.mindwellCache = mindwellCache;
    $rootScope.currentUser = $cookies.current_user;

    $rootScope.updateUser= function() {
        if ($rootScope.currentUser === '') {
            delete $cookies.current_user;
        } else {
            $cookies.current_user = $rootScope.currentUser;
        }
        $timeout(function() {
            $rootScope.getClientsPromise = mindwellCache.getClients(true);
            mindwellCache.getCustomForm(true);
        });
    };


});
