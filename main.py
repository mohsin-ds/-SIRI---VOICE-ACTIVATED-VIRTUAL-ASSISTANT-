import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import requests
import g4f  # free AI

recognizer = sr.Recognizer()
newsapi = "b48768b7ef31464789eaca9837435fb9"

# ---------------- Speak Function ----------------
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech error:", e)

# ---------------- AI Function ----------------
def aiProcess(command):
    try:
        output = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": command}]
        )
        return str(output)
    except Exception as e:
        return f"AI error: {e}"

# ---------------- Command Handler ----------------
def processCommand(c):
    c = c.lower()

    if "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found in library")

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:  # read top 5
                speak(article['title'])

    elif "stop" in c:
        speak("Goodbye")
        exit(0)

    else:
        output = aiProcess(c)
        print("AI Response:", output)
        speak(output)

# ---------------- Main Loop ----------------
if __name__ == "__main__":
    speak("Initializing Siri....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if "siri" in word.lower():
                speak("Yes, I am listening.")

                with sr.Microphone() as source:
                    print("Siri Active... Listening for command.")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"API error: {e}")
        except Exception as e:
            print(f"Error: {e}")
