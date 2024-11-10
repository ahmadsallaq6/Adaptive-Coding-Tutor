document.addEventListener('DOMContentLoaded', function() {
    // Ensure the Monaco editor is initialized before attempting to use it
    const editorInitInterval = setInterval(() => {
        if (window.editor) {
            // Monaco editor instance is now available
            clearInterval(editorInitInterval);

            // Event listener for sending the challenge request
            document.getElementById('send-message-btn').addEventListener('click', function() {
                const userPrompt = document.getElementById('user-prompt').value;

                if (userPrompt.trim() !== '') {
                    // Send the prompt and chat history to the backend to generate the challenge
                    fetch('/generate-challenge', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            prompt: userPrompt,
                            chat_history: window.chatHistory || []  // Send the existing chat history (if any)
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        const challenge = data.challenge;  // Get the response (challenge) from the backend
                        window.chatHistory = data.chat_history;  // Update the chat history with the new message
                        window.currentQuestion = userPrompt; // Store the current question

                        // Display the challenge in the chat display
                        const chatDisplay = document.getElementById('chat-display');
                        chatDisplay.innerHTML += `<div class="message user-message">${userPrompt}</div>`;
                        chatDisplay.innerHTML += `<br/>`;
                        chatDisplay.innerHTML += `<div class="message bot-response">${challenge}</div>`;
                        chatDisplay.innerHTML += `<br/>`;

                        // Clear the input field after sending
                        document.getElementById('user-prompt').value = '';

                        // Scroll to the bottom of the chat display
                        chatDisplay.scrollTop = chatDisplay.scrollHeight;
                    })
                    .catch(error => {
                        const chatDisplay = document.getElementById('chat-display');
                        chatDisplay.innerHTML += `<div class="chat-message error">Error generating response!</div>`;
                        console.error('Error:', error);
                    });
                }
            });

            // Event listener for submitting the solution
            document.getElementById('submit-btn').addEventListener('click', function() {
                // Get the solution from Monaco editor
                const userSolution = window.editor.getValue();  // Fetch the user's solution
                const currentQuestion = window.currentQuestion; // Get the current question

                if (userSolution.trim() !== '' && currentQuestion) {
                    // Log the solution and question before sending to the backend
                    console.log("User Solution:", userSolution);
                    console.log("Question Prompt:", currentQuestion);

                    // Send the question and solution to the backend for validation
                    fetch('/check-solution', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            question: currentQuestion,
                            solution: userSolution
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        const assessment = data.assessment || 'Incorrect'; // Use 'Incorrect' as a fallback if assessment is undefined
                        const feedbackDisplay = document.getElementById('feedback');

                        // Display feedback about the solution
                        feedbackDisplay.innerHTML = `<p><strong>Assessment: </strong>${assessment}</p>`;

                        // Optional: Add a visual cue to indicate success or failure
                        if (assessment === 'Correct') {
                            feedbackDisplay.style.color = 'green';
                        } else {
                            // If the solution is incorrect, provide the user with options
                            feedbackDisplay.style.color = 'red';
                            feedbackDisplay.innerHTML += `    
                                <div>
                                    <button id="try-again-btn">Try Again</button>
                                    <button id="get-solution-btn">Get Step-by-Step Solution</button>
                                </div>
                            `;

                            // Event listener for "Try Again" button
                            document.getElementById('try-again-btn').addEventListener('click', () => {
                                feedbackDisplay.innerHTML = '';
                            });

                            // Event listener for "Get Step-by-Step Solution" button
                            document.getElementById('get-solution-btn').addEventListener('click', () => {
                                // Send a request to the backend to get the step-by-step solution
                                fetch('/get-solution', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        question: currentQuestion,
                                        solution: userSolution
                                    })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    const stepByStepSolution = data.step_by_step_solution;
                                    feedbackDisplay.innerHTML = `<pre>${stepByStepSolution}</pre>`;
                                })
                                .catch(error => {
                                    feedbackDisplay.innerHTML = `<p class="error">Error getting step-by-step solution.</p>`;
                                    console.error('Error:', error);
                                });
                            });
                        }
                    })
                    .catch(error => {
                        const feedbackDisplay = document.getElementById('feedback');
                        feedbackDisplay.innerHTML = `<p class="error">Error checking solution!</p>`;
                        console.error('Error:', error);
                    });
                } else {
                    alert("Please enter a solution before submitting.");
                }
            });
        }
    }, 100); // Check every 100ms until the editor is available
});