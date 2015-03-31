describe('mwInvoicesTable', function() {

    beforeEach(module('mindwell'));
    beforeEach(module('templates'));

    var scope, compile, mwTestCommon;
    beforeEach(inject(function($rootScope, $compile, _mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        scope = $rootScope.$new();
        scope.invoices = [];
        compile = $compile;
    }));

    it('should create a table', function() {

        var element = compile('<mw-invoices-table ng-model="invoices"></mw-invoices-table>')(scope);
        scope.$digest();
        expect(element.find('table').length).toEqual(1);


    });
});
