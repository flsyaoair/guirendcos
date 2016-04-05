var dashboard = angular.module('dashboard', ['ngRoute']);

dashboard.run(['$rootScope', '$location', function($rootScope, $location) {

    $rootScope.$on('$routeChangeSuccess', function(newV) {
        $rootScope.path = $location.path();
        var path = $location.path().replace('/', '');
        var num = path.indexOf('/');
        console.log(path.slice(0, num));
        $rootScope.rootpath = path.slice(0, num);
    });

}]);