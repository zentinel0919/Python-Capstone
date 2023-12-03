from flask import Flask, jsonify, request
import openai
from flask_cors import CORS
import os
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
conversation_history = [
    {"role": "system", "content": "You are an AI acting as an interviewer. You will ask the user a series of interview questions, it should be strictly maximum of 5 questions and after that end the conversation, then score and evaluate the user's response by grammar, choice of words, and formality of the user's answer. Make sure to ask 1 question at a time only. If the user say something outside the interview, say something then continue the interview but if the user ask about career paths or interview tips, answer it then continue the interview"}
]

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY', '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')

@app.route('/openai', methods=['POST'])
def call_openai():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    
    conversation_history.append({"role": "user", "content": data.get('prompt', '')})
    engine = data.get('engine', 'gpt-3.5-turbo')  # Use the correct engine identifier
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 400)  # Default max_tokens if not specified

    try:
        response = openai.ChatCompletion.create(
            model=engine,  # Use 'model' instead of 'engine' for chat completions
            messages=conversation_history,
            max_tokens=max_tokens
        )
        app.logger.debug(f"OpenAI response: {response}")
        conversation_history.append(response['choices'][0]['message'])
        return jsonify(response)
    except openai.error.InvalidRequestError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/reset_conversation', methods=['GET'])
def reset_conversation():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": "You are an AI acting as an interviewer. You will ask the user a series of interview questions, it should be strictly maximum of 5 questions and after that end the conversation by scoring the grammar, choice of words, and formality of the user's answer per question. Make sure to ask 1 question at a time only. If the user say something outside the interview, say something to continue the interview"}
    ]
    return jsonify({'status': 'Conversation history reset'})



if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode for production
