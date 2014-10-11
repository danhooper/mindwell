describe('MultiSelectCtrl', function() {

    beforeEach(module('mindwell'));

    var scope, ctrl;

    beforeEach(inject(function($rootScope, $controller) {
        scope = $rootScope.$new();
        ctrl = $controller('MultiSelectCtrl', {
            $scope: scope,
            currValue: '',
            title: '',
            choices: [],
            $modalInstance: {close: function() {}}
        });
    }));

    it('should ...', inject(function() {

        expect(1).toEqual(1);

    }));

});
