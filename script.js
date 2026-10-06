const chatBox=document.getElementById("chatBox");
const input=document.getElementById("userInput");


input.addEventListener("keypress",(e)=>{
if(e.key==="Enter") sendMessage();
});


async function sendMessage(){

let message=input.value.trim();
if(!message) return;

addUser(message);
input.value="";

showTyping();

const res=await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message})
});

const data=await res.json();

removeTyping();
streamText(data.reply);
}


// USER MESSAGE
function addUser(text){
chatBox.innerHTML+=`
<div class="flex justify-end">
<div class="bg-blue-500 p-3 rounded-xl">${text}</div>
</div>`;
scrollBottom();
}


// STREAM RESPONSE
function streamText(text){

let div=document.createElement("div");
div.className="bg-[#444654] p-3 rounded-xl";
chatBox.appendChild(div);

let i=0;

let interval=setInterval(()=>{
div.innerHTML+=text.charAt(i);
i++;
scrollBottom();

if(i>=text.length)
clearInterval(interval);

},10);
}


// TYPING
function showTyping(){
chatBox.innerHTML+=`
<div id="typing" class="bg-[#444654] p-3 rounded-xl">
Nova AI typing...
</div>`;
scrollBottom();
}

function removeTyping(){
document.getElementById("typing")?.remove();
}


// AUTO SCROLL
function scrollBottom(){
chatBox.scrollTop=chatBox.scrollHeight;
}


// LOAD HISTORY
async function loadHistory(){

const res=await fetch("/history");
const data=await res.json();

data.forEach(chat=>{
addUser(chat[0]);
streamText(chat[1]);
});
}

loadHistory();