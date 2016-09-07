var socket = null;
var isopen = false;
var clientID = '';
window.onload = function() {

    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.binaryType = "arraybuffer";
    socket.onopen = function() {
        console.log("Connected!");
        isopen = true;
    }
    socket.onmessage = function(e) {
        console.log("Message received: " + e.data);
        $('#last').text('/result/?tag=' + $('#tag').val());
        if (clientID == '')
            clientID = e.data;
    }
    socket.onclose = function(e) {
        console.log("Connection closed.");
        socket = null;
        isopen = false;
    }

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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('#search').click(function(e){
        e.preventDefault();

        send_message(clientID);

        url=$('.form form').attr('action');
        $.ajax({
            url: url,
            type: "POST",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType:"html",
            data: ({tag: $('#tag').val()}),
            success: function(data) {
                $('#list_links').html(data);
            }
        });
    });
};

function send_message(id) {
    if (isopen) {
        socket.send(id);
        console.log("Message is sent.");
    } else {
        console.log("Connection not opened.")
    }
};
