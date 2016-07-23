;(function (angular) {
  "use strict";
  angular.module("home")
         .component("home", {

           "templateUrl": "js/home/home.html",
           "controller"  : ["$rootScope", "Session", "$http", "$scope", "$state","DTOptionsBuilder", "DTColumnBuilder","$timeout",

	function ( $rootScope, Session,$http, $scope, $state, DTOptionsBuilder, DTColumnBuilder, $timeout) {
		var self = this;
        this.user = Session.get();

        if (this.user.roles.indexOf("Agent") >= 0) {
            this.user.role = "Agent";
        }

        if (this.user.roles.indexOf("Customer") >= 0) {
            this.user.role = "Customer";
        }

        if(this.user.role == "Customer"){
            $('#fileupload').hide();
        }

	}]
        });
}(window.angular));

