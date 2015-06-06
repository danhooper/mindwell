angular.module('mindwell').factory('mwTestCommon', function() {

    var mwTestCommon = {};

    var dosHandler = function(url) {
        console.log('got dos', arguments);
        return true;
        //return url.indexOf('/Mindwell/rest/dos') === 0;
    };

    var dosResponse = function() {
        return {};
    };

    mwTestCommon.init = function() {
        inject(function($httpBackend, Restangular, mindwellRest) {
            mwTestCommon.$httpBackend = $httpBackend;
            mwTestCommon.Restangular = Restangular;
            mwTestCommon.mindwellRest = mindwellRest;
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/clientinfo').respond([]);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/clientinfo');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/dos/2').respond(dosResponse);
            mwTestCommon.$httpBackend.expectGET('/Mindwell/rest/dos/2');
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/custom_form').respond([]);
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/calendar_settings').respond([]);
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/userperm').respond([]);
            mwTestCommon.$httpBackend.when('GET', '/Mindwell/rest/logouturl').respond([]);
        });
    };


    return mwTestCommon;
});
