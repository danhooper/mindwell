angular.module('mindwell').factory('mwExport', function(mindwellCache, mindwellUtil, $q) {

    var mwExport = {};

    var createCSV = function(entities, fields) {
        var csvContent = 'data:text/csv;charset=utf-8,';
        var values;
        var rows = _.map(entities, function(entity) {
            values = _.map(fields, function(field) {
                return entity[field.key];
            });
            return values.join(',');
        });
        var header = _.map(fields, function(field) {
            return field.title;
        }).join(',');
        rows.unshift(header);
        csvContent += rows.join('\n');
        return csvContent;
    };

    mwExport.getClientCSV = function() {
        mindwellCache.getClients().then(function() {
            window.open(encodeURI(createCSV(mindwellCache.clients, mindwellUtil.clientFields)));
        });
    };

    //var downloadDOSChunk = function(chunkIdx, clientsChunked, dosAccumulator) {
    //    var promises = _.map(clientsChunked, function(client) {
    //        return mindwellRest.dos.getList({clientinfo: client.id});
    //    });
    //    $q.all(promises).then(function(data) {
    //    });
    //};

    //mwExport.getDOSCsv = function() {
    //    mindwellCache.getClients().then(function() {
    //        var clientsChunked = _.chunk(mindwellCache.clients, 4);
    //        var chunkIdx;
    //        for( chunkIdx = 0; chunkIdx <
    //    });
    //};

    return mwExport;
});

