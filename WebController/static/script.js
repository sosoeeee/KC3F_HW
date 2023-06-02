function sendMessage() {
    var message = document.getElementById('messageInput').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send-message', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('message=' + encodeURIComponent(message));
}
