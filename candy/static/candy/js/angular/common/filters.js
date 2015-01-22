var mod = angular.module("candy.filters", []);

mod.filter('strip', function () {
    return function (input, params) {
        var n = params.split(',');
        if (n.length == 1) {
            var start = parseInt(n[0]);
            return input.slice(parseInt(start));
        } else if (n.length == 2) {
            var start = parseInt(n[0]);
            var end = parseInt(n[1]);
            return input.slice(parseInt(start), parseInt(end));
        }
    }
});

mod.filter('fp', function() {
  return function(input, params) {
    if (input && input.indexOf("filepicker") > -1) {
      return input + "/convert?" + params;
    }
    return input;
  };
});


mod.filter('removeEmailDomain', function() {
  return function(input) {
    if (input) {
    var res = input.split("@");
    return res[0]
    }
    return input

  };
});