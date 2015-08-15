describe('mwDosForm', function() {

    beforeEach(module('mindwell'));
    beforeEach(module('templates'));

    var scope, compile, mwTestCommon, mindwellCache;

    beforeEach(inject(function($rootScope, $compile, _mwTestCommon_, _mindwellCache_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        mindwellCache = _mindwellCache_;
        scope = $rootScope.$new();
        scope.dos = {};
        compile = $compile;
    }));

    it('should create a form', function() {

        var element = compile('<mw-dos-form ng-model="dos"></mw-dos-form>')(scope);
        scope.$digest();
        mwTestCommon.$httpBackend.flush();
        expect(element.find('form').length).toEqual(1);
    });

    it ('should clear the client when a blocked time is selected', function() {
        scope.testClient = {id: 1};
        mindwellCache.clients = [scope.testClient];
        var element = compile('<mw-dos-form mw-client="testClient" ng-model="dos"></mw-dos-form>')(scope);
        scope.$digest();
        mwTestCommon.$httpBackend.flush();
        expect(scope.$$childHead.client).toBeDefined();
        scope.$$childHead.blockedTimeChange();
        expect(scope.client).toBeUndefined();
    });
});
