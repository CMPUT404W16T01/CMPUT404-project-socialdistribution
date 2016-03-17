$(document).ready(function () {
    $('#post_form').on('submit', function(event){
        event.preventDefault();
	    console.log("form submitted!");  // sanity check
	    save_settings();
});

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function save_settings() {
    console.log("creating post...");
    //console.log($('#post-input').val());
    //console.log($('#is-markdown').prop('checked'));
    //console.log($('#visibility').val());
    console.log($('#display_name').val());
    console.log($('#old_password').val());
    console.log($('#new_password').val());
    console.log($('#retype').val());
    console.log($('#github_name').val());
    console.log($('#test6').val());

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url : "/settings/save_settings/", // the endpoint
        type : "POST", // http method
        data : { 
        	display_name: 	$('#display_name').val(),
	        old_password: 	$('#old_password').val(), 
	        new_password: 	$('#new_password').val(),
	        retype: 		$('#retype').val(),
	        github_name: 	$('#github_name').val(),
	        test6: 			$('#test6').prop('checked')
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }
    });
};
});