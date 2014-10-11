describe('ReferrerCtrl', function() {

    beforeEach(module('mindwell'));

    var scope, ctrl;

    beforeEach(inject(function($rootScope, $controller) {
        scope = $rootScope.$new();
        ctrl = $controller('ReferrerCtrl', {
            $scope: scope,
            client: {referrer: ''},
            customForm: {referrer_choices: ''},
            $modalInstance: {close: function() {}}
        });
    }));

    it('should ...', inject(function() {

        expect(1).toEqual(1);

    }));

});
