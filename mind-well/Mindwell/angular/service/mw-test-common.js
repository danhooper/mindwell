angular.module('mindwell').factory('mwTestCommon', function() {

    var mwTestCommon = {};

    mwTestCommon.init = function() {
        inject(function($httpBackend, Restangular, mindwellRest) {
            mwTestCommon.$httpBackend = $httpBackend;
            mwTestCommon.Restangular = Restangular;
            mwTestCommon.mindwellRest = mindwellRest;
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/clientinfo').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/clientinfo');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/custom_form').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/custom_form');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/calendar_settings').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/calendar_settings');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/userperm').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/userperm');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/logouturl').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/logouturl');
        });
    };


    return mwTestCommon;
});
