#Firts install the neccessary modules.
#Developing a language translator

import os
from deep_translator import GoogleTranslator
import speech_recognition as sr

# Function to translate text
def translate_text(text, dest_language):
    try:
        translator = GoogleTranslator(source='auto', target=dest_language)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        return f"Error: {str(e)}"

# Function to recognize speech and convert it to text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Main function to run the translator
def main():
    print("Welcome to the AI-based Language Translator!")
    mode = input("Choose mode: (1) Text Translation (2) Speech Translation: ")

    if mode == '1':
        text = input("Enter the text to translate: ")
        dest_language = input("Enter the destination language code (e.g., 'es' for Spanish): ")
        translated_text = translate_text(text, dest_language)
        print(f"Translated Text: {translated_text}")

    elif mode == '2':
        dest_language = input("Enter the destination language code (e.g., 'es' for Spanish): ")
        spoken_text = recognize_speech()
        if "Error" not in spoken_text:
            translated_text = translate_text(spoken_text, dest_language)
            print(f"Translated Text: {translated_text}")
        else:
            print(spoken_text)

    else:
        print("Invalid mode selected. Please choose 1 or 2.")

if __name__ == "__main__":
    main()



"""
    When prompted, choose the mode of translation:
        1. Text Translation: Enter the text you want to translate and the destination language code (e.g., 'es' for Spanish).
        2. Speech Translation: Speak into your microphone, and the program will convert your speech to text and then translate it.
"""


