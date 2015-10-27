describe('ClientDosCtrl', function() {

    beforeEach(module('mindwell'));
    var scope, ctrl, mwTestCommon, mindwellCache, $timeout, $q, $location;

    beforeEach(inject(function($rootScope, $controller, _mwTestCommon_, _mindwellCache_, _$location_, _$timeout_, _$q_) {
        mwTestCommon = _mwTestCommon_;
        $timeout = _$timeout_;
        $q = _$q_;
        $location = _$location_;
        $location.search('contentId', '1');
        mwTestCommon.init();
        mindwellCache = _mindwellCache_;
        mindwellCache.getClients().then(function() {
            scope.testClient = {
                id: 1
            };
            mindwellCache.clients = [scope.testClient];
        });
        scope = $rootScope.$new();
        ctrl = $controller('ClientDosCtrl', {
            $scope: scope,
            $location: $location,
            mindwellCache: mindwellCache
        });
    }));

    it('should run with no problems', inject(function() {
        scope.$digest();
        mwTestCommon.$httpBackend.flush();
    }));

    it('should fetch DOS for a client', function(done) {
        var promise = $q.defer();
        $timeout(function() {
            scope.getDOS(promise, {sorting: function() {}});
            mwTestCommon.$httpBackend.flush();
            done();
        });
        mwTestCommon.$httpBackend.flush();
        $timeout.flush();
    });

});

