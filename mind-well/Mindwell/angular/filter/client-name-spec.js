describe('clientName', function() {

	beforeEach(module('mindwell'));

	it('should ...', inject(function($filter) {

        var filter = $filter('clientName');

		expect(filter('input')).toEqual('output');

	}));

});