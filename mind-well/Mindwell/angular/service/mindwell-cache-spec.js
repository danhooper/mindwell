describe('mindwellCache', function() {

    var mwTestCommon;
    beforeEach(module('mindwell'));

    beforeEach(inject(function(_mwTestCommon_) {
        mwTestCommon = _mwTestCommon_;
        mwTestCommon.init();
    }));

    it('should cache clients', function(done) {
        inject(function(mindwellCache) {
            spyOn(mwTestCommon.mindwellRest.clients, 'getList').and.callThrough();
            mindwellCache.clearClientCache();

            mindwellCache.getClients().then(function() {
                expect(mindwellCache.clients.length).toEqual(0);
                expect(mwTestCommon.mindwellRest.clients.getList.calls.count()).toEqual(1);
                return mindwellCache.getClients();
            }).then(function() {
                expect(mindwellCache.clients.length).toEqual(0);
                expect(mwTestCommon.mindwellRest.clients.getList.calls.count()).toEqual(1);
                done();
            });
            mwTestCommon.$httpBackend.flush();
        });

    });

});
