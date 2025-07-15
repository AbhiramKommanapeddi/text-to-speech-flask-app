from flask import Flask, request, send_file, render_template, jsonify
from gtts import gTTS
import os
import uuid # For unique filenames

app = Flask(__name__)

# Directory to save temporary audio files
AUDIO_DIR = 'temp_audio'
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

@app.route('/')
def index():
    # Flask will look for 'index.html' inside the 'templates' folder
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'en') # Get language from frontend, default to 'en'

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Generate a unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    tts_file_path = os.path.join(AUDIO_DIR, f'output_{file_id}.mp3')

    try:
        # Create a gTTS object with the text and language
        tts = gTTS(text=text, lang=lang, slow=False) # slow=False for normal speed

        # Save the speech to a temporary file
        tts.save(tts_file_path)

        # Return the URL to the audio file. The client will then request this URL.
        return jsonify({'audio_url': f'/audio/{file_id}'}), 200

    except Exception as e:
        print(f"Error during TTS conversion: {e}")
        return jsonify({'error': f'Failed to convert text to speech: {str(e)}'}), 500

@app.route('/audio/<file_id>')
def serve_audio(file_id):
    file_path = os.path.join(AUDIO_DIR, f'output_{file_id}.mp3')
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/mpeg', as_attachment=False)
    else:
        return jsonify({'error': 'Audio file not found'}), 404

@app.route('/cleanup', methods=['POST']) # Optional route for cleanup
def cleanup_audio_files():
    for filename in os.listdir(AUDIO_DIR):
        file_path = os.path.join(AUDIO_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")
    return jsonify({'message': 'Temporary audio files cleaned up'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run on port 5000 for development