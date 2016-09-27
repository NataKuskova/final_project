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
        if(e.data == 'ok')
            $('#last').text('/result/?tag=' + $('#id_tag').val());
        else if(e.data == 'error')
            $('#last').text('Error');
//        else if(e.data == 'google' || e.data == 'yandex' || e.data == 'instagram')
//            $('#last').text('' + $('#id_tag').val());
        if (clientID == '')
            clientID = e.data;

    }
    socket.onclose = function(e) {
        console.log("Connection closed.");
        socket = null;
        isopen = false;
    }


    $('#search').click(function(e){
        e.preventDefault();

        send_message(clientID, $('#id_tag').val());
        url=$('.form form').attr('action');
        $.ajax({
            url: url,
            type: "POST",
            dataType:"html",
            data: $('#search_form').serialize(),
            success: function(data) {
//                alert(data);
                $('#list_links').html(data);
            }
        });
    });
};

function send_message(id, tag) {
    if (isopen) {
        socket.send(JSON.stringify({'id': id, 'tag': tag}));
        console.log("Message is sent.");
    }
    else {
        console.log("Connection not opened.")
    }
};
