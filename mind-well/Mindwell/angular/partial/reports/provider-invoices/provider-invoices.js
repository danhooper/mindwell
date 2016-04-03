angular.module('mindwell').controller('ProviderInvoicesCtrl', function(
    $scope, mindwellRest, ngTableParams, mindwellCache, mindwellUtil, $rootScope, $location) {


    $scope.startOpened = false;
    $scope.endOpened = false;

    $scope.dosList = [];
    $scope.generate = function() {
        var params = {
            start: moment($scope.genForm.start).format('YYYY-MM-DD'),
            end: moment($scope.genForm.end).format('YYYY-MM-DD'),
        };
        $rootScope.busy = mindwellRest.dos.getList(params).then(function(dosList) {
            $scope.dosList = dosList;
            var dosByCat = _.groupBy($scope.dosList, 'type_pay');
            $scope.dosSummary = {};
            $scope.total = 0;
            _.each(Object.keys(dosByCat), function(cat) {
                var sum = 0;
                $scope.dosSummary[cat] = _.reduce(dosByCat[cat], function(prevValue, dos) {
                    return prevValue + (parseFloat(dos.amt_paid) || 0);
                }, sum);
                $scope.total += $scope.dosSummary[cat];
            });
        });
    };
    $scope.genForm = {};
    var search = $location.search();
    if (search.start && search.end) {
        $scope.genForm.start = new Date(search.start);
        $scope.genForm.end = new Date(search.end);
        $scope.generate();
    } else {
        $scope.genForm = {
            start: new Date(),
            end: new Date()
        };
    }

    $scope.startOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.startOpened = true;
    };
    $scope.endOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.endOpened = true;
    };
});
