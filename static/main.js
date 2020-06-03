document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    const socket = io();

    // When connected notify server, configure buttons
    socket.on('connect', () => {

        // Notify server that user joined this channel
        socket.emit('joined');

        // Notify server when user leaves channel
        document.querySelector('#leave').onclick = () => {
            console.log('left');
            socket.emit('leave');
        };

        // Send button is disabled by default
        document.querySelector('#send').disabled = true;

        // Enable button only if there is text in the input field
        document.querySelector('#message').onkeyup = () => {
            if (document.querySelector('#message').value =='') {
                document.querySelector('#send').disabled = true;
            } else {
                document.querySelector('#send').disabled = false;
            }
        };

        // Send button should emit a "send message" event
        var send = document.querySelector('#send');
        send.onclick = () => {
 
            const message = document.querySelector('#message').value;
            send.disabled = true;
            socket.emit('send message', {'message': message});
        };

        // Hit ENTER to send message

        var input_field = document.querySelector('#message');

        input_field.addEventListener('keydown', event => {
            if (event.key == 'Enter' && input_field.value.length > 0) {
                document.getElementById('send').onclick();

            }
        });

        // Delete button emits a "delete message" event

        var delete_btns = document.querySelectorAll('.delete_message');

        if (delete_btns != null) {
            delete_btns.forEach(function(button) {
                button.onclick = () => {
                    const message_id = button.getAttribute('data-message-id');
                    socket.emit('delete message',{'message_id': message_id});
                };
            });
        }

        // Focus on the bottom of the page
        var element = document.getElementById('messages');
        element.scrollTop = element.scrollHeight;
    });

    // When a new message is announced, add it to chat window
    socket.on('announce message', data => {

        console.log(data['message'])
    
        const message = document.createElement('div');
        message.className = 'message_container';
        message.setAttribute('id', data['message']['id']);

        const username = document.createElement('span');
        username.className = 'username';
        username.innerHTML = data['message']['username'];

        const message_text = document.createElement('p');
        message_text.className = 'message_text';
        message_text.innerHTML = data['message']['message_text'];

        const time = document.createElement('span');
        time.className = 'time_stamp';
        time.innerHTML = data['message']['time'];

        const delete_btn = document.createElement('button');
        delete_btn.className = 'delete_message';
        delete_btn.innerHTML = 'DELETE';
        delete_btn.setAttribute('data-message-id', data['message']['id']);

        // Add delete function
        delete_btn.onclick = function() {
            const message_id = delete_btn.getAttribute('data-message-id');
            socket.emit('delete message',{'message_id': message_id});
        }; 
        
        message.appendChild(username);
        message.appendChild(delete_btn);
        message.appendChild(message_text);
        message.appendChild(time);

        document.querySelector('#messages').append(message);

         // Clear input field
        document.querySelector('#message').value = '';

        // Automatically scroll to the bottom of chat
        var element = document.getElementById('messages');
        element.scrollTop = element.scrollHeight;
    
    });

    // Error when someone tries to delete other's messages
    socket.on('user cant delete message', data => {
        alert ("You can't delete other's messages");
    });
    

    // When a message is deleted
    socket.on('deleted message', data => {

        var message_id = data.message_id;
        element = document.querySelector('#' + CSS.escape(message_id));
        element.parentNode.removeChild(element);
        
    });
});