# Adaptive Coding Tutor

The **Adaptive Coding Tutor** is an AI-powered platform designed to help users improve their coding skills through interactive, challenge-based learning. Users can engage with a Large Language Model (LLM) to request coding challenges, solve them in a code editor, and receive feedback in real time.

## Features

- **Coding Challenges**: Users can request coding challenges directly from the website.
- **Interactive Code Editor**: Users solve challenges in a built-in code editor and submit their solutions.
- **Automated Code Evaluation**: The LLM assesses the submitted code and provides feedback:
  - **Correct**: If the solution is correct, the user is notified of their success.
  - **Incorrect**: If the solution is incorrect, the user can either:
    - **Try Again**: Resubmit a revised solution.
    - **Step-by-Step Solution**: Request a step-by-step explanation to learn the correct approach.
- **User Interface**: The platform includes a chat interface with user responses in blue and bot responses in gray.

## Demo

*Include screenshots or a GIF demonstrating the flow of using the Adaptive Coding Tutor.*

## Usage

1. **Login**: Start by logging into the platform (optional depending on project setup).
2. **Request a Challenge**: Initiate a chat with the tutor to receive a coding challenge.
3. **Solve the Challenge**: Type your code solution in the editor and submit.
4. **Get Feedback**: Receive feedback on your solution and proceed as desired:
   - **Correct**: Move to the next challenge.
   - **Incorrect**: Choose to either try again or get a step-by-step solution.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask 
- **AI Model**: Gemini 1.5 Flash

## Project Structure

adaptive-coding-tutor/ 

    ├── backend/ 
      ├── app.py # Main application file
      ├── templates/ 
      │ ├── index.html # Main chat interface 
      ├── static/ 
        │ ├── style.css
        │ ├── script.js
        │ └── editor.js  




