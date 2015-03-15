var app = angular.module("candy.directives.contenteditable", []);

app.directive("contenteditable", function() {
  return {
    require: "ngModel",
    link: function(scope, element, attrs, ngModel) {

      function read() {
	      html = element.html().replace(/<div>/g, '').replace(/<br>/g, '').replace(/<\/div>/g, '');
        ngModel.$setViewValue(html);
      }

      ngModel.$render = function() {

        element.html(ngModel.$viewValue || "");
      };

      element.bind("blur keyup change", function() {
        scope.$apply(read);
      });
    }
  };
});