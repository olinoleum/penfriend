function responsiveChat(element) {
    function showLatestMessage(element) {
        $(element)
            .scrollTop($(element)[0].scrollHeight);
    }
    showLatestMessage(element);

    /* Submit message on pressing enter */
    $('#user-input').keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            $('#button-addon2').click();
        }
    });

    /* Send message */
    $('#button-addon2').click(function(event) {

        event.preventDefault();
        var message = $('#user-input').val();

        if (message) {
            var user_msg_data = {"msgText": message,
            "lang": $("#language-menu").prop("checked")
            }

            fetchData("POST", "/sendMsg", user_msg_data, afterSendMsg);

        }
        $('#user-input').val("");
        showLatestMessage(element);
    });

    /* Get corrected message on click */
    $(".my-message").on('click', function(event){
        event.preventDefault();
        var msgId = $(this).attr("data-bs-msgid");
        var msgText = $(this).text();
        fetchData("POST", "/getCorrection", {"msgId": msgId, "orgMsg": msgText}, afterCorrection);
    });

    /* Get translated message on click */
    $(".ai-message").on('click', function(event){
        event.preventDefault();
        var msgId = $(this).attr("data-bs-msgid");
        var msgText = $(this).text();
        fetchData("POST", "/getTranslation", {"msgId": msgId, "orgMsg": msgText}, afterTranslate);
    });
}

function responsiveChatPush(element, origin, message, msgId) {
    var originClass;
    var modalId;
    if (origin == "me") {
        originClass = "my-message message";
        modalId = "#my-msg-modal";
    } else {
        originClass = "ai-message message";
        modalId = "#ai-msg-modal"
    }
    $(element).append(
        '<div class="' + originClass + '" data-bs-toggle="modal" data-bs-target="'+modalId+'" data-bs-msgid="'+msgId+'">' + message + "</div>"
    );
}

function fetchData(method, endpoint, body, func){
    event.preventDefault();
    req = $.ajax({
        type: method,
        url: endpoint,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(body)});


    req.done(function(data){
        func(data);
    });

    };

function afterResponse(data) {
    responsiveChatPush(".chat-space", "you", data.msgText, data.msgId);
        $(".ai-message").on('click', function(event){
        event.preventDefault();
        var msgId = $(this).attr("data-bs-msgid");
        var msgText = $(this).text();
        fetchData("POST", "/getTranslation", {"msgId": msgId, "orgMsg": msgText}, afterTranslate);
    });
    return false;
};

function afterSendMsg(data) {
    responsiveChatPush(".chat-space", "me", data.msgText, data.msgId);

    var conversationData = {"engine": $("#engine-menu").val(),
            "lang": $("#language-menu").prop("checked")
             }
            fetchData("POST", "/getResponse", conversationData, afterResponse);

        $(".my-message").on('click', function(event){
        event.preventDefault();
        var msgId = $(this).attr("data-bs-msgid");
        var msgText = $(this).text();
        fetchData("POST", "/getCorrection", {"msgId": msgId, "orgMsg": msgText}, afterCorrection);
    });

    fetchData("POST", "/correctGrammar", {"msgId": data.msgId}, afterInfoCorrection)
    return false;
}

function afterInfoCorrection(data) {
    if (data.msgIdCorrected) {
        $(".chat-space .my-message").last().append('<i class="bi bi-lightning-fill text-warning"></i>')
    };
}

function afterTranslate(data) {
    var translatedMsg = data.translatedMsg;
    var orgMsg = data.orgMsg;
    var aiModal = $("#ai-msg-modal .message-menu em");
    var aiModalOrgMsg = $("#ai-msg-modal .ai-message");
    aiModal.text(translatedMsg);
    aiModalOrgMsg.text(orgMsg);
}

function afterCorrection(data) {
    var correctedMsg = data.correctedMsg;
    var orgMsg = data.orgMsg;
    var myModal = $("#my-msg-modal .message-menu em");
    var myModalOrgMsg = $("#my-msg-modal .my-message");
    if (data.msgIsCorrected) {
        myModal.text(correctedMsg);
        }
    else {
        myModal.text("Brak błędów");
    }
    myModalOrgMsg.text(orgMsg);


}

/* Activating chatbox on element */
responsiveChat(".chat-space");