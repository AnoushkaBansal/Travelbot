function appendMessage(who, text) {
    const chatWindow = document.getElementById('chatWindow');
    const messageElement = document.createElement('div');

    // This assumes all text is safe to render as HTML. Be cautious if 'text' can include user-generated content.
    // Proper sanitization is necessary to prevent XSS attacks in such cases.
    let content = '';
    if (typeof text === 'object' && text !== null && Array.isArray(text)) {
        // If 'text' is an array of objects, format accordingly.
        const formattedText = text.map(item => {
            // Modify this line based on the actual structure of your objects.
            return `Mode: ${item.mode_of_transport}, Provider: ${item.provider}, Price: ${item.price}`;
        }).join('<br>'); // Join each item with a line break for display.
        content = `${who}: ${formattedText}`;
    } else {
        // For string messages, including those with HTML, directly assign them.
        content = `${who}: ${text}`;
    }
    if (who === 'You') {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }

    // Use 'innerHTML' to ensure that HTML tags are rendered.
    messageElement.innerHTML = content;

    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom.
}



function sendMessage() {
    const inputElement = document.getElementById('userInput');
    const userText = inputElement.value.trim();

    if (userText === '') {
        alert('Please type a query.');
        return;
    }

    appendMessage('You', userText);
    inputElement.value = ''; // Clear input after sending

    // Example of sending userText to your server and handling the response
    fetch('/process_query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userText }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            // Directly display the message from the server
            appendMessage('Bot', data.message);
        } else {
            // If there's no message, proceed with formatting the data as before
            const formattedText = formatResponse(data);
            if (formattedText) {
                appendMessage('Bot', formattedText);
            } else {
                appendMessage('Bot', 'Sorry, I couldn\'t find any information.');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('Bot', 'Sorry, something went wrong.');
    });
}

function formatResponse(data) {

    if ('general_intent' in data) {
       
        return `Bot: ${data.general_intent}`; 
    }
    Object.keys(data).forEach(key => {
        data[key].forEach(item => {
            switch(key) {
                case 'accommodations':
                    formattedText += `🏨 <b>${item.name}</b> located in ${item.location}. The price range category is ${item.price}  and has a rating of ${item.rating}.<br>`;
                    break;
                case 'local_transport':
                    formattedText += `🚌 For getting around, you can use <b>${item.type}</b> on the ${item.route_name} route. It costs $${item.price} and operates from ${item.operating_hours}.<br>`;
                    break;
                case 'points_of_interest':
                    formattedText += `📍 Check out <b>${item.name}</b> in ${item.location}. It's a ${item.type} with an entry fee of $${item.entry_fee} and is open ${item.operating_hours}.<br>`;
                    break;
                case 'transport_options':
                    formattedText += `✈️ For travel, consider <b>${item.mode_of_transport}</b> from ${item.provider}. Tickets start at $${item.price}, departing at ${item.departure_time} and it'll take about ${item.duration}.<br>`;
                    break;


           
            }
        });
    });

    if (!formattedText) {
        formattedText = "I couldn't find anything matching your query. Could you try rephrasing it?";
    }

    return formattedText;
}

