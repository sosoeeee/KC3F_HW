var joystick1 = document.getElementById('joystick1');
var stick1 = document.getElementById('stick1');
var joystick2 = document.getElementById('joystick2');
var stick2 = document.getElementById('stick2');
var xhr = new XMLHttpRequest();

joystick1.addEventListener('touchstart', function(event) {
    event.preventDefault();
    stick1.style.transition = 'none';
});

joystick1.addEventListener('touchmove', function(event) {
    event.preventDefault();
    var touch = event.touches[0];
    var x = touch.clientX - (joystick1.getBoundingClientRect().left + joystick1.offsetWidth / 2);
    var y = touch.clientY - (joystick1.getBoundingClientRect().top + joystick1.offsetHeight / 2);
    var radius = joystick1.offsetWidth / 2;
    var distance = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    var angle = Math.atan2(y, x);

    if (distance <= radius) {
        var stickX = x + joystick1.offsetWidth / 2;
        var stickY = y + joystick1.offsetHeight / 2;
    } else {
        x = radius * Math.cos(angle);
        y = radius * Math.sin(angle);
        var stickX = radius * Math.cos(angle) + joystick1.offsetWidth / 2;
        var stickY = radius * Math.sin(angle) + joystick1.offsetHeight / 2;
    }

    message = x + ',' + y;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send-message', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('message=' + encodeURIComponent(message));

    stick1.style.left = stickX  + 'px';
    stick1.style.top = stickY + 'px';
});

joystick1.addEventListener('touchend', function(event) {
    event.preventDefault();
    stick1.style.transition = 'all 0.3s ease';
    stick1.style.left = '50%';
    stick1.style.top = '50%';

    message = 0 + ',' + 0;
    xhr.open('POST', '/send-message', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('message=' + encodeURIComponent(message));
});

joystick2.addEventListener('touchstart', function(event) {
    event.preventDefault();
    stick2.style.transition = 'none';
});

joystick2.addEventListener('touchmove', function(event) {
    event.preventDefault();
    var touch = event.touches[0];
    var x = touch.clientX - (joystick2.getBoundingClientRect().left + joystick2.offsetWidth / 2);
    var y = touch.clientY - (joystick2.getBoundingClientRect().top + joystick2.offsetHeight / 2);
    var radius = joystick2.offsetWidth / 2;
    var distance = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    var angle = Math.atan2(y, x);

    message = x + ',' + radius * Math.cos(angle) + ',' + y +',' + radius * Math.sin(angle);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send-message', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('message=' + encodeURIComponent(message));

    if (distance <= radius) {
        var stickX = x + joystick2.offsetWidth / 2;
        var stickY = y + joystick2.offsetHeight / 2;
    } else {
        var stickX = radius * Math.cos(angle) + joystick2.offsetWidth / 2;
        var stickY = radius * Math.sin(angle) + joystick2.offsetHeight / 2;
    }

    stick2.style.left = stickX  + 'px';
    stick2.style.top = stickY + 'px';
});

joystick2.addEventListener('touchend', function(event) {
    event.preventDefault();
    stick2.style.transition = 'all 0.3s ease';
    stick2.style.left = '50%';
    stick2.style.top = '50%';
});