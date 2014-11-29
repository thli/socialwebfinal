$(document).ready(function() {
    $(".collect-btn").click(function() {
        var post = $(this).closest(".post");
        var url = "/vidavid/like-post"
        var id = post.attr("post-id");
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            'type': "POST",
            'url': url,
            'data': {
                'id' : id,
                'csrfmiddlewaretoken' : csrftoken,
            }
        }).done(function(numLikes) {
            post.find(".likes").html(numLikes + " likes");
        });
    });
    
    
    $(".delete-btn").click(function() {
        var post = $(this).closest(".post");
        var url = "/vidavid/delete-post"
        var id = post.attr("post-id");
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            'type': "POST",
            'url': url,
            'data': {
                'id' : id,
                'csrfmiddlewaretoken' : csrftoken,
            }
        }).done(function() {
            post.remove();
        });
    });    

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
};