angular.module('mindwell', ['ui.bootstrap','ui.utils','ngRoute','ngAnimate', 'restangular', 'ngTable', 'cgPrompt', 'ipCookie', 'cgBusy', 'ui.calendar']);

angular.module('mindwell').config(function($routeProvider, RestangularProvider) {

    $routeProvider.when('/client-list',{templateUrl: 'partial/client-list/client-list.html'});
    $routeProvider.when('/client-detail',{templateUrl: 'partial/client-detail/client-detail.html'});
    $routeProvider.when('/client-dos',{templateUrl: 'partial/client-dos/client-dos.html'});
    $routeProvider.when('/calendar',{templateUrl: 'partial/calendar/calendar.html'});
    /* Add New Routes Above */
    $routeProvider.otherwise({redirectTo:'/client-list'});

    RestangularProvider.setBaseUrl('/Mindwell/rest');

});

angular.module('mindwell').run(function($rootScope, mindwellCache, $timeout, mindwellUtil, ipCookie) {
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

    $rootScope.calendarMenuClicked = function() {
        $rootScope.$broadcast('mw.calendarMenuClicked');
    };

    $rootScope.getCalendarURL = function() {
        return '/angular/index.html#/calendar';
        //return '/Mindwell/' + moment().format('YYYY/MM/DD') + '/calendar/';
    };

    $rootScope.mindwellCache = mindwellCache;
    $rootScope.mindwellUtil = mindwellUtil;
    $rootScope.currentUser = ipCookie('current_user');

    $rootScope.updateUser= function() {
        if ($rootScope.currentUser === '') {
            ipCookie.remove('current_user', {path: '/'});
        } else {
            ipCookie('current_user', $rootScope.currentUser, {path: '/'});
        }
        $timeout(function() {
            mindwellCache.clearClientCache();
            $rootScope.getClientsPromise = mindwellCache.getClients();
            mindwellCache.clearCustomFormCache();
            mindwellCache.getCustomForm();
            $rootScope.$broadcast('mw-change-user');
        });
    };


});
