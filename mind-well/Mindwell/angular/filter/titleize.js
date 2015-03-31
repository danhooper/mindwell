angular.module('mindwell').filter('titleize', function() {
    return function(input) {
        return s.titleize(input);
    };
});
