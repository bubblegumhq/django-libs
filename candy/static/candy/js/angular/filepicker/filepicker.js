'use strict';

var mod = angular.module("candy.filepicker", []);

mod.service('FilePicker', ['$q',
		function ($q) {
			var FilePickerService = {};

			FilePickerService.pickSingle = function () {
				var deferred = $q.defer();
				filepicker.pickAndStore(
					{
						mimetype: "image/*",
						folders: false
					},
					{
						location: "S3"
					},
					function (Blobs) {
						//NOTE: We only support loading one file at a time!
						if (Blobs.length > 0) {
							var blob = Blobs[0];
							//NOTE: Grab with and height from filepicker
							filepicker.stat(
								blob,
								{
									width: true,
									height: true
								},
								function (metadata) {
									blob.width = metadata.width;
									blob.height = metadata.height;
									deferred.resolve(blob);
								}
							)
						}
					}
				);
				return deferred.promise();
			};

			FilePickerService.pick = function (callback) {
				filepicker.pickAndStore(
					{
						mimetype: "image/*",
						folders: false
					},
					{
						location: "S3"
					},
					function (Blobs) {
						//NOTE: We only support loading one file at a time!
						if (Blobs.length > 0) {
							var blob = Blobs[0];
							//NOTE: Grab with and height from filepicker
							filepicker.stat(
								blob,
								{
									width: true,
									height: true
								},
								function (metadata) {
									blob.width = metadata.width;
									blob.height = metadata.height;
									callback(blob);
								}
							)
						}
					}
				);
			};

			FilePickerService.pickCSV = function () {
				var d = $q.defer();
				filepicker.pickAndStore(
					{
						mimetype: "text/csv",
						folders: false
					},
					{
						location: "S3"
					},
					function (Blobs) {
						if (Blobs.length > 0) {
							d.resolve(Blobs[0]);
						}
					}
				);
				return d.promise;
			};

			return FilePickerService;
		}]
);
