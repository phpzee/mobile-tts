from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import uuid

app = Flask(__name__)
CORS(app)  # <-- Add this line to allow browser requests

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    lang = data.get('lang', 'hi')
    speed = float(data.get('speed', 1.0))

    if not text:
        return jsonify({'error':'No text provided'}), 400

    filename = f"{uuid.uuid4()}.mp3"
    try:
        tts = gTTS(text=text, lang=lang, slow=(speed<0.9))
        tts.save(filename)
        return send_file(filename, mimetype='audio/mpeg', as_attachment=True, download_name='speech.mp3')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
