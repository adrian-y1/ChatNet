

const globalChatContainer = document.querySelector('.global-chat-container')
const globalChatBox = document.querySelector('.global-chat-box')
const username = JSON.parse(document.getElementById('current-user-username-global').textContent)
const currentUserPicture = JSON.parse(document.getElementById('current-user-picture-global').textContent)

const dropupBtn = document.querySelector('.dropup-btn')
const dropupContent = document.querySelector('.dropup-content')

if(dropupContent !== null){
    dropupContent.style.display = 'none'
}

if(dropupBtn != null){
    dropupBtn.onclick = () => {
        if(dropupContent.style.display === 'block') {
            dropupContent.style.display = 'none'
        }else {
            dropupContent.style.display = 'block'
        }
    }
}

window.addEventListener('mouseup', function(event) {
    if(event.target != dropupContent && event.target.parentNode != dropupBtn){
        if (dropupContent !== null ) {
            dropupContent.style.display = 'none'
        }
    }
})


const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/'
    + ' '
    
);

chatSocket.onconnect = function (e) {
    const data = JSON.parse(e.data)
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const el = document.createElement('div')
    if(data.username === username){
        el.innerHTML = `<li class="chat-right">
                            <div class="chat-msg-con">
                                <div class="d-flex justify-content-end flex-column align-items-end">
                                    <div id="chat-log" class="chat-message">
                                        ${data.message}
                                    </div>
                                    <div class="date-con">
                                        <p>${data.current_time}</p>
                                    </div>
                                </div>
                            </div>
                        </li>`
    } else {
    el.innerHTML = `<li class="chat-left">
                        <div class="chat-msg-con">
                            <div class="chat-icon">
                                <img src="${data.img}" alt="" class="rounded-circle">
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
    }
    globalChatContainer.appendChild(el)
    globalChatContainer.scrollTo(0, globalChatContainer.scrollHeight)
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

if(document.querySelector('#chat-message-input') !== null){
    document.querySelector('#chat-message-input').focus();
}
if(document.querySelector('#chat-message-input') !== null){
    document.querySelector('#chat-message-input').onkeydown = function(e) {
        if (e.keyCode === 13 && !e.shiftKey) {  // enter, return
            e.preventDefault();
            document.querySelector('#chat-message-submit').click();
        }
    };
}

if(document.querySelector('#chat-message-submit') !== null){
    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        if (message.trim() !== ''){
            chatSocket.send(JSON.stringify({
                'message': message,
                'username': username
            }));
            messageInputDom.value = '';
        }
    };
}


// ---------------- Infinite Scroll ---------------- \\


loading = document.querySelectorAll(".loading")
loading.forEach(l => {
    l.style.animationPlayState = 'paused';
})

function animate () {
    loading.forEach(l => {
        l.style.animationPlayState = 'running';
    })
}

let counter = 0;
let stop_execution = 0;
let num_of_posts = 10;

document.addEventListener('DOMContentLoaded', load);

window.onload = () => {
    console.log("Fully Loaded")
    setTimeout(() => {
        globalChatContainer.scrollTo({top: globalChatContainer.scrollHeight, behavior: 'smooth' }) 
    }, 100);
    console.log("Scrolled Bottom")
}

document.querySelector('.loading-con').style.display = 'none';

globalChatContainer.onscroll = () => {
    if(globalChatContainer.scrollTop === 0 ){
        if(counter < stop_execution){
            document.querySelector('.loading-con').style.display = 'flex';
            animate();
            setTimeout(function(){
                load();
                if(stop_execution / counter > 1){
                    globalChatContainer.scrollTo({ top: 600, left: 600, behavior: 'smooth'})
                } else {
                    globalChatContainer.scrollTo({ top: 100, left: 100, behavior: 'smooth'})
                }
              }, 1000)
        }
    } else {
        document.querySelector('.loading-con').style.display = 'none'
    }
}

function load() {
    let start = counter;
    let end = start + num_of_posts - 1;
    counter = end + 1;

    url = `/global_messages?start=${start}&end=${end}`
    fetch(url)
    .then(res => res.json())
    .then(data => {
        stop_execution = parseInt(data.length_msg)

        data.messages_data.forEach(function(msg) {
            add_msg(msg)
        })
    })
    .catch(error => console.log("ERROR:", error))
}

function add_msg(msg) {
    const element = document.createElement('div')
    if(msg[0].user.username === username){
        element.innerHTML += `<li class="chat-right">
                                <div class="chat-msg-con">
                                    <div class="d-flex justify-content-end flex-column align-items-end">
                                        <div id="chat-log" class="chat-message">
                                            ${msg[0].content}
                                        </div>
                                        <div class="date-con">
                                            <p>${msg[0].date_sent}</p>
                                        </div>
                                    </div>
                                    
                                </div>
                            </li>`
    } else {
        element.innerHTML += `<li class="chat-left">
                                <div class="chat-msg-con">
                                    <div class="chat-icon">
                                        <img id="chat-icon-img" src="${msg[1].user_img}" alt="" class="rounded-circle">
                                        <div class="chat-name">${msg[0].user.username}</div>
                                    </div>
                                    <div class="d-flex justify-content-start flex-column align-items-start">
                                        <div class="chat-message">
                                            ${msg[0].content}
                                        </div> 
                                        <div class="date-con">
                                            <p>${msg[0].date_sent}</p>
                                        </div>
                                    </div>
                                </div>
                            </li>`
    }
    globalChatBox.append(element)
}