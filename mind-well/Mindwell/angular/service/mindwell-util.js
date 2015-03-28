angular.module('mindwell').factory('mindwellUtil', function($location, mindwellCache, $rootScope, mindwellRest) {

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
        _.reduceRight(dosList, function(prevDOS, dos) {
            var amt_due, amt_paid, balance;
            // calculate first DOS' balance
            if (!prevDOS.balance) {
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


    return mindwellUtil;
});
