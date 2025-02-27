from googletrans import Translator
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
import requests
import cv2  # OpenCV for image processing
import speech_recognition as sr  # Speech recognition for audio input
import pyttsx3  # Text-to-speech library

def extract_text_from_image(image_url_or_path):
    """Extracts text from an image using Tesseract."""
    if is_valid_url(image_url_or_path):
        # Download the image from the URL
        response = requests.get(image_url_or_path)
        image = response.content

        # Convert the image data to a format readable by Tesseract
        image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    else:
        # Read the image from the file path
        image = cv2.imread(image_url_or_path)

    if image is not None:
        # Extract text from the image
        image_text = pytesseract.image_to_string(image)
        return image_text
    else:
        print("Invalid image URL or file path.")
        return None

def translate_text(text, source_language, target_language):
    """Translates text from the source language to the given target language using Google Translate."""
    translator = Translator()
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text

def translate_speech(target_language):
    """Translates speech to the given target language using Google Speech-to-Text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            recognized_speech = recognizer.recognize_google(audio_data)

            # Detect the source language
            language_detector = Translator()
            source_language = language_detector.detect(recognized_speech).lang

            translation = translate_text(recognized_speech, source_language, target_language)
            print_translation(translation)

        except sr.UnknownValueError:
            print("Could not recognize speech.")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition request failed: {str(e)}")
            return None

def is_valid_url(url):
    """Checks if the given URL is valid."""
    import re
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def print_translation(translation):
    print("Translated text:", translation)
    recite_text(translation)

def recite_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    input_type = input("Enter 'text', 'image', or 'audio' for input: ").lower()
    target_language = input("Enter the target language (e.g., 'fr' for French): ").lower()

    if input_type == "text":
        text = input("Enter the text to translate: ")
        translation = translate_text(text, "en", target_language)  # Assuming English as the source language for text input
        print_translation(translation)
    elif input_type == "image":
        image_url_or_path = input("Enter the image URL or file path: ")

        image_text = extract_text_from_image(image_url_or_path)
        if image_text:
            print("Text extracted from the image:", image_text)
            translation = translate_text(image_text, "en", target_language)  # Assuming English as the source language for image input
            print_translation(translation)
        else:
            print("No text found in the image.")
    elif input_type == "audio":
        translate_speech(target_language)
    else:
        print("Invalid input type.")

if __name__ == "__main__":
    main()