angular.module('mindwell').controller('SettingsCtrl', function($scope, mindwellCache, mindwellRest, Restangular) {

    mindwellCache.getInvoiceSettings().then(function() {
        $scope.invoice = Restangular.copy(mindwellCache.invoiceSettings);
    });

    $scope.saveInvoiceSettings = function() {
        $scope.invoice.save().then(function(invoice) {
            mindwellCache.invoiceSettings = invoice;
            $scope.invoice = Restangular.copy(mindwellCache.invoiceSettings);
        });
    };

    mindwellCache.getCalSettings().then(function() {
        $scope.calendar = Restangular.copy(mindwellCache.calSettings);
    });

    $scope.saveCalendarSettings = function() {
        $scope.calendar.save().then(function(calendar) {
            mindwellCache.calSettings = calendar;
            $scope.calendar = Restangular.copy(mindwellCache.calSettings);
        });
    };

    $scope.displayWeekendChoices = ['No', 'Yes'];
    var nums = _.range(0, 12);
    nums[0] = 12;
    var ams = _.map(nums, function(num) {
        return num + ' am';
    });
    var pms = _.map(nums, function(num) {
        return num + ' pm';
    });
    $scope.calendarStartTimeChoices = ams.concat(pms);

    mindwellCache.getUserPerm().then(function() {
        $scope.userPermissions = mindwellCache.userPerm;
    });
    $scope.permissionLevels = ['Read and Write'];
    $scope.newPermission = {
        permissionlevel: $scope.permissionLevels[0]
    };
    $scope.saveNewPermissionRequest = function() {
        mindwellRest.userPerm.post($scope.newPermission).then(function(req) {
            $scope.userPermissions.push(req);
            mindwellCache.userPerm = $scope.userPermissions;
        });
    };

    $scope.deletePerm = function(perm) {
        perm.remove().then(function() {
            $scope.userPermissions = _.remove($scope.userPermissions, {id: perm.id});
        });
    };

    $scope.permissionResponse = ['User Approval',
        'Not Yet Approved'
    ];
    $scope.permissionRequests = [];
    $scope.savePermissionResponse = function() {};

    mindwellCache.getCustomForm().then(function() {
        $scope.clientForm = Restangular.copy(mindwellCache.customForm);
    });
    $scope.saveClientFormSettings = function() {
        $scope.clientForm.save().then(function(clientForm) {
            mindwellCache.customForm = clientForm[0];
        });
    };
});
