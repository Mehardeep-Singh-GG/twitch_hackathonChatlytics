import time
import socket
import threading
import speech_recognition as sr
from app import twitch_oauth
from openai import OpenAI


# Twitch IRC settings
server = "irc.chat.twitch.tv"
port = 6667
nickname = "meharzz"  # Your Twitch nickname
access_token = "1tcxaoa2xzmxww750qqh6qcivhmnfo"
token = f"oauth:{access_token}"
channel = "#KaiCenat"

# Initialize recognizer
recognizer = sr.Recognizer()

# Lists to store transcriptions and chat messages
transcriptions = []
messages = []

# Variables to hold the latest transcription and chat context
latest_transcription = ""
latest_chat = ""

# Set up Twitch IRC connection
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    irc.connect((server, port))
    print("Connected to Twitch server.")
except Exception as e:
    print("Failed to connect to server:", e)
    exit()

# Authenticate and join channel
irc.send(f"PASS {token}\n".encode("utf-8"))
irc.send(f"NICK {nickname}\n".encode("utf-8"))
irc.send(f"JOIN {channel}\n".encode("utf-8"))
print(f"Joined channel: {channel}")

# Initialize OpenAI client
api_key = "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"
client = OpenAI(api_key=api_key)

def real_time_transcribe():
    """Transcribes microphone audio in real-time and stores in transcriptions."""
    global transcriptions
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Real-time transcription started. Speak now...")

        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                transcriptions.append(text)
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print("Error with the speech recognition service; check your network connection.")

def listen_twitch_chat():
    """Listens for messages from Twitch chat and stores in messages."""
    global messages
    while True:
        try:
            response = irc.recv(2048).decode("utf-8", errors="replace")
            if response.startswith("PING"):
                irc.send("PONG :tmi.twitch.tv\n".encode("utf-8"))
            message = parse_message(response)
            if message:
                messages.append(message)
            if "403" in response:
                print("Error: Cannot join the channel. Check permissions or channel name.")
                break
            elif "Login authentication failed" in response:
                print("Error: Login authentication failed. Check OAuth token.")
                break
        except Exception as e:
            print("Error:", e)
            break

def parse_message(response):
    """Parses Twitch IRC messages to extract chat content."""
    if "PRIVMSG" in response:
        try:
            message = response.split(":", 2)[-1].strip()
            return message
        except IndexError:
            return None
    return None

def combine_and_send_context():
    """Combines and sends transcriptions and chat messages to OpenAI every 10 seconds."""
    global latest_transcription, latest_chat
    while True:
        time.sleep(10)
        if transcriptions or messages:
            latest_transcription = " ".join(transcriptions)
            latest_chat = "\n".join(messages)

            # Prepare and send the combined context to OpenAI
            combined_text = f"Transcription: {latest_transcription}\nChat Messages: {latest_chat}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": combined_text}
                ]
            )

            # Print OpenAI response
            print("\nOpenAI Response:")
            print(response.choices[0].message["content"])

            # Clear lists for the next interval
            transcriptions.clear()
            messages.clear()

# Start threads
threading.Thread(target=real_time_transcribe, daemon=True).start()
threading.Thread(target=listen_twitch_chat, daemon=True).start()
combine_and_send_context()  # Run in main thread for periodic context sending
