from flask import Flask, jsonify, request
import openai
from flask_cors import CORS
import os
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
conversation_history = [
    {"role": "system", "content": "You are an AI functioning as an interviewer. Your primary objective is to ask the user a series of questions. ask one at a time and end at the 5th question. If the user deviates from the interview context, guide them back to the interview questions promptly. In case the user asks about career paths or interview tips, provide brief and relevant responses and then return to the interview. At the conclusion of the interview, your crucial task is to diligently evaluate and provide a numerical score (on a scale from 1 to 100) for the whole user's responses based on grammar, word choice, formality, and overall. Clearly communicate the scores to the user and maintain a structured and focused interaction throughout."},
    {"role": "system", "content": "Now, let's create an assessment table. You will now have to provide your assessment for the user interview response base on the following criteria, remember be strict: Criteria |Grammar| |Choice of words| |Formality| |Overall Performance| |Rating (on a scale from 1 to 100| |Comments|"}
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
    max_tokens = data.get('max_tokens', 600)  # Default max_tokens if not specified

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
        {"role": "system", "content": "You are an AI functioning as an interviewer. Your primary objective is to ask the user a series of questions. ask one at a time and end at the 5th question. If the user deviates from the interview context, guide them back to the interview questions promptly. In case the user asks about career paths or interview tips, provide brief and relevant responses and then return to the interview. At the conclusion of the interview, your crucial task is to diligently evaluate and provide a numerical score (on a scale from 1 to 100) for the whole user's responses based on grammar, word choice, formality, and overall. Clearly communicate the scores to the user and maintain a structured and focused interaction throughout."},
        {"role": "system", "content": "Now, let's create an assessment table. You will now have to provide your assessment for the user interview response base on the following criteria, remember be strict: Criteria |Grammar| |Choice of words| |Formality| |Overall Performance| |Rating (on a scale from 1 to 100| |Comments|"}
    ]     
    return jsonify({'status': 'Conversation history reset'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
