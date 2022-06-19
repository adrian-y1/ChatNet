# ChatNet - CS50W Capstone Project 2022

## Overview 
---
*ChatNet* is a chatting web application designed for users to communicate with other fellow users via chat messaging. There are various features that *ChatNet* offers to its users which are but not limited to, *Friend Request System, Global Chat Messaging, Private Chat Messaging, Profile Picture Setting,* and many more. Users are also provided with an Authentication System whereby they are able to create their own accounts, change their passwords as well as setting their own profile pictures to help establish their online presence and their unique identity. The implementation of *ChatNet* greatly utilized the usage of `Django-Channels` to create WebSockets/Chat Rooms that run on Async Consumers where users can communicate with each other. The `pillow` libary as well as `Django-Signals` was also used to give the user the ability to change/update their profile image.


## Global Chat/Home
---
*Global Chat* is a public chat messaging view where any authenticated user can send a message to the group and this message is accessible and viewed by everyone. As mentioned earlier, to send a message the user must have an account registered, however users who are not yet authenticated can still view the Global Chat messages although they are unable to communicate as such. *Global Chat* uses WebSockets to connect users to the chat where they can view and communicate with others.
### Global Chat Infinite Scroll
*Global Chat*'s secondary feature (primary is messaging), is *Infinite Scroll*. With *Infinite Scroll*, users will only be able to see the latest 10 messages (if any) of the chat when the page is loaded. If users would like to load older messages, they can do so by scrolling to the top of the chat and load the next 10 message and so on. *Infinite Scroll* helps increase the User Experience due its functionality of only needing to scroll to the top of the chat to view older messages and it also decreases server load times since the *Global Chat View* will only need to load 10 messages when the page is loaded compared to loading 100s or even thousands of messages all at once will decrease the User's Experience due to high server load times.  
  
Infinite Scroll is implemented by creating an API that sends over the latest 10 messages every time the user scrolls to the top of the chat room. Creating Infinite Scroll, i referenced Brian's implementation of a basic one in `Lecture 6 - User Interfaces` and built greatly upon it and made it more complex. 

### Other Features
* Markdown

    - Users can utilise *Markdown Syntax* when sending messages. *Markdown* allows users to create various HTML elements by using specific and user friendly syntax. A dropup menu is provided in the message section to users who are not familiar with *Markdown* to view its functionality and syntax.

* Timestamp

    - Every message has a timestamp that specifies how long ago the message was sent.

* User Details 

    - Every message includes details about what the message was, when it was sent but also reveals the user that sent the message and their Profile Picture.


## Authentication System
---
*ChatNet's* Authentication System includes the following features:
- Register

    - With *Register*, users will be able to create their own accounts by filling out the registration form that is provided and must follow the criteria in order for their account to get created. Through this view, users can navigate to other views such as *Login* and *Change Password*.

- Login
    - In *Login*, users can sign in to the account they have created and use the website. Here they can also navigate to *Register* and *Change Password*.
- Change Password
    - Here, users who already have an account can change their password to a new one. In this view they can also navigate to *Login* and *Register*.


## Friend Request System
---
With the *Friend Request System*, users can send friend requests to other users who have an account and add them as a friend. The *Friend Request System* consists of the following features:
- Add Friend
    - When users choose **Add Friend**, a friend request will be sent to the user that it was specified to. 
- Cancel Friend Request
    - This feature is only available to the user who sent the friend request in the first place and the corresponding user who it was sent to has not responded with an answer yet. When users click this button, the friend request is canceled and deleted as if it was never there. 
- Accept 
    - This feature is only available to the users whom the friend request was sent to. If the user clicks **Accept** then they become friends.
- Decline
    - This feature is also only available to the users whom the friend request was sent to. If the user clicks **Decline**, the request is then deleted and the two users do not become friends.
- Remove Friend
    - This features is only avaialble to users whom are already friends. Clicking this option will remove them as friends. Both users have this option.

## Private Chat
---
*Private Chat* is a chat messaging system whereby two users who are friends can message each other in a private One-on-One chat. The two users must be authenticated to use and also view this feature and must be friends. Similar to *Global Chat*, *Private Chat* uses `WebSockets` and also has the following features:
### Private Chat Infinite Scroll
*Private Chat*'s Infinite Scroll functions the exact same as that of *Global Chat's*. Only the latest 10 messages are loaded when the user visits the chat and to view older messages, the user must scroll to the top of the chat. 

### Other Features (Similar to Global Chat)
* Markdown
    - Users can utilise *Markdown Syntax* when sending messages. *Markdown* allows users to create various HTML elements by using specific and user friendly syntax. A dropup menu is provided in the message section to users who are not familiar with *Markdown* to view its functionality and syntax.

* Timestamp

    - Every message has a timestamp that specifies how long ago the message was sent.

* User Details 

    - Every message includes details about what the message was, when it was sent but also reveals the user that sent the message and their Profile Picture.

## Profile
---
In a user's *Profile*, details such as their name, email address, join date as well as the amount of friends they have are displayed. *Profile* Includes various features such as:
- Profile Picture
    - When users view their own profile, they are able to click the camera button in order to change their profile picture if desired. This picture will be displayed anywhere their name is associated with. 
    - This feature is created by using the `pillow` library and `Django-Signals` module. 
- Add Friend
    - Users can send friend requests to other users when they are viewing that user's if that user is not their current friend.
- Cancel Friend Request
    - Users who sent the request can also cancel it here.
- Accept 
    - Users whom the friend request was sent to can view the sender's profile and accept their request in order to become friends and chat privately.
- Decline
    - Users whom the friend request was sent to can view the sender's profile and decline their request and then the request will be deleted.
- Message
    - If the current user's profile that is being viewied is friends with the currently authenticated user, then that user has the option to click **message* to be redirected to the private chat room.
- Remove Friend
    - Users whom are already friends can remove each other as friends via each other's profile. 

## Friends
---
In this view, users will be able to see all their people they have as friends. Features include:
- User Details
    - The username and profile picture of that friend will be displayed here. Clicking either will take you to their profile page.
- Message
    - Clicking **message** will take you to the private chat room that has you and that friend. 
- Remove
    - Clicking **remove** you can remove the current friend from your friends list.
- Search
    - You can search through your friends list for your friend's username here by typing their full username or substrings. 

## Add Users
---
In this view, there will be a list of all the users who you do not currently have as friends. Features that *Add Users* includes are:
- User Details
    - The username and profile picture of that user will be displayed here. Clicking either will take you to their profile page.
- Add Friend
    - You can send friend requests to other users here by clicking **Add Friend**.
- Cancel Friend Request
    - You can also cancel the friend request you sent by clicking **Cancel**.
- Accept 
    - Here you can also see if a user has sent you a friend request, if so you can choose to **Accept** their friend request and become friends.
- Decline
    - Similary, you can also **Decline** the friend request sent to you.
- Search
    - You can search through the list of all non-friended users here by typing their full username or substrings. 

## Incoming
---
*Incoming* displays all of the incoming friend requests that other users have sent for you. Features:
- User Details
    - The username and profile picture of the users will be displayed here. Clicking either will take you to their profile page.
- Accept 
    - Here you can choose to **Accept** friend requests sent to you to become friends with the sender.
- Decline
    - Similary, you can also **Decline** the friend requests sent to you.

## Outgoing
---
*Outgoing* is the opposite of *incoming*. Here you will see all the friend requests of whom you have sent. Features Include:
- User Details
    - The username and profile picture of the users will be displayed here. Clicking either will take you to their profile page.
- Cancel
    - Clicking **cancel** will cancel the friend request you have sent. 

## Friend Sidebar
---
This sidebar is displayed on the right side of your screen and is accessible no matter what page you are on. The *Friends Sidebar* displays a full list of your current friends including the following feautres:
- Search
    - You can search for a specific friend at any time by typing in their username or substrings of their username. 
- User Details
    - You can view their username and current profile picture. Clicking on either will take you to their profile page.
- Message
    - Clicking the message icon will take you directly to the private chat of you and that friend.
- Latest Message
    - The latest message between you and that friend will be displayed under the friend's name and it will involve details such as who the latest message was sent by and part of the message content it self.

## Navigation Sidebar
---
This sidebar is displayed on the left of your screen and is also accessible no matter what page you are on. This sidebar displays links to the following pages:
- Home (Global Chat)
- Profile (Your Profile Page)
- Friends
- Add Users
- Incoming
- Outgoing  

*Incoming* and *outgoing* have a bell icon that shakes if you have 1 or more requests in them to notify you.

At the bottom of the sidebar your profile picture and username are also displayed. Clicking on either will take you to your profile page. A logout icon is also displayed which if clicked, will log you out of your account.

## Files
---
The following is a list of files used in my project and their purpose.

### Static
- `static\chat\images` - Here i store the website's general logo.
- `static\chat\js\global_chat.js` - This is a JS file used to perform functions that coresspond to the `index.html` file. Functions include but not limited to, creating a WebSocket, listening for `connecting/disconnecting` events, adding `onmessage` event listener to detect when a message has been sent to the WebSocket as well as creating Infinite Scroll function.
- `static\chat\js\room.js` - This is also a JS file that is tied to `room.html` and has essentially similar functions `global_chat.js`, however the main difference here is that WebSockets are created for every 2 users who become friends making the WebSocket unique to only them two and not accessible by anyone else. The other main function `room.js` includes is Infinite Scroll.
- `static\chat\js\layout.js` - This is a JS file coressponding to `layout.html` and has the implementations of several functions such as searching through friends list which is done through an API created in `views.py` that provides a list of all friends, functions that make the website responsive on smaller devices as well as adding animation and making links active.
- `static\chat\styles.css` - This file includes all CSS styling created and performed on the website. 

### Templates
- `chat\templates\chat\change_password.html` - The HTML template used for displaying to the user a form for changing their password.
- `chat\templates\chat\error.html` - A custom error page that displays appropriate message depending on the error received.
- `chat\templates\chat\friends_list.html` - This file displays to the user their all friends as well as a form where the user can remove a friend. A real time search bar is also implemented used to search for friends which is done by creating an API that gives current user's friend list.
- `chat\templates\chat\incoming.html` - Displays all incoming friend requests as well as a form to accept and decline those requests.
- `chat\templates\chat\outgoing.html` - Displays all outgoing friend requests as well as a form to cancel those requests.
- `chat\templates\chat\index.html` - This file displays to the user the global chat room which involves all the messages, textarea to send a message as well as a send button and a question mark button to view markdown syntax.
- `chat\templates\chat\layout.html` - This file is the base template for the website that includes the sidebars on all pages.
- `chat\templates\chat\login.html` - Displays a login form to the user.
- `chat\templates\chat\register.html` - Displays a registeration form to the user.
- `chat\templates\chat\profile.html` - This file is used to display the profile pages for every user. It also includes features such as changing profile picture, sending, canceling, accepting or declining a friend request. As well as removing a friend.
- `chat\templates\chat\suggestions.html` - This file displays all users that are not currently friends with the current user. Features include, sending, canceling, accepting and or declining friend requests.

### .py files
- `chatapp\chat\admin.py` - Used to register models so they are acessible in Admin Dashboard for creating, deleting, updating and or reading data in the database.
- `chatapp\chat\consumers.py` - In this file, Asynchronous consumers are written for both Global Chat and Private Chat which are used to accept websocket connections that are created. The 4 main events are detecting when a user connects and opens a websocket, detecting when they disconnect/close the WebSocket, detecting when a message is sent to the websocket as well as detecting when a message is received. The messages along with various other details are also saved here in regards to their coressponding models.
- `chatapp\chat\context_processors.py` - This file holds several functions created to pass variable that hold data to any desired template.
- `chatapp\chat\models.py` - This file includes all the models that have been created and used to store data.
- `chatapp\chat\routing.py` - This file includes the routing configurations used to connect a URL route to the corresponding consumer similar to what views are to urls.
- `chatapp\chat\signals.py` - This file utilizes the usage of Django Signals in order to detect when a User object is created and when it is created, create a profile object coressponding to that user and save it. 
- `chatapp\chat\urls.py` - In this file, all the URLs and their coressponding `views` are stored here.
- `chatapp\chat\views.py` - This file includes all the python functions/views that are created to perform certain tasks. Each view maps to a particular URL in `urls.py`.
- `chatapp\urls.py` - This file maps to the `chat` app's urls.py file.
- `chatapp\asgi.py` - This file maps to the `chatapp\chat\routing.py` configuration file which involves a `ProtocolTypeRouter` wrapper that checks if a connection is ws (webscoket), if so then it is given to `AuthMiddlewareStack` which populates a connections scope. 

### Media File
- `chatapp\media` - This folder is used to store the default image that all newly registered users get, however this folder consists of another folder called `profile_pictures` which uniquely stores all the images/pictures users use for their profile pictures.

## Responsive
---
ChatNet is responsive can work on any device, particularly mobile-devices as the elements are resized and altered depending on the user's viewport. Elements such as the sidebars are not displayed on smaller screens unless the user clicks their respective buttons to display them.

## Distinctiveness and Complexity
--- 
This project is very distinctive to the other projects i have created in this course because firstly, this website is responsive and can be used on any device. Secondly, the use of `Django-Channels` library and in particular `WebSockets` that run on `Asynchronous` consumers, provides a level of complexity as well as distinctiveness that is far greater than that of any project i have done, as this project has taken me well over a month to finish. Thirdly, the use of a Friend Request System is very distinctive to that of follow/unfollow system used in `Project 4 - Network` along with using `pillow` and `Django-Signals` to help create a system where users can freely update and choose their own profile pictures. Lastly, i used a large amount of JavaScript to create various unique functions such as Infinite Scroll but as well using JavaScript to make the website responsive and interactive. 

## How to run
---
### Option 1 - Redis
This application utilizes `channel_redis` and the use of WSL to open a redis server which serves as a `BACKEND` for the channel layers.Firstly, you must install channels_redis with `pip install channels_redis` in the terminal. Then you must install `Ubuntu` from microsoft store to use Windows Subsystem for Linux. After you have the WSL working, use the following commands in `Ubuntu` to install redis:
- `sudo apt-add-repository ppa:redislabs/redis`
- `sudo apt-get update`
- `sudo apt-get upgrade`
- `sudo apt-get install redis-server`
Once you have redis installed, use `redis-cli` to use redis's Command Line Interface then enter `redis-server` to open a redis server. Now go to the projects terminal and change directory into chatapp with `cd chatapp` and runserver with `python manage.py runserver` to start using the web app.
  
### Option 2 - InMemory
If option 1 if very complicated, you can remove redis configuration i have done and use a InMemory option provided with django-channels that however should only be used in development and testing environment. To do this:
- Go to `settings.py` and find `CHANNEL_LAYERS`
- Remove `'CONFIG': { "hosts": [('127.0.0.1', 6379)], },`
- Remove the current BACKEND line and add `'BACKEND': 'channels.layers.InMemoryChannelLayer'`
- Go to the projects terminal and change directory into chatapp with `cd chatapp` and runserver with `python manage.py runserver` to start using the web app.

Enjoy!
## Conclusion
---
To conclude, creating this project was very challenging as it was my first time using the `Django-Channels` library and to help with this i spent the first week learning about the library and in particular `WebSockets`, `Consumers` and `Asynchronous functions` and i did not start coding till the second week. This project expanded my knowledge and showed me whats possible as well as pushing me to my limits and finding what i was capable of doing. I learned alot of things from this project that i will use to make better projects.