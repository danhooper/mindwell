angular.module('mindwell').factory('mwExport', function(
    mindwellCache, mindwellUtil, $q, mindwellRest) {

    var mwExport = {};

    var createCSV = function(entities, fields) {
        var csvContent = 'data:text/csv;charset=utf-8,';
        var values;
        var rows = _.map(entities, function(entity) {
            values = _.map(fields, function(field) {
                if (!entity[field.key]) {
                    return '';
                }
                return entity[field.key];
            });
            return values;
        });
        console.log(rows);
        var header = _.map(fields, 'title');
        return csvContent + new CSV(rows, {header: header}).encode();
    };

    mwExport.getClientCSV = function() {
        return mindwellCache.getClients().then(function() {
            window.open(encodeURI(createCSV(mindwellCache.clients, mindwellUtil.clientFields)));
        });
    };

    var fetchDOSChunk = function(chunkIdx, clientsChunked, currDOSList, deferred) {
        var promises = _.map(clientsChunked[chunkIdx], function(client) {
            return mindwellRest.dos.getList({clientinfo: client.id});
        });
        return $q.all(promises).then(function(data) {
            _.each(data, function(dosList) {
                currDOSList = currDOSList.concat(dosList);
            });
            deferred.notify(Math.round((chunkIdx * 100) / clientsChunked.length));
            if (chunkIdx < clientsChunked.length) {
                return fetchDOSChunk(chunkIdx + 1, clientsChunked, currDOSList, deferred);
            } else {
                return currDOSList;
            }
        });
    };

    mwExport.getDOSCsv = function() {
        var deferred = $q.defer();
        mindwellCache.getClients().then(function() {
            var clientsChunked = _.chunk(mindwellCache.clients, 4);
            return fetchDOSChunk(0, clientsChunked, [], deferred);
        }).then(function(dosList) {
            _.each(dosList, function(dos) {
                // TODO: Remove parseInt once issue #48 is fixed
                var client = _.find(mindwellCache.clients, {id: parseInt(dos.clientinfo, 10)});
                if (client) {
                    dos.client = client.lastname + ',' + client.firstname;
                }
            });
            deferred.resolve();
            window.open(encodeURI(createCSV(dosList, mindwellUtil.dosFields)));
        });
        return deferred.promise;
    };

    return mwExport;
});

