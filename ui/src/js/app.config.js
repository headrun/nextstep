;(function (angular) {
  "use strict";

  var LOGIN_STATE = "login",
      LOGIN_REDIRECT_STATE = "home";

  var routes = [

    /*
     * The config follows the following convention
     * [statename , path, template, authRequired]
     */

    ["login", "/login", "<login></login>"],
    ["home", "/", "<home></home>", true]
  ];

  angular.module("nextstep")
         .config(["$locationProvider", "$stateProvider",
                  "$httpProvider", "$urlRouterProvider",
           function ($lp, $sp, $hp, $urp) {

             $lp.hashPrefix('');

             var route;

             for (var index in routes) {

               route = routes[index];

               $sp.state(route[0], {
                 "url": route[1],
                 "template": route[2],
                 "authRequired": route[3]
               });
             }

             $urp.otherwise("/");

             $hp.defaults.xsrfCookieName = "csrftoken";
             $hp.defaults.xsrfHeaderName = "X-CSRFToken";
           }
         ]).run(["$rootScope", "$state",
                 "Auth", "AUTH_EVENTS",

          function ($rootScope, $state, Auth, AUTH_EVENTS) {

            var skipAsync = false;

            $rootScope.$on("$stateChangeStart", function (event, next) {

              if (skipAsync) {

                skipAsync = false;
                return;
              }

              if (next.authRequired) {

                event.preventDefault();

                ;(function (thisNext) {

                  Auth.status().then(function (resp) {

                    if (thisNext.name !== next.name) {

                      return;
                    }

                    if (!resp.user) {

                      $rootScope.$broadcast(AUTH_EVENTS.unAuthorized);
                      return;
                    }

                    skipAsync = true;
                    $state.go(next.name);
                  });
                }(next));
              }
            });

            $rootScope.$on(AUTH_EVENTS.loginSuccess, function () {

              $state.go(LOGIN_REDIRECT_STATE, {"location": "replace"});
            });

            function goToLogin () {

              $state.go(LOGIN_STATE, {"location": "replace"});
            }

            $rootScope.$on(AUTH_EVENTS.unAuthorized, goToLogin);
            $rootScope.$on(AUTH_EVENTS.logoutSuccess, goToLogin);
          }
         ]);
}(window.angular));
