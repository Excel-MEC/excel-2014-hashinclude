$(document).ready(function() {
	$("#app").addClass("nav-min");
	$(".nav-profile").removeClass("open");

	$("#nav-container").mouseenter(function(){
		$("#app").removeClass("nav-min");
	}).mouseleave( function(){
		$("#app").addClass("nav-min");
	});
});