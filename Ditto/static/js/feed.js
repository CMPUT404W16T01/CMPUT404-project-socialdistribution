$(document).ready(function () {
    $(".dropdown-button").dropdown();
    $('select').material_select();

$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

$('#testbutton').click( function(event){
	console.log("clicked");
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


function create_post() {
    console.log("creating post...");
    //console.log($('#post-input').val());
    //console.log($('#is-markdown').prop('checked'));
    //console.log($('#visibility').val());
    console.log($('#title').val());
    console.log($('#description').val());
    console.log($('#categories').val());

var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

    $.ajax({
        url : "/feed/create_post/", // the endpoint
        type : "POST", // http method
        data : { post_body : $('#post-input').val(),
        		is_markdown : $('#is-markdown').prop('checked'), 
        		visibility : $('#visibility').val(),
                title: $('#title').val(),
                description: $('#description').val(),
                categories: $('#categories').val()
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