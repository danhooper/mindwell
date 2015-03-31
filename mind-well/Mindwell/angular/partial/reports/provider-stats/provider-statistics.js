angular.module('mindwell').controller('ProviderStatisticsCtrl',function($scope, $rootScope, mindwellRest, ngTableParams){

    $scope.year = undefined;
    $scope.DOSStats = [];

    $scope.years = [
        {text: 2010, value: 2010},
        {text: 2011, value: 2011},
        {text: 2012, value: 2012},
        {text: 2013, value: 2013},
        {text: 2014, value: 2014},
        {text: 2015, value: 2015},
        {text: 2016, value: 2016},
        {text: 2017, value: 2017},
        {text: 2018, value: 2018},
        {text: 2019, value: 2019},
        {text: 2020, value: 2020},
        {text: 2021, value: 2021},
        {text: 2022, value: 2022},
        {text: 2023, value: 2023},
        {text: 2024, value: 2024},
        {text: 2025, value: 2025}
    ];

    var calcDOStats = function() {
        var stats = _.map(_.range(1, 13), function(month) {
            return {month: month, dos_count: 0, dos_value: 0};
        });
        var month;
        _.each($scope.dosList, function(dos) {
            month = moment(dos.dos_datetime).month();
            console.log(dos.clientinfo);
            if (!dos.clientinfo) {
                return;
            }
            console.log(month);
            stats[month].dos_value += (parseFloat(dos.amt_paid) || 0);
            stats[month].dos_count += 1;
        });
        $scope.DOSStats = stats;
    };

    $scope.onYearSelect = function() {
        var params = {
            start: moment($scope.year + '-' + '01-01').format('YYYY-MM-DD'),
            end: moment($scope.year + '-' + '12-31').format('YYYY-MM-DD'),
        };
        $rootScope.busy = mindwellRest.dos.getList(params).then(function(dosList) {
            $scope.dosList = dosList;
            calcDOStats();
            $scope.tableParams.reload();
        });
    };

    $scope.dosStatsCols = [{
        title: 'Month',
        field: 'month',
        visible: true,
    }, {
        title: 'DOS Count',
        field: 'dos_count',
        visible: true,
    }, {
        title: 'DOS Value',
        field: 'dos_value',
        visible: true
    }];
    $scope.tableParams = new ngTableParams({ //jshint ignore:line
        page: 1, // show first page
        count: 1000, // count per page
        sorting: {
            month: 'asc' // initial sorting
        },
        filter: $scope.filters,
    }, {
        total: 1,
        counts: [],
        getData: function($defer, params) {
            $defer.resolve($scope.DOSStats);
        }
    });

});
