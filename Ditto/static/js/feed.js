$(document).ready(function () {
    $(".dropdown-button").dropdown();
    $('select').material_select();
    $('.modal-trigger').leanModal();

    $('#create-post').on('submit', function(event){
        event.preventDefault();
        create_post();
        this.reset();
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
   // console.log("creating post...");
  //  console.log($('#title').val());
   // console.log($('#description').val());
  //  console.log($('#categories').val());
   // console.log($('#is-markdown-post').prop('checked'));

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url : "/feed/create_post/", 
        type : "POST", 
        data : { post_body : $('#post-input').val(),
        is_markdown : $('#is-markdown-post').prop('checked'), 
        visibility : $('#visibility').val(),
        title: $('#title').val(),
        description: $('#description').val(),
        categories: $('#categories').val()
        }, 

        success : function(json) {
            console.log("Success"); 
        },

        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }
    });
};


});