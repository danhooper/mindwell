describe('ClientListCtrl', function() {

    beforeEach(module('mindwell'));

    var scope, ctrl, mwTestCommon;

    beforeEach(inject(function($rootScope, $controller, _mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        scope = $rootScope.$new();
        ctrl = $controller('ClientListCtrl', {
            $scope: scope
        });
    }));

    it('should ...', inject(function() {
        scope.$apply();
        scope.tableParams.settings().$scope = scope;
        mwTestCommon.$httpBackend.flush();
    }));

    it('build a list letters for clients lastnames', inject(function() {
        scope.$apply();
        scope.tableParams.settings().$scope = scope;
        mwTestCommon.$httpBackend.flush();
        // no client data so no links should be set
        _.each(scope.clientLetters, function(letterObj) {
            expect(letterObj.link).toBeUndefined();
        });
    }));

});
