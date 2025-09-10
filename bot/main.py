import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
from elevenlabs import play, stream, ElevenLabs

# Set up Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up ElevenLabs client with the API key
eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

# Initialize speech recognition engine
r = sr.Recognizer()

# Function to get a response from Gemini
def get_response(prompt):
    if not prompt:
        return ""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "I'm sorry, I couldn't get a response right now."

# New function to speak the response using ElevenLabs
def speak(text, voice_id="dRtOp8kfRuFIbDKMu38H"):
    try:
        audio_stream = eleven_client.text_to_speech.stream(
            text=text,
            voice_id=voice_id
        )
        stream(audio_stream)
    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")

# The main loop remains the same
def main_loop():
    print("AI Voice Assistant is running. Say 'goodbye' to exit.")
    while True:
        command = listen()
        if "goodbye" in command.lower():
            speak("Goodbye!")
            break
        
        response = get_response(command)
        speak(response, voice_id="dRtOp8kfRuFIbDKMu38H")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

if __name__ == "__main__":
    main_loop()