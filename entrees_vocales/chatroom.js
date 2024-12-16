const messagesDiv = document.getElementById('messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const voiceButton = document.getElementById('voice-button');
    
    function addMessage(sender, text) {
      const messageElement = document.createElement('div');
      messageElement.textContent = `${sender}: ${text}`;
      messagesDiv.appendChild(messageElement);
      messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll
    }

    function sendMessage() {
      const message = chatInput.value.trim();
      if (message) {
        addMessage('You', message);
        socket.emit('user_uttered', {
            "message": message,
          });
        chatInput.value = '';
      }
    }

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') sendMessage();
    });

    // Check if the browser supports SpeechRecognition
    const socket = io("http://localhost:5005");
    socket.on('connect', function () {
        console.log("Connected to Socket.io server");
    });
    socket.on('connect_error', (error) => {
        // Write any connection errors to the console 
        console.error(error);
    });
    socket.on('bot_uttered', function (response) {
        console.log("Bot uttered:", response);
        addMessage("Bot", response["text"])
    });

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
      console.log("SpeechRecognition is supported in your browser!");

      // Create a new instance of SpeechRecognition
      const recognition = new SpeechRecognition();

      // Configure the SpeechRecognition instance
      recognition.lang = 'fr-FR';
      recognition.interimResults = false; // Return only final results
      recognition.continuous = false; // Stop after a single recognition session

      // Start listening when the user clicks a button
      voiceButton.addEventListener("click", () => {
        recognition.start();
        console.log("Listening...");
      });

      // Handle the result event
      recognition.addEventListener("result", (event) => {
        const transcript = event.results[0][0].transcript; // Get the transcript of the first result
        console.log("You said:", transcript);
        addMessage("You", transcript)

        // api test
        fetch("http://127.0.0.1:5005/model/parse?token=thisismysecret", {
          method: "POST",
          body: JSON.stringify({
            text: transcript,
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS"
          }
        })
          .then((response) => response.json().then((data) => {
            console.log(data);
          }).catch((err) =>  {
            console.log(err)
          }))

          // message sent to socket
          socket.emit('user_uttered', {
            "message": transcript,
          });
      });

      // Handle the end event (optional)
      recognition.addEventListener("end", () => {
        console.log("Speech recognition ended.");
      });

      // Handle errors
      recognition.addEventListener("error", (event) => {
        console.error("Error occurred in speech recognition:", event.error);
      });
    } else {
      console.error("SpeechRecognition is not supported in your browser.");
    }