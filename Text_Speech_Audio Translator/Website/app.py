from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import pytesseract
import speech_recognition as sr
from PIL import Image
import io

app = Flask(__name__, template_folder='templates', static_folder='static')

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_text', methods=['POST'])
def translate_text():
    if request.method == 'POST':
        input_type = request.form['input_type']

        if input_type == 'text':
            text = request.form['text_input']
        elif input_type == 'image':
            image_file = request.files['image_file']
            if image_file:
                # Open the image using PIL
                image = Image.open(io.BytesIO(image_file.read()))
                text = pytesseract.image_to_string(image)
        elif input_type == 'audio':
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                text = "Could not recognize speech."

        if not text:
            return 'Input is empty.'

        source_language = translator.detect(text).lang
        target_language = request.form['target_language']
        translated_text = translator.translate(text, src=source_language, dest=target_language).text

        translated_text = translator.translate(text, src=source_language, dest=target_language).text

        return render_template('index.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
