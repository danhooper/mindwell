angular.module('mindwell', ['ui.bootstrap', 'ui.utils', 'ngRoute', 'ngAnimate', 'restangular', 'ngTable', 'cgPrompt', 'ipCookie', 'cgBusy', 'ui.calendar']);

angular.module('mindwell').config(function($routeProvider, RestangularProvider) {

    $routeProvider.when('/client-list', {
        templateUrl: 'partial/client-list/client-list.html'
    });
    $routeProvider.when('/client-detail', {
        templateUrl: 'partial/client-detail/client-detail.html'
    });
    $routeProvider.when('/client-dos', {
        templateUrl: 'partial/client-dos/client-dos.html'
    });
    $routeProvider.when('/calendar', {
        templateUrl: 'partial/calendar/calendar.html'
    });
    $routeProvider.when('/settings', {
        templateUrl: 'partial/settings/settings.html'
    });
    $routeProvider.when('/reports', {
        templateUrl: 'partial/reports/reports.html'
    });
    $routeProvider.when('/reports/invoices', {
        templateUrl: 'partial/reports/invoices/invoices.html'
    });
    $routeProvider.when('/reports/provider-invoices', {
        templateUrl: 'partial/reports/provider-invoices/provider-invoices.html'
    });
    $routeProvider.when('/reports/provider-stats', {
        templateUrl: 'partial/reports/provider-stats/provider-statistics.html'
    });
    /* Add New Routes Above */
    $routeProvider.otherwise({
        redirectTo: '/client-list'
    });

    RestangularProvider.setBaseUrl('/Mindwell/rest');

    RestangularProvider.setRequestInterceptor(function(elem, operation) {
        if (operation === "remove") {
            return undefined;
        }
        return elem;
    });

});

angular.module('mindwell').run(function($rootScope, mindwellCache, $timeout, mindwellUtil, ipCookie, $location) {
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

    $rootScope.updateUser = function() {
        if ($rootScope.currentUser === '') {
            ipCookie.remove('current_user', {
                path: '/'
            });
        } else {
            ipCookie('current_user', $rootScope.currentUser, {
                path: '/'
            });
        }
        $timeout(function() {
            mindwellCache.clearClientCache();
            $rootScope.getClientsPromise = mindwellCache.getClients();
            mindwellCache.clearCustomFormCache();
            mindwellCache.getCustomForm();
            $rootScope.$broadcast('mw-change-user');
        });
    };

    $rootScope.sections = {
        settings: [{
            name: 'Invoice Settings',
            template: 'partial/settings/templates/settings-invoice.html'
        }, {
            name: 'Calendar Settings',
            template: 'partial/settings/templates/settings-calendar.html'
        }, {
            name: 'Permission Settings',
            template: 'partial/settings/templates/settings-permission.html'
        }, {
            name: 'Client Form Settings',
            template: 'partial/settings/templates/settings-client-form.html'
        }],
        reports: [{
            name: 'Customer Invoices',
            template: 'partial/reports/invoices/invoices.html'
        }, {
            name: 'Provider Invoices',
            template: 'partial/reports/provider-invoices/provider-invoices.html'
        }, {
            name: 'Provider Statistics',
            template: 'partial/reports/provider-stats/provider-statistics.html'
        }]
    };
    $rootScope.selectSection = function(path, section) {
        $location.path(path);
        $location.search('section', section.name);
        $rootScope.activeSection = section;
    };
    var activeSection;
    if ($location.path() === '/settings') {
        activeSection = _.find($rootScope.sections.settings, {
            name: $location.search()['section']
        });
        $rootScope.selectSection('settings', activeSection ? activeSection : $rootScope.sections.settings[0]);
    }
    if ($location.path() === '/reports') {
        activeSection = _.find($rootScope.sections.reports, {
            name: $location.search()['section']
        });
        $rootScope.selectSection('reports', activeSection ? activeSection : $rootScope.sections.reports[0]);
    }
    $rootScope.$location = $location;

});
