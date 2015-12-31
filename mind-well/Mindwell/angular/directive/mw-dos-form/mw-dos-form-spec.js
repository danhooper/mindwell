describe('mwDosForm', function() {

    beforeEach(module('mindwell'));
    beforeEach(module('templates'));

    var scope, compile, mwTestCommon, mindwellCache, $timeout;

    beforeEach(inject(function($rootScope, $compile, _mwTestCommon_, _mindwellCache_, _$timeout_) {
        mwTestCommon = _mwTestCommon_;
        $timeout = _$timeout_;
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

    it('should clear the client when a blocked time is selected', function(done) {
        mindwellCache.getClients().then(function() {
            scope.testClient = {
                id: 1
            };
            var element = compile('<mw-dos-form mw-client="testClient" ng-model="dos"></mw-dos-form>')(scope);
            mindwellCache.clients = [scope.testClient];
        });
        $timeout(function() {
            expect(scope.$$childHead.client).toBeDefined();
            scope.$$childHead.blockedTimeChange();
            expect(scope.$$childHead.client).toBeUndefined();
            done();
        });
        mwTestCommon.$httpBackend.flush();
        $timeout.flush();
    });

    it('should update fields when cancelling sessions', function(done) {
        // TODO: Try to update with jquery
        mindwellCache.getClients().then(function() {
            scope.testClient = {
                id: 1
            };
            var element = compile('<mw-dos-form mw-client="testClient" ng-model="dos"></mw-dos-form>')(scope);
            mindwellCache.clients = [scope.testClient];
        });
        $timeout(function() {
            scope.$$childHead.newDOS.session_result = 'Cancellation - Timely';
            scope.$$childHead.sessionResultChanged();
            expect(scope.$$childHead.newDOS.amt_due).toEqual(0);
            done();
        });
        mwTestCommon.$httpBackend.flush();
        $timeout.flush();
    });
});

