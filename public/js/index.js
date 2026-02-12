const socket = io();
const messagesDiv = document.getElementById('messages');
const messageForm = document.getElementById('sender');
const usernameForm = document.getElementById('formUsername');
const usernameInput = document.getElementById('username');
const messageInput = document.getElementById('messageInput');

// Récupérer le username depuis le cookie
let username = Cookies.get('username');
if (username) {
    usernameInput.value = username;
}

// Initialiser highlight.js
hljs.highlightAll();

// Fonction pour ajouter un message au DOM
function appendMessage(msg) {
    const messageParts = msg.message.split(' ');
    const isImageCommand = messageParts[0] === '/image';

    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg';

    if (isImageCommand && messageParts.length > 1) {
        msgDiv.innerHTML = `<div>
                                <strong>${msg.username} :</strong>
                                <img src="${messageParts[1]}" alt="Image envoyée">
                            </div>
                            <p class="date">${msg.date}</p>`
    } else {
        msgDiv.innerHTML = `<div>
                            <strong>${msg.username} :</strong>
                            <p>${msg.message}</p>
                        </div>
                        <p class="date">${msg.date}</p>`
    }

    messagesDiv.appendChild(msgDiv);
    hljs.highlightAll();
    return msgDiv;
}

// Recevoir les messages existants
socket.on('update_messages', (data) => {
    appendMessage(data);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Recevoir un nouveau message
socket.on('new_message', (data) => {
    appendMessage(data);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Envoyer un message
messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    if (message && username) {
        socket.emit('send_message', { username, message });
        messageInput.value = '';
    } else if (!username) {
        usernameInput.style.borderColor = "#cf6679"
        usernameForm.querySelector('input[type="submit"]').style.borderColor = "#cf6679"
        usernameForm.querySelector('input[type="submit"]').style.backgroundColor = "#cf6679"
    }
});

// Définir le username
usernameForm.addEventListener('submit', (e) => {
    e.preventDefault();
    username = usernameInput.value.trim();
    if (username) {
        Cookies.set('username', username, { expires: 30 });
    }
});
