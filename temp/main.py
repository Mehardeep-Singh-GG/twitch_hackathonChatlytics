from app import twitch_oauth


access_token = twitch_oauth.get_access_token()
ACCESS_TOKEN = access_token
print(ACCESS_TOKEN)
ACCESS_TOKEN = "1tcxaoa2xzmxww750qqh6qcivhmnfo"
import speech_recognition as sr
import socket
import time
import threading

# Twitch IRC settings
server = "irc.chat.twitch.tv"
port = 6667
nickname = "meharzz"  # Your Twitch nickname
token = f"oauth:{ACCESS_TOKEN}"  # Your OAuth token
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


def real_time_transcribe():
    """Transcribes microphone audio in real-time and stores in transcriptions."""
    global transcriptions
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Real-time transcription started. Speak now...")

        while True:
            try:
                # Capture audio
                audio = recognizer.listen(source)
                # Transcribe audio
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
            # Respond to PING to stay connected
            if response.startswith("PING"):
                irc.send("PONG :tmi.twitch.tv\n".encode("utf-8"))
            # Parse chat messages
            print(response)
            message = parse_message(response)
            print(message)
            if message:
                messages.append(message)
            # Check for errors
            if "403" in response:
                print("Error: Cannot join the channel. Check permissions or channel name.")
                break
            elif "Login authentication failed" in response:
                print("Error: Login authentication failed. Check OAuth token.")
                break
        except UnicodeDecodeError as e:
            print("Decoding error:", e)
            continue
        except KeyboardInterrupt:
            print("Disconnecting...")
            irc.send(f"PART {channel}\n".encode("utf-8"))
            irc.close()
            break
        except Exception as e:
            print("Error:", e)
            break


def parse_message(response):
    """Parses Twitch IRC messages to extract chat content."""
    if "PRIVMSG" in response:
        try:
            # Extract message by finding the last colon in the line
            message = response.split(":", 2)[-1].strip()
            return message
        except IndexError:
            return None
    return None


def combine_context():
    """Combines and stores transcriptions and chat messages every 10 seconds."""
    global latest_transcription, latest_chat
    while True:
        time.sleep(10)  # 10-second interval
        if transcriptions or messages:
            # Combine transcriptions and messages
            latest_transcription = " ".join(transcriptions)
            latest_chat = "\n".join(messages)

            # Output for debugging or checking purposes
            print("\nUpdated Context for last 10 seconds:")
            print(f"Latest Transcription: {latest_transcription}")
            print(f"Latest Chat:\n{latest_chat}")

            # Clear lists for the next interval
            transcriptions.clear()
            messages.clear()


# Start threads for transcription, chat listening, and context combination
threading.Thread(target=real_time_transcribe, daemon=True).start()
threading.Thread(target=listen_twitch_chat, daemon=True).start()
combine_context()  # Run in main thread to manage periodic output

from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
