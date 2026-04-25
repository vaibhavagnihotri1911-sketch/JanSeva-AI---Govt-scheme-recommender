import speech_recognition as sr

def get_voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Speak in Hindi or English...")
            
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

            print("Processing...")

            # Google Speech Recognition
            text = recognizer.recognize_google(audio, language="hi-IN")

            print("You said:", text)
            return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except sr.RequestError:
        print("API unavailable")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""