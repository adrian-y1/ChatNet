let current_user = document.getElementById("current").textContent

document.querySelectorAll('#user-btn').forEach(btn => {
    btn.onclick = function(e) {
        var roomName = btn.value;
        window.location.pathname = '/chat/' + roomName + '/';
    }
});

const search = document.querySelector('.friend-search')
const card = document.querySelectorAll('.sidebar-friend')
let all_friends = []

search.addEventListener('input', e => {
    const value = e.target.value.toLowerCase();
    for(i = 0; i < all_friends.length; i++){
        if(all_friends[i].includes(value)){
            card[i].style.display = 'flex'
        } else {
            card[i].style.display = 'none'
        }
    }
})
fetch('/all_friends')
.then(res => res.json())
.then(data => {
    if (data.length > 0) {
        data.all_friends.forEach(d => {
            all_friends.push(d.username)
        })
    }
})

const openFriendSidebar = document.getElementById('open-friend-sidebar')
const friendSidebar = document.getElementById('sidebar-friends-wrap')
const closeFriendSidebar = document.getElementById('close-friend-sidebar')
const openLeftSidebar = document.getElementById('open-left-sidebar')
const closeLeftSidebar = document.getElementById('close-left-sidebar')
const domBody = document.getElementById('body')
const leftSidebar = document.getElementById('sidebar-nav')

closeLeftSidebar.style.display = 'none'
closeFriendSidebar.style.display = 'none'

document.addEventListener('DOMContentLoaded', () => {
    openFriendSidebar.onclick = () => {
        friendSidebar.style.display = 'block'
        friendSidebar.classList.add('slide-in-friend')
        friendSidebar.style.animationPlayState = 'running'
        closeFriendSidebar.style.display = 'block'
        if(window.innerWidth < 768){
            openLeftSidebar.style.display = 'none'
        }
        if(window.innerWidth < 500){
            leftSidebar.style.display = 'none'
            domBody.style.display = 'none'
        }
    }
    closeFriendSidebar.onclick = () => {
        friendSidebar.style.display = 'none'
        closeFriendSidebar.style.display = 'none'
        if(window.innerWidth < 768){
            openLeftSidebar.style.display = 'block'
        }
        if(window.innerWidth < 500){
            leftSidebar.style.display = 'none'
            domBody.style.display = 'block'
        }
    }

    openLeftSidebar.onclick = () => {
        leftSidebar.style.display = 'block'
        leftSidebar.classList.add('slide-in')
        leftSidebar.style.animationPlayState = 'running'
        closeLeftSidebar.style.display = 'block'
        if(window.innerWidth < 768){
            openFriendSidebar.style.display = 'none'
        }
        if(window.innerWidth < 500){
            friendSidebar.style.display = 'none'
            domBody.style.display = 'none'
        }
    }

    closeLeftSidebar.onclick = () => {
        leftSidebar.style.display = 'none'
        closeLeftSidebar.style.display = 'none'
        if(window.innerWidth < 768){
            openFriendSidebar.style.display = 'block'
        }
        if(window.innerWidth < 500){
            friendSidebar.style.display = 'none'
            domBody.style.display = 'block'
        }
    }
    const activeLink = window.location.pathname;
    const homeLink = document.querySelector('#home-link')
    const sidebarLinks = document.querySelectorAll('#sidebar-ul a').forEach(link => {
        if(activeLink === '/'){
            homeLink.classList.add('active');
            
        } else if(link.href.includes(`${activeLink}`)){
            link.classList.add('active');
        }
    })

})