dashboard.config(['$routeProvider',function ($routeProvider) {
    $routeProvider
    .when('/iso/list', {
        templateUrl: '/static/views/iso/list.html',
        controller: 'isoList'
    })
    .when('/iso/make', {
        templateUrl: '/static/views/iso/make.html',
        controller: 'isoMake'
    })
    .when('/app/create', {
        templateUrl: '/static/views/app/create.html',
        controller: 'appCreate'
    })
    .when('/app/status', {
        templateUrl: '/static/views/app/status.html',
        controller: 'appStatus'
    })
    .otherwise({
        redirectTo: '/iso/list'
    });
}]);