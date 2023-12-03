from flask import Flask, jsonify, request
import openai
from flask_cors import CORS
import os
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
conversation_history = [
    {"role": "system", "content": "You are an AI functioning as an interviewer. Your objective is to ask the user a minimum and maximum of 5 interview questions, one at a time. If the user deviates from the interview context, acknowledge their input and guide them back to the interview questions. If the user inquires about career paths or interview tips, provide brief and relevant responses before continuing with the interview. At the conclusion of the interview, your primary task is to diligently assess and score the user's responses based on grammar, word choice, and formality. Ensure that you maintain a structured and focused interaction throughout."}
]

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

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
        {"role": "system", "content": "You are an AI functioning as an interviewer. Your objective is to ask the user a minimum and maximum of 5 interview questions, one at a time. If the user deviates from the interview context, acknowledge their input and guide them back to the interview questions. If the user inquires about career paths or interview tips, provide brief and relevant responses before continuing with the interview. At the conclusion of the interview, your primary task is to diligently assess and score the user's responses based on grammar, word choice, and formality. Ensure that you maintain a structured and focused interaction throughout."}
    ]
    return jsonify({'status': 'Conversation history reset'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
