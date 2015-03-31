describe('titleize', function() {

    beforeEach(module('mindwell'));

    it('should make user friendly strings', inject(function($filter) {

        var filter = $filter('titleize');

        expect(filter('input')).toEqual('Input');
        expect(filter('client info')).toEqual('Client Info');

    }));

});
