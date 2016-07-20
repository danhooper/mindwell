angular.module('mindwell').filter('clientName', function() {
    return function(client, arg) {
        if (!client) {
            return '';
        }
        return client.lastname + ', ' + client.firstname;
    };
});
