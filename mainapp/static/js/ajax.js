	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
	$("#app").addClass("nav-min");
	$(".nav-profile").removeClass("open");

	$("#nav-container").mouseenter(function(){
		$("#app").removeClass("nav-min");
	}).mouseleave( function(){
		$("#app").addClass("nav-min");
	});
});
 $(window).load(function() {
            $("#loadingpage").css("display","none");
      });

function updatebody()
{
	console.log('body called');
	$('#mydiv').text($(obj).attr('value'));
}

function login(response)
{


var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        
    }
});

data = {'name':response['name'],'id':response['id'],'username':$('#').val(),
		'password':$('#').val(),'csrfmiddlewaretoken':getCookie('csrftoken')};

$.ajax({
    url: '/fblogin',
    type: 'post', 
	data:data,
    success: function(data) {
	if(data=='success') {
	window.location.replace("/index");}
	else {
	alert('Error');
	}

    },
    failure: function(data) { 
        alert('Got an error');
    }
}); 

}

