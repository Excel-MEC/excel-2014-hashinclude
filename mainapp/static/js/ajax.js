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

function fb_login(response)
{


var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        
    }
});
$('#password').val('null');
data = {'name':response['name'],'id':response['id'],'username':$('#username').val(),
		'password':$('#password').val(),'csrfmiddlewaretoken':getCookie('csrftoken')};
console.log('Here');
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
function fblogout(){

      window.fbAsyncInit = function() {
        FB.init({
          appId      : '549935245152079',
          xfbml      : true,
          version    : 'v2.0'
        });
      };

      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));

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


var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);

    }
});

$.ajax({
    url: '/logout',
    type: 'get',

    success: function(data) {
        if(data=='fbuser') {
	FB.getLoginStatus(function(response) {
        if (response && response.status === 'connected') {
            FB.logout(function(response) {
                document.location.reload();
            });
        }
    });
        }
        else {
	window.location.replace("/index");}
        

    },
    failure: function(data) {
        alert('Got an error');
    }
});


}

