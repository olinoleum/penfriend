
const msgSent = document.getElementById("message-sent");
const sendBtn = document.getElementById("send-button");

function getResponse() {
    addNewMessage("You:", msgSent.value);
    var botResponse = sendResponseRequest();
    addNewMessage("Bot:", botResponse);
}

function addNewMessage(sender, msg) {
    var conversationField = document.querySelector(".conversation-field");

    var msgField = document.createElement("div");
    msgField.className = "message-field";

    var senderElement = document.createElement("div");
    senderElement.className = "sender";
    senderElement.textContent = sender;

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
    var messages = document.querySelectorAll(".message-field");
    var currentConversationArr = [];

    messages.forEach(function(msgField) {
        currentConversationArr.push(msgField.textContent);
    });

    var currentConversation = currentConversationArr.join("\n");
    console.log(currentConversation);
    return "This is bot at level " + engineLevel;
};