describe('mindwellUtil', function() {

    beforeEach(module('mindwell'));

    it('should calculate balances', inject(function(mindwellUtil) {


        var sampleDOSList = [{
            "session_type": "",
            "amt_paid": "220",
            "meta_version": "3",
            "dos_repeat_end_date": null,
            "amt_due": "110",
            "dos_duration": "45",
            "note": "",
            "clientinfo": 5066549580791808,
            "userinfo": "test@example.com",
            "user_id": "185804764220139124118",
            "session_result": "Attended",
            "dos_endtime": "11:00:00",
            "type_pay": "check",
            "dos_repeat": "No",
            "id": 4644337115725824,
            "dsm_code": "",
            "dos_datetime": "2015-08-15T11:00:00"
        }, {
            "session_type": "",
            "amt_paid": "110",
            "meta_version": "3",
            "dos_repeat_end_date": null,
            "amt_due": "110",
            "dos_duration": "45",
            "note": "",
            "clientinfo": 5066549580791808,
            "userinfo": "test@example.com",
            "user_id": "185804764220139124118",
            "session_result": "Scheduled",
            "dos_endtime": "12:00:00",
            "type_pay": "",
            "dos_repeat": "No",
            "id": 5207287069147136,
            "dsm_code": "",
            "dos_datetime": "2015-08-15T12:00:00"
        }, {
            "session_type": "",
            "amt_paid": "",
            "meta_version": "3",
            "dos_repeat_end_date": null,
            "amt_due": "0",
            "dos_duration": "45",
            "note": "",
            "clientinfo": 5066549580791808,
            "userinfo": "test@example.com",
            "user_id": "185804764220139124118",
            "session_result": "Cancellation - Timely",
            "dos_endtime": "09:00:00",
            "type_pay": "",
            "dos_repeat": "No",
            "id": 5348024557502464,
            "dsm_code": "",
            "dos_datetime": "2015-08-15T09:00:00"
        }, {
            "session_type": "",
            "amt_paid": "110",
            "meta_version": "3",
            "dos_repeat_end_date": null,
            "amt_due": "110",
            "dos_duration": "45",
            "note": "",
            "clientinfo": 5066549580791808,
            "userinfo": "test@example.com",
            "user_id": "185804764220139124118",
            "session_result": "Attended",
            "dos_endtime": "08:45:00",
            "type_pay": "check",
            "dos_repeat": "No",
            "id": 6192449487634432,
            "dsm_code": "",
            "dos_datetime": "2015-08-15T08:00:00"
        }, {
            "session_type": "",
            "amt_paid": "0",
            "meta_version": "3",
            "dos_repeat_end_date": null,
            "amt_due": "110",
            "dos_duration": "45",
            "note": "",
            "clientinfo": 5066549580791808,
            "userinfo": "test@example.com",
            "user_id": "185804764220139124118",
            "session_result": "Attended",
            "dos_endtime": "10:00:00",
            "type_pay": "",
            "dos_repeat": "No",
            "id": 6473924464345088,
            "dsm_code": "",
            "dos_datetime": "2015-08-15T10:00:00"
        }];

        sampleDOSList = mindwellUtil.calcBalances(sampleDOSList);
        expect(sampleDOSList[0].balance).toEqual(0);
        expect(sampleDOSList[1].balance).toEqual(0);
        expect(sampleDOSList[2].balance).toEqual(110);
        expect(sampleDOSList[3].balance).toEqual(0);
        expect(sampleDOSList[4].balance).toEqual(0);
    }));

});
