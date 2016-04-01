$(document).ready(function () {
    $(".dropdown-button").dropdown();
    $('select').material_select();
    $('.modal-trigger').leanModal();


    $('#create-post').on('submit', function(event){
        event.preventDefault();

    var csrftoken = getCookie('csrftoken');
    //From the official django documentation: https://docs.djangoproject.com/en/1.9/ref/csrf/





    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var form_data = new FormData($('#create-post').get(0));
    form_data.append("post-input",$('#post-input').val());
    form_data.append("is-markdown-post",$('#is-markdown-post').prop('checked'));
    form_data.append("visibility",$('#visibility').val());
    form_data.append("title",$('#title').val());
    form_data.append("description",$('#description').val());
    form_data.append("categories",$('#categories').val());



    
    console.log(form_data);

    $.ajax({
    url: "/feed/create_post/",
    type: "POST",
    data: form_data,
    cache: false,
    processData: false,
    contentType: false,

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


function create_post() {

};


});