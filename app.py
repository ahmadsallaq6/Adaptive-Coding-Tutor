import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session
import re

#this is the right one

# Configure the Gemini API with your API key
genai.configure(api_key='your_gemini_api_key')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '12345'  # Set a secret key for session management

# Set the generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="act as a coding instructor, generate coding challenges that help users progressively improve their coding skills. Each challenge should focus on a specific concept, technique, or algorithm. After the user submits their solution, assess the code for correctness, efficiency, and clarity, offering constructive feedback. Provide hints or tips when necessary, and encourage users to explore multiple solutions. Tailor the difficulty of challenges based on the user’s skill level and learning objectives, ensuring they build a strong foundation in coding and never provide the solution with the challenge only give hints",
)

# Route to serve the frontend files
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-challenge', methods=['POST'])
def generate_challenge():
    try:
        user_prompt = request.json.get('prompt')

        if not user_prompt:
            raise ValueError("No prompt provided")

        # Add additional instruction to the user prompt
        additional_instruction = (
        )

        # Append the additional instruction to the user prompt
        user_prompt = f"{user_prompt}\n\n{additional_instruction}"

        # Simulate getting a response from the model (you would call the LLM here)
        chat_session = model.start_chat(history=[])  # Empty history
        response = chat_session.send_message(user_prompt)

        if not response or not response.text:
            raise ValueError("Invalid response from model")

        challenge = response.text.strip()  # Extract challenge text

        # Clean and format the challenge output
        challenge = format_challenge_output(challenge)

        # Return challenge without session history
        return jsonify({'challenge': challenge})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in generate-challenge: {str(e)}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500




def format_challenge_output(challenge_text):
    # Convert markdown bold (**) to HTML <strong> tags
    challenge_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", challenge_text)

    # Convert single * into bullet points <ul> <li> tags
    challenge_text = re.sub(r"^\* (.*)", r"<ul><li>\1</li></ul>", challenge_text, flags=re.MULTILINE)

    # Convert ## to main title (e.g., h2)
    challenge_text = re.sub(r"^## (.*)", r"<h2>\1</h2>", challenge_text, flags=re.MULTILINE)

    # Insert newlines before certain keywords to break up the text
    keywords = ["Understand the `print()` Function:", "Correct the Code:", "Explanation:", "Let's Test it!",
                "Important Note:", "Let's try another challenge!"]
    for keyword in keywords:
        challenge_text = re.sub(rf"\b{keyword}\b", f"\n\n{keyword}", challenge_text)

    # Split by lines and remove excess whitespace
    lines = challenge_text.split("\n")
    formatted_output = []

    for line in lines:
        if line.strip():  # Ignore empty lines
            formatted_output.append(line.strip())

    # Join the formatted content with <br> tags for HTML line breaks
    return "<br>".join(formatted_output)  # Use <br> tags for HTML line breaks


@app.route('/check-solution', methods=['POST'])
def check_solution():
    try:
        # Get the question and solution from the request
        data = request.json
        question = data.get('question')
        solution = data.get('solution')

        if not question or not solution:
            raise ValueError("Missing question or solution")

        # Logic to check the solution (you can add a real validation here)
        assessment = validate_solution(question, solution)

        # Return the feedback as JSON
        return jsonify({'assessment': assessment})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in check_solution: {str(e)}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

def validate_solution(question, solution):
    # Create a prompt for the model to evaluate the solution
    prompt = f"Question:\n{question}\nSolution:\n{solution}\nTask:\nEvaluate whether the provided solution is correct, considering that it should produce the correct output as expected. If the solution produces the right output, respond with 'Correct'. If the solution is incorrect or does not produce the correct output, respond with 'Wrong'. Additionally, provide your own solution to the question and again only say 'Wrong' or 'Correct' dont add anymore words."

    # Initialize a chat session with the model
    chat_session = model.start_chat(history=[])

    print(solution)
    print(question)
    # Get the model's response to the prompt
    response = chat_session.send_message(prompt)

    print(response)

    # Check and clean up the response text
    if response and response.text:
        assessment = response.text.strip()

        print("the result is: ", assessment)
        # Ensure output is either 'Correct' or 'Incorrect'
        if 'correct' in assessment.lower():
            return "Correct"
        else:
            return "Incorrect"
    else:
        # Fallback in case of an unexpected response
        return "Could not assess solution."

@app.route('/get-solution', methods=['POST'])
def get_solution():
    try:
        # Get the question and solution from the request
        data = request.json
        question = data.get('question')
        solution = data.get('solution')

        if not question:
            raise ValueError("Missing question")

        # Construct a prompt to request a step-by-step solution from the model
        prompt = f"This is the question:\n{question}\n\nThe user attempted this solution:\n{solution}\n\nPlease provide a step-by-step solution to solve the problem correctly. dont say im absolutely right you are tutoring the user and dont forget to add the solution to the question and before giving the solution tell the user where is the error."

        # Initialize a chat session with the model
        chat_session = model.start_chat(history=[])

        # Get the model's response to the prompt
        response = chat_session.send_message(prompt)

        if response and response.text:
            step_by_step_solution = response.text.strip()
        else:
            step_by_step_solution = "Could not generate a step-by-step solution."

        # Return the step-by-step solution as JSON
        return jsonify({'step_by_step_solution': format_challenge_output(step_by_step_solution)})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_solution: {str(e)}")
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)