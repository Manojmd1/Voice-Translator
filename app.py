from flask import Flask, request, render_template, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# About Us page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# E-books page
@app.route('/ebooks')
def ebooks():
    return render_template('ebooks.html')

# Translation endpoint
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    target_lang = data.get('lang', 'hi')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_lang).text

        tts = gTTS(translated, lang=target_lang)
        filename = f"static/audio/{uuid.uuid4()}.mp3"
        tts.save(filename)

        return {
            "translated_text": translated,
            "audio_url": '/' + filename
        }

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs("static/audio", exist_ok=True)
    app.run(debug=True, port=5000)
