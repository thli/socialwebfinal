$(document).ready(function() {
    $(window).scroll($.throttle(function() {
        if($(window).scrollTop() + $(window).height() > $(document).height()-100) {
            var url = "/vidavid/update-index"
            var id = $(".post").last().attr("data-id");
            var csrftoken = getCookie('csrftoken');
            $.getJSON(url, {"min_id": id}, 
            function(data) {
                //append html to start of post list
                $("#post-stream").append(data);
            });
        }
    }, 1000));
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