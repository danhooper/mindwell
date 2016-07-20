describe('mwClientForm', function() {
    beforeEach(module('mindwell'));
    beforeEach(module('templates'));

    var scope, compile, mwTestCommon;

    beforeEach(inject(function($rootScope, $compile, _mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        scope = $rootScope.$new();
        scope.client = {};
        compile = $compile;
    }));

    it('should create a form', function() {

        var element = compile('<mw-client-form ng-model="client"></mw-client-form>')(scope);
        scope.$digest();
        expect(element.find('form').length).toEqual(1);

    });
});
