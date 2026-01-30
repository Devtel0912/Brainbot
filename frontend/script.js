const InputMessage = document.getElementById("InputMessage");
const sendBtn = document.getElementById("sendBtn");
const chatbox = document.getElementById("chatbox");
const brainBtn = document.getElementById("brainBtn");
const chatbot = document.querySelector(".container");



/* ------------------ CHAT VISIBILITY ------------------ */

// Hide chatbot on page load
chatbot.style.display = "none";

// Open chatbot when brain is clicked
brainBtn.addEventListener("click", () => {
    chatbot.style.display = "flex";
    brainBtn.style.display = "none";
    InputMessage.focus();
});





function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    
    if (sender === "bot") {
        const icon = document.createElement("i");
        icon.classList.add("fa-solid", "fa-brain", "bot-chat-logo"); // use the same class as your HTML
        msgDiv.appendChild(icon); // icon comes first
    }

    const textBubble = document.createElement("span");
    textBubble.classList.add("text-bubble");
    textBubble.textContent = text;
    
    msgDiv.appendChild(textBubble);
    chatbox.appendChild(msgDiv);
    
   
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage(){
    const message=InputMessage.value.trim();

    if(!message) return ; 
    appendMessage(message,"user");
    InputMessage.value = '';
    sendBtn.disabled=true;


    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method:'POST',
            headers: { 'Content-Type': 'application/json' },
            body:JSON.stringify({message})
        })

        if (!response.ok) throw new Error("Network Response not working");

        const data = await response.json();
         // data.reply
         appendMessage(data.reply,"bot")

    } catch (error) {
        appendMessage('Error219: Could not reach server','bot');
    } finally{
        sendBtn.disabled=false;
        InputMessage.focus();

    }

    console.log(message);
}


sendBtn.addEventListener("click",sendMessage)
InputMessage.addEventListener("keypress",function (e){
    if (e.key == "Enter") sendMessage();
})