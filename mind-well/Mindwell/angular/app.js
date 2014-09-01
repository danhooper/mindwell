angular.module('mindwell', ['ui.bootstrap','ui.utils','ngRoute','ngAnimate', 'restangular', 'ngTable']);

angular.module('mindwell').config(function($routeProvider, RestangularProvider) {

    $routeProvider.when('/client-list',{templateUrl: 'partial/client-list/client-list.html'});
    /* Add New Routes Above */
    $routeProvider.otherwise({redirectTo:'/home'});

    RestangularProvider.setBaseUrl('http://havok:9000/Mindwell/rest');
    RestangularProvider.setDefaultHttpFields({
        'withCredentials': true
        });

});

angular.module('mindwell').run(function($rootScope) {

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



});
