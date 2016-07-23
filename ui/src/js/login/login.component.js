;(function (angular) {
  "use strict";

  angular.module("login")
         .component("login", {

           "templateUrl": "js/login/login.html",
           "controller"  : ["$rootScope", "Auth", "AUTH_EVENTS",

             function ($rootScope, Auth, AUTH_EVENTS) {

              this.credentials = {

                "username": "",
                "password": ""
              };

              this.onSubmit = function (credentials) {

                Auth.login(credentials).then(function () {

                  $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
                });
              };
            }]
        });

}(window.angular));
