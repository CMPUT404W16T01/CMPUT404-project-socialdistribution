$(document).ready(function () {
    $('select').material_select();
    $('.modal-trigger').leanModal();


    $('#add-friend-form').on('submit', function(event){
        event.preventDefault();
        send_friend_request();
        this.reset();
    });

    $('#unfriend-form').on('submit', function(event){
        event.preventDefault();
        unfriend();
        this.reset();
    });


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
        },
        
        success : function(json) {  
            // var active = $("u1.tabs").tabs('option', 'active');
            // $('ul.tabs').tabs('select_tab', active);
            //location.reload();
        },
        
        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }

    });
}

function unfriend() {
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
        url : "/api/unfriend/", 
        type : "POST", 
        data : { 
            query : "unfriend",
            author: $('#sender_id').val(),
            unfriending: $('#friend_id').val()
        },
        
        success : function(json) {  
            // var active = $("u1.tabs").tabs('option', 'active');
            // $('ul.tabs').tabs('select_tab', active);
            //location.reload();
            console.log("AJAX L");

        },
        
        error : function(xhr,errmsg,err) {
            console.log("AJAX ERROR");
            console.log(errmsg);
        }

    });
}





});