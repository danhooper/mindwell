describe('MwClientModalCtrl', function() {

    beforeEach(module('mindwell'));

    var scope, ctrl;

    beforeEach(inject(function($rootScope, $controller) {
        scope = $rootScope.$new();
        ctrl = $controller('MwClientModalCtrl', {
            $scope: scope,
            $modalInstance: {close: function() {}}
        });
    }));

    it('should ...', inject(function() {

        expect(1).toEqual(1);

    }));

});
