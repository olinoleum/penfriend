function responsiveChat(element) {
    function showLatestMessage(element) {
        $(".messages")
            .scrollTop($(".messages")[0].scrollHeight);
    }
    showLatestMessage(element);

    /* Submit message on pressing enter */
    $(element + ' input[type="text"]').keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            $(element + ' input[type="submit"]').click();
        }
    });


    $(element + ' input[type="submit"]').click(function(event) {
        event.preventDefault();
        var message = $(element + ' input[type="text"]').val();
        if (message) {
            $(element + " div.messages").append(
                '<div class="message"><div class="myMessage"><p>' +
                message +
                "</p></div></div>"
            );
            var messagesText = grabAllMessages(element);
            fetchData("POST", "/getResponse", {"engine":$("#ai-engine option:selected").text(),
                                                "prompt":messagesText,
                                                "lang": $("#language option:selected").text()});

        }
        $(element + ' input[type="text"]').val("");
        showLatestMessage(element);
    });
}

function grabAllMessages(element) {
    var messages = Array.from($(element + " div.message div"));

    var messagesModified = messages.map(function(msg){
        var whoWrote = msg.className;
        var wroteText = msg.textContent;
        return whoWrote + ": " + wroteText
    });

    return messagesModified.join("\n") + "\nfromThem: "
}


function responsiveChatPush(element, origin, message) {
    var originClass;
    if (origin == "me") {
        originClass = "myMessage";
    } else {
        originClass = "fromThem";
    }
    $(element + " .messages").append(
        '<div class="message"><div class="' +
        originClass +
        '"><p>' +
        message +
        "</p></div></div>"
    );
}

function fetchData(method, endpoint, body){
    event.preventDefault();
    req = $.ajax({
        type: method,
        url: endpoint,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(body)});


    req.done(function(data){
            responsiveChatPush(".chat-container", "you", data);
            return false;
            });
    };


/* Activating chatbox on element */
responsiveChat(".chat-container");