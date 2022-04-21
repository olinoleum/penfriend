
const msgSent = document.getElementById("message-sent");
const sendBtn = document.getElementById("send-button");

function getResponse() {
    addNewMessage("You:", msgSent.value);
    sendResponseRequest();
    msgSent.value = "";
}

function addNewMessage(sender, msg) {
    var conversationField = document.querySelector(".conversation-field");

    var msgField = document.createElement("div");
    msgField.className = "message-field";

    var senderElement = document.createElement("div");
    senderElement.className = "sender";
    senderElement.textContent = sender;

    if (sender == "Bot:") {
        msgField.classList.add("sender-bot");
    } else {
        msgField.classList.add("sender-user");
    }

    var messageElement = document.createElement("div");
    messageElement.className = "message";
    messageElement.textContent = msg;

    msgField.appendChild(senderElement);
    msgField.appendChild(messageElement);

    conversationField.appendChild(msgField);

    conversationField.scrollTop = conversationField.scrollHeight;
}

function sendResponseRequest() {
    var engineLevel = document.getElementById("level-choice").value;
    var lang = document.getElementById("lang").value;
    var messages = document.querySelectorAll(".message-field");
    var currentConversationArr = [];

    messages.forEach(function(msgField) {
        var sender = msgField.querySelector(".sender").textContent;
        var msg = msgField.querySelector(".message").textContent;
        currentConversationArr.push(sender+msg);
    });

    currentConversationArr.push("Bot:")

    var currentConversation = currentConversationArr.join("\n")
    console.log("fetching data");
    fetchData("POST", "/getResponse", {"engine":engineLevel,
    "prompt":currentConversation, "lang": lang
    });
};

function fetchData(method, endpoint, body){
    event.preventDefault();
    req = $.ajax({
        type: method,
        url: endpoint,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(body)});


    req.done(function(data){
            console.log(data);
            addNewMessage("Bot:", data);
            return false;
            });
    };


$(document).ready(function(){
    $("#send-button").on("click", function(){
        getResponse();
    })

});