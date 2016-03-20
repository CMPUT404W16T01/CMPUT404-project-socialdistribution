$(document).ready(function () {
    $('select').material_select();
    $('.modal-trigger').leanModal();


    console.log("AHHHHHHHHHHh")
    $('form').bind('submit', function(){
        console.log("Beep")
        send_friend_request();


    });

    // $('#add_friend_button').click(function() {
    //     send_friend_request();
    // });
    //From the official django documentation: https://docs.djangoproject.com/en/1.9/ref/csrf/
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
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function send_friend_request() {
    console.log("aaggggggg")
    console.log($('#sender_id').val())
    var csrftoken = getCookie('csrftoken');
    //From the official django documentation: https://docs.djangoproject.com/en/1.9/ref/csrf/
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });



    $.ajax({
        url : "/api/friendrequest/", 
        type : "POST", 
        data : { 
            query : "friendrequest",
            //is_markdown : $('#is-markdown-post').prop('checked'), 
            author : JSON.stringify({
                id: $('#sender_id').val(),
                host: $('#sender_host').val(),
                displayName: $('#sender_display_name').val()
            }),
            friend : JSON.stringify({
                id: $('#friend_id').val(),
                host: $('#friend_host').val(),
                displayName: $('#friend_display_name').val(),
                url: $('#friend_url').val()
            })
        },*/
        
        success : function(json) {  
            // var active = $("u1.tabs").tabs('option', 'active');
            // $('ul.tabs').tabs('select_tab', active);
            location.reload();
        },
        
        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }

    });
}


function create_post() {

    var csrftoken = getCookie('csrftoken');
    //From the official django documentation: https://docs.djangoproject.com/en/1.9/ref/csrf/
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
            // var active = $("u1.tabs").tabs('option', 'active');
            // $('ul.tabs').tabs('select_tab', active);
            location.reload();
        },
        
        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }

    });
};


});