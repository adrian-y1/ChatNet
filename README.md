# ChatNet

Visit website: [chatnet.up.railway.app](https://chatnet.up.railway.app/)

## Overview

ChatNet is a web application that enables users to chat with each other in real-time. It has various features such as a Friend Request System, Global Chat Messaging, Private Chat Messaging, Profile Picture Setting, infinite scroll and more. Users can create accounts, change passwords, and set profile pictures to establish their unique online presence. `django-channels` was used to create WebSockets/Chat Rooms for `Async Consumers` to facilitate user communication, and the `pillow` library and `django-signals` were used to allow users to update their profile image.

This application was developed as the final project for the "[CS50's Web Programming with Python and JavaScript course](https://cs50.harvard.edu/web/2020/)" course offered by Harvard University.

## Features Overview

- Login, Register & Forgot Password
- Real-time text messaging
- Private chat & Global chat
- Infinite Scroll
- Markdown support
- Profile Picture
- Message Timestamps & User details on each message
- Send/Cancel Friend Request
- Accept/Decline Friend Request
- Remove Friend
- Timestamps use the user's timezone
- Incoming & Outgoing Friend Requests
- Search users/friends feature created with Ajax requests
- API Endpoints in views.py are used extensively with Ajax requests
- DOM manipulation
- Reponsive design that works on different screen sizes
- User-friendly UI
- Visually Appealing design

## Global Chat/Home

The Global Chat feature of the app enables registered users to send and receive messages in a public chat view accessible by all authenticated users. Utilizing WebSockets, users can easily communicate with each other in real-time. Unregistered users can view the chat messages, but they are not allowed to participate in the conversation until they have created an account.

## Private Chat

Private Chat allows two authenticated users who are friends to communicate with each other in a private one-on-one chat messaging system. To use this feature, the two users must be friends and must have registered accounts. Like Global Chat, Private Chat also utilizes WebSockets for real-time messaging

## Infinite Scroll

The chat messaging feature in both private and global chat uses Infinite Scroll to load only the latest 10 messages when the page is loaded. Users can load older messages by scrolling to the top of the chat. This feature helps improve user experience and reduces server load times since the chat view only needs to load 10 messages at a time. It was implemented by creating an API that sends the latest 10 messages every time the user scrolls to the top of the chat, building upon Brian's basic implementation in [Lecture 6 - User Interfaces](https://cs50.harvard.edu/web/2020/weeks/6/).

### More Chatting Features

- Markdown Support:
  - ChatNet supports Markdown syntax in messages. This allows users to easily format their messages using simple and intuitive syntax. A drop-down menu is provided for users who are not familiar with Markdown to view its functionality and syntax.
- Timestamps:
  - Each message displays a timestamp that indicates when the message was sent, allowing users to easily track the timing of conversations.
- User Details:
  - Each message displays the user's name, profile picture, and message content, providing users with more context about the message they are reading.

## Authentication System

- Register

  - Register allows users to create their own accounts by filling out a registration form. Users must follow specific criteria to successfully create their account. This view also provides access to other authentication views, such as Login and Change Password.

- Login

  - Login enables users to sign in to their account and access the website. Users can also navigate to other authentication views, such as Register and Change Password.

- Change Password

  - Change Password enables users to update their password. In this view, users can also navigate to other authentication views, such as Login and Register.

## Friend Request System

The Friend Request System enables users to send friend requests to other users who have an account and add them as friends. This system consists of the following features:

- Add Friend
  - When users click on "Add Friend", a friend request is sent to the specified user.
- Cancel Friend Request
  - If the user who sent the friend request has not yet received a response, they can cancel the request by clicking on "Cancel Friend Request".
- Accept
  - Users who receive a friend request can click on "Accept" to become friends with the sender.
- Decline
  - If users choose to decline a friend request, they can click on "Decline" and the request will be deleted.
- Remove Friend
  - Once users become friends, they can choose to remove the friendship by clicking on "Remove Friend". This option is available to both users.

## Friend Sidebar

The Friend Sidebar is a convenient feature accessible from any page of the website, displayed on the right-hand side of the screen. It lists all of your current friends and includes the following features:

- Search
  - You can easily search for a specific friend by typing in their username or a substring of their username. This feature is implemented using DOM manipulations and Ajax request.
- User Details
  - You can view your friends' usernames and current profile pictures, and clicking on either will take you to their profile page.
- Message
  - Clicking the message icon will take you directly to the private chat between you and that friend.
- Latest Message
  - The latest message between you and that friend will be displayed under the friend's name, showing who sent it and part of the message content.

## Difficulties

Developing this project has been one of the most challenging experiences for me as a web developer. I had to learn a variety of new concepts and technologies, such as Django-channels, websockets, asynchronous and synchronous programming, consumers, channels, and routes, which were previously unfamiliar to me. Implementing the real-time chat messaging feature with a database to store the chat messages and their details was by far the most challenging part of the project.

## Overcoming Difficulties

To successfully implement the real-time chat messaging feature using django-channels library, I adopted a systematic approach that involved dedicating the first week to learning about the library and its dependencies. During this period, I took the time to carefully read through the documentation, take notes, and plan how to go about tackling various features of the website such as the friend request system, infinite scroll, authentication system, and the messaging feature itself. I documented everything, including ideas and approaches, problems and solutions, and UI features to implement.

I also sought assistance from various online communities such as Discord, YouTube videos, and forums whenever I encountered challenges. By doing so, I was able to obtain useful tips and suggestions from other experienced developers who have previously faced similar challenges. This helped to educate me to avoid making costly mistakes and fix mistakes that i have already made.

Throughout the development process, I kept a keen eye on the overall user experience, ensuring that the website is both visually appealing and user-friendly.

Overall, while the project was challenging, the systematic approach, dedication, and willingness to seek help when needed were key to overcoming the difficulties and delivering a good quality website.

## Conclusion

In conclusion, building this complex project such as a real-time messaging system with a friend request feature was a very challenging and overwhelming task. However, by dedicating time to learning the necessary technologies and planning out the features and implementation approach, it was possible to overcome these difficulties. Utilizing resources such as documentation, online communities, and tutorials was very helpful in finding solutions to problems that arose during the development process. Overall, taking a structured and strategic approach, along with perseverance and a willingness to learn, helped lead me to a successful implementation of a challenging project.

With the knowldege and practical experience i gained from this project, i have been able to use it whilst developing the [Facebook Clone](https://github.com/adrian-y1/odin-facebook) project.
