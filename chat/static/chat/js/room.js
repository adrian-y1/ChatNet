
const chatContainer = document.querySelector('.chat-container')
const chatBox = document.querySelector('.chat-box')


const other_user_name = JSON.parse(document.getElementById('other-user-name').textContent);
const other_user = JSON.parse(document.getElementById('other-user-id').textContent);
const userName = JSON.parse(document.getElementById('current-user-id').textContent);
const currentTime = JSON.parse(document.getElementById("current-time").textContent);
const current_user_profile_pic = JSON.parse(document.getElementById('current-user-profile-pic').textContent)
const other_user_profile_pic = JSON.parse(document.getElementById('other-user-profile-pic').textContent)
const currentUserIdentification = JSON.parse(document.getElementById('current-user-identification').textContent)
const dropupBtn = document.querySelector('.dropup-btn')
const dropupContent = document.querySelector('.dropup-content')

dropupContent.style.display = 'none'

dropupBtn.onclick = () => {
    if(dropupContent.style.display === 'block') {
        dropupContent.style.display = 'none'
    }else {
        dropupContent.style.display = 'block'
    }
}

window.addEventListener('mouseup', function(event) {
    if(event.target != dropupContent && event.target.parentNode != dropupBtn){
        dropupContent.style.display = 'none'
    }
})

// Create a new websocket for the room name that was entered
const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/wss/chat/'
    + other_user
    + '/'
);

// Listen for the .onmessage event 
// The .onmessage event occurs when a message is recieved through an event source. 
// When a message is recieved, use JSON.parse to turn it into a JavaScript Object
// data.message grabs the message from the data 
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const el = document.createElement('div')
    const rooms = document.querySelectorAll('.latest-message')

    if (data.username === userName){
        console.log(data.username, userName)
        el.innerHTML = `<li class="chat-right">
                            <div class="chat-msg-con">
                                <div class="d-flex justify-content-end flex-column align-items-end">
                                    <div id="chat-log"  class="chat-message">
                                        ${data.message}
                                    </div>
                                    <div class="date-con">
                                        <p>${data.current_time}</p>
                                    </div>
                                </div>
                            </div>
                        </li>`
        
        rooms.forEach(r => {
            if(r.dataset.room.includes(`${String(currentUserIdentification)}`) && r.dataset.room.includes(`${String(other_user)}`)){
                
                if(data.message.includes('<h1>') || data.message.includes('<h2>') || data.message.includes('<h3>') || data.message.includes('<h4>')){
                    r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>You:</strong>${data.message.slice(4)}</span>`

                } else {
                    if(data.message.length > 20){
                        r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>You:</strong>${data.message.slice(0, 20)}...</span>`
                    } else {
                        r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>You:</strong>${data.message.slice(0, 20)}</span>`
                    }
                }
            }
        })

    } else {
        el.innerHTML = `<li class="chat-left">
                            <div class="chat-msg-con">
                                <div class="chat-icon">
                                    <img src="${other_user_profile_pic}" alt="" class="rounded-circle">
                                    <div class="chat-name">${data.username}</div>
                                </div>
                                <div class="d-flex justify-content-start flex-column align-items-start">
                                    <div class="chat-message">
                                        ${data.message}
                                    </div> 
                                    <div class="date-con">
                                        <p>${data.current_time}</p>
                                    </div>
                                </div>
                            </div>
                        </li>`
        rooms.forEach(r => {
            if(r.dataset.room.includes(`${String(currentUserIdentification)}`) && r.dataset.room.includes(`${String(other_user)}`)){
                if(data.message.includes('<h1>') || data.message.includes('<h2>') || data.message.includes('<h3>') || data.message.includes('<h4>')){
                    r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>${data.username}:</strong>${data.message.slice(4)}</span>`

                } else {
                    if(data.message.length > 20){
                        r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>${data.username}:</strong>${data.message.slice(0, 20)}...</span>`
                    } else {
                        r.innerHTML = `<span class="latest-msg-temp flex-wrap-wrap d-flex flex-row justify-content-start align-items-start px-0"><strong>${data.username}:</strong>${data.message.slice(0, 20)}</span>`
                    }
                }
            }
        })
    }
    chatContainer.appendChild(el)
    chatContainer.scrollTo(0, chatContainer.scrollHeight)
};
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// When enter key is pressed, force click submit button
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeydown = function(e) {
    if (e.keyCode === 13 && !e.shiftKey) {  // enter, return
        e.preventDefault();
        document.querySelector('#chat-message-submit').click();
    }
};

// When the submit button is clicked, grab the input value of the message that was entered, and send it to the chatSocket
document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if(message.trim() !== ''){
        chatSocket.send(JSON.stringify({
            'message': message,
            "username": userName,
            "current_time": currentTime
    
        }));
        // here we reset the value of the input to empty string
        messageInputDom.value = '';
    }
};

// ---------------- Infinite Scroll ---------------- \\

loading = document.querySelectorAll(".loading")
loading.forEach(l => {
    l.style.animationPlayState = 'paused';
})

function run_animate () {
    loading.forEach(l => {
        l.style.animationPlayState = 'running';
    })
}
// Start with First post
let counter = 0;

let stop_execution = 0;

// load 10 posts at a time
let num_of_posts = 10;

// When DOM loads, render the frist 10 posts
document.addEventListener('DOMContentLoaded', load);

window.addEventListener('load', () => {
    console.log("Fully Loaded")
    setTimeout(() => {
        chatContainer.scrollTo({top: chatContainer.scrollHeight, behavior: 'smooth' }) 
    }, 1000);
    console.log("Scrolled Bottom")
})


document.querySelector('.loading-con').style.display = 'none';
// If scrolled to top, load the next 20 posts
chatContainer.onscroll = () => {
    if(chatContainer.scrollTop === 0){
        if(counter < stop_execution){
            console.log(counter, stop_execution)
            document.querySelector('.loading-con').style.display = 'flex';
            run_animate();
            setTimeout(function(){
                load();
                if(stop_execution / counter > 1){
                    chatContainer.scrollTo({ top: 600, left: 600, behavior: 'smooth'})
                } else {
                    chatContainer.scrollTo({ top: 100, left: 100, behavior: 'smooth'})
                }
              }, 500)
        } 
    } else {
        document.querySelector('.loading-con').style.display = 'none'
    }
};

// Load next set of posts
function load() {
    let start = counter;
    let end = start + num_of_posts - 1;
    counter = end + 1;
    
    url = `/chat/${other_user_name}/messages?start=${start}&end=${end}`

    // Get new posts and add posts
    fetch(url)
    .then(response => response.json())
    .then(data => {
        
        stop_execution = parseInt(data.length_msg)
       
        // For each msg sent...
        data.messages_data.forEach(function(msg) {
            add_msg(msg)
        })
    })
    .catch(error => console.log("ERROR:", error))
}

function add_msg(msg){
    const element = document.createElement('div')
    if(msg.user.username === userName){
        element.innerHTML += `<li class="chat-right">
                                <div class="chat-msg-con">
                                    <div class="d-flex justify-content-end flex-column align-items-end">
                                        <div id="chat-log"  class="chat-message">
                                            ${msg.content}
                                        </div>
                                        <div class="date-con">
                                            <p>${msg.date_sent}</p>
                                        </div>
                                    </div>
                                </div>
                            </li>`
    } else {
        element.innerHTML += `<li class="chat-left">
                                <div class="chat-msg-con">
                                    <div class="chat-icon">
                                        <img src="${other_user_profile_pic}" alt="" class="rounded-circle">
                                        <div class="chat-name">${msg.user.username}</div>
                                    </div>
                                    <div class="d-flex justify-content-start flex-column align-items-start">
                                        <div class="chat-message">
                                            ${msg.content}
                                        </div> 
                                        <div class="date-con">
                                            <p>${msg.date_sent}</p>
                                        </div>
                                    </div>
                                </div>
                            </li>`
    }
    chatBox.append(element)
}
