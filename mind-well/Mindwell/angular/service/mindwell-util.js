angular.module('mindwell').factory('mindwellUtil', function($location, mindwellCache, $rootScope, mindwellRest, prompt) {

    var mindwellUtil = {};

    mindwellUtil.onEditClient = function(client) {
        $location.path('/client-detail').search({
            'contentId': client.id
        });
    };

    mindwellUtil.generateClientInvoicesByDate = function(start, end) {
        var dateFormat = 'YYYY/MM/DD';
        window.location = '/Mindwell/' + start.format(dateFormat) + '/' + end.format(dateFormat) + '/generate_client_invoices_by_date';
    };

    mindwellUtil.generateProviderInvoicesByDate = function(start, end) {
        var dateFormat = 'YYYY/MM/DD';
        window.location = '/Mindwell/' + start.format(dateFormat) + '/' + end.format(dateFormat) + '/provider_invoices';
    };

    mindwellUtil.calcBalances = function(dosList) {
        var sortedDOS = _.sortBy(dosList, 'dos_datetime');
        _.reduce(sortedDOS, function(prevDOS, dos) {
            var amt_due, amt_paid, balance;
            // calculate first DOS' balance
            if (prevDOS.balance === undefined) {
                amt_due = parseFloat(prevDOS.amt_due) || 0;
                amt_paid = parseFloat(prevDOS.amt_paid) || 0;
                prevDOS.balance = amt_due - amt_paid;
            }
            amt_due = parseFloat(dos.amt_due) || 0;
            amt_paid = parseFloat(dos.amt_paid) || 0;
            balance = parseFloat(prevDOS.balance) || 0;
            dos.balance = balance + amt_due - amt_paid;
            return dos;
        });
        return sortedDOS;
    };

    mindwellUtil.saveClient = function(client) {
        var savedClient;
        if (client.id) {
            return client.save().then(function(client) {
                savedClient = client;
                return mindwellCache.getClients();
            }).then(function() {
                var cacheId = _.findIndex(mindwellCache.clients, function(cacheClient) {
                    return savedClient.id === cacheClient.id;
                });
                mindwellCache.clients[cacheId] = savedClient;
                $rootScope.$broadcast('mw-client-updated', savedClient);
                return savedClient;
            });
        } else {
            return mindwellRest.clients.post(client).then(function(client) {
                savedClient = client;
                return mindwellCache.getClients();
            }).then(function() {
                mindwellCache.clients.push(savedClient);
                $rootScope.$broadcast('mw-client-updated', savedClient);
                return savedClient;
            });
        }
    };

    mindwellUtil.updateDOSCache = function(dos, update) {
        return mindwellCache.getClients().then(function(clients) {
            var client = _.find(clients, {
                id: dos.clientinfo
            });
            if (client && client.dosList) {
                if (update) {
                    var idx = _.findIndex(client.dosList, function(oldDos) {
                        return oldDos.id === dos.id;
                    });
                    client.dosList[idx] = dos;
                } else {
                    client.dosList.push(dos);
                }
            }
        });
    };

    mindwellUtil.deleteDOS = function(dos, client) {
        return prompt({
            title: 'Delete DOS?',
            message: 'Are you sure you want to delete this DOS from ' + dos.dos_datetime + '?'
        }).then(function() {
            return dos.remove();
        }).then(function(dos) {
            return mindwellCache.getClients();
        }).then(function(clients) {
            if (client && client.id) {
                var updatedClient = _.find(mindwellCache.clients, {
                    id: client.id
                });
                if (updatedClient.dosList) {
                    updatedClient.dosList = _.without(updatedClient.dosList, dos);
                }
                return updatedClient.dosList;
            }
        }).then(function() {
            $rootScope.$broadcast('mw-dos-deleted', dos);
            return dos;
        });
    };

    mindwellUtil.printReceipt = function(dos) {
        window.open('/Mindwell/' + dos.id + '/dos_receipt/', '_blank');
    };

    mindwellUtil.clientFields = [{
        key: 'lastname',
        title: 'Last Name'
    }, {
        key: 'firstname',
        title: 'First Name'
    }, {
        key: 'cellnumber',
        title: 'Cell'
    }, {
        key: 'cellmessage',
        title: 'Cell Message'
    }, {
        key: 'homenumber',
        title: 'Home'
    }, {
        key: 'homemessage',
        title: 'Home Message'
    }, {
        key: 'worknumber',
        title: 'Work Number'
    }, {
        key: 'emailaddress',
        title: 'Email'
    }, {
        key: 'address',
        title: 'Address 1'
    }, {
        key: 'address2',
        title: 'Address 2'
    }, {
        key: 'city',
        title: 'City'
    }, {
        key: 'state',
        title: 'State'
    }, {
        key: 'zipcode',
        title: 'Zip'
    }, {
        key: 'dob_month',
        title: 'DOB Month'
    }, {
        key: 'dob_day',
        title: 'DOB Day'
    }, {
        key: 'dob_year',
        title: 'DOB Year'
    }, {
        key: 'referrer',
        title: 'Referrer'
    }, {
        key: 'dms_code',
        title: 'ICD 10'
    }, {
        key: 'client_status',
        title: 'Client Status'
    }, {
        key: 'guardians_name',
        title: 'Guardians Name'
    }, {
        key: 'guardians_phone_number',
        title: 'Guardians Phone Number'
    }, {
        key: 'emergency_contact',
        title: 'Emergency Contact'
    }, {
        key: 'emergency_contact_phone_number',
        title: 'Emergency Contact Phone'
    }, {
        key: 'reason_for_visit',
        title: 'Reason For Visit'
    }];

    mindwellUtil.dosFields = [{
        key: 'client',
        title: 'Client',
    }, {
        key: 'dos_datetime',
        title: 'DOS Date and Time'
    }, {
        key: 'session_type',
        title: 'Session Type'
    }, {
        key: 'session_result',
        title: 'Session Result'
    }, {
        key: 'type_pay',
        title: 'Type of Payment'
    }, {
        key: 'note',
        title: 'Note'
    }, {
        key: 'amt_due',
        title: 'Amount Due'
    }, {
        key: 'amt_paid',
        title: 'Amount Paid'
    }];


    return mindwellUtil;
});
