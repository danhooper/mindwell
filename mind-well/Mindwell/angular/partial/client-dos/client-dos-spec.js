describe('ClientDosCtrl', function() {

    beforeEach(module('mindwell'));
    var scope, ctrl, mwTestCommon;

    beforeEach(inject(function($rootScope, $controller, _mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        scope = $rootScope.$new();
        ctrl = $controller('ClientDosCtrl', {
            $scope: scope
        });
    }));

    it('should ...', inject(function() {
        scope.$digest();
    }));

});
