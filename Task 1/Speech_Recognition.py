import speech_recognition as sr

def recognize_speech():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
                try:
                        text = recognizer.recognize_google(audio)
                        print(f"Recognized: {text}")
                        return text
                except sr.UnknownValueError:
                        print("Sorry, I did not understand that.")
                except sr.RequestError:
                        print("Could not request results; check your network connection.")