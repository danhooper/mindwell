describe('mwDosForm', function() {

    beforeEach(module('mindwell'));
    beforeEach(module('templates'));

    var scope, compile, mwTestCommon;

    beforeEach(inject(function($rootScope, $compile, _mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        scope = $rootScope.$new();
        scope.dos = {};
        compile = $compile;
    }));

    it('should create a form', function() {

            var element = compile('<mw-dos-form ng-model="dos"></mw-dos-form>')(scope);
            scope.$digest();
            expect(element.find('form').length).toEqual(1);
    });
});
