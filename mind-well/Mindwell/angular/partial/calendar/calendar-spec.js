describe('CalendarCtrl', function() {

    beforeEach(module('mindwell'));

    var scope, ctrl, mwTestCommon, $compile, $timeout, mindwellCache;

    beforeEach(inject(function($rootScope, $controller, _$compile_, _$timeout_, _mwTestCommon_, _mindwellCache_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
        $compile = _$compile_;
        $timeout = _$timeout_;
        scope = $rootScope.$new();
        ctrl = $controller('CalendarCtrl', {
            $scope: scope,
            mindwellRest: mwTestCommon.mindwellRest
        });
    }));

    it('should run with no problems', inject(function() {
        scope.$digest();
        mwTestCommon.$httpBackend.flush();
    }));

    it('should render event titles and notes', inject(function() {
        var element = $compile('<span><span class="fc-title"></span></span>')(scope);
        scope.calConfig.eventRender({
            title: 'title',
            note: 'note'
        }, element);
        expect(element.html()).toContain('title<br>note');
    }));

    it('should insert a space for empty notes', inject(function() {
        var element = $compile('<span><span class="fc-title"></span></span>')(scope);
        scope.calConfig.eventRender({
            title: 'title'
        }, element);
        expect(element.html()).toContain('title<br>&nbsp;');
    }));

    it('should handling missing titles', inject(function() {
        var element = $compile('<span><span class="fc-title"></span></span>')(scope);
        scope.calConfig.eventRender({
            note: 'note'
        }, element);
        expect(element.html()).toContain('note');
    }));

    it('should put a DOS on scope when an event is clicked', inject(function($q, $httpBackend) {
        expect(Object.keys(scope.newDOS).length).toEqual(0);
        scope.eventClick({
            clientinfo: 1,
            id: 2,
            recurrId: -1
        });
        mwTestCommon.$httpBackend.flush();
        expect(Object.keys(scope.newDOS).length).toBeGreaterThan(0);
    }));

});
