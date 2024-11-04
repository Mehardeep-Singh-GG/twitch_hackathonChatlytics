import ast

import speech_recognition as sr
import socket
import time
import threading
import os

import json

import google.generativeai as genai
import re
# Initialize OpenAI client (replace with environment variable or secure method)
# from app import twitch_oauth
#
#
# access_token = twitch_oauth.get_access_token()
# ACCESS_TOKEN = access_token
# print(ACCESS_TOKEN)

# Twitch IRC settings
server = "irc.chat.twitch.tv"
port = 6667
nickname = "meharzz"  # Your Twitch nickname
token = "oauth:8jtlevv30jt95o08qw10hjuuzoi6hu"  # Your OAuth token
channel = "#KaiCenat"

# Initialize recognizer
recognizer = sr.Recognizer()

# Lists to store transcriptions and chat messages
transcriptions = []
messages = []

# Variables to hold the latest transcription and chat context
latest_transcription = ""
latest_chat = ""

import requests

# Replace with your own Client ID and OAuth token
client_id = 'blsc7q9tyyit2ey3hcd6gzhn4w24ms'
access_token = '8jtlevv30jt95o08qw10hjuuzoi6hu'


# Function to get all live streams


# Function to get all live streams
def get_streams_data():
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'first': 100  # Maximum results per request
    }

    streams_data = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json()['message']}")
            break

        data = response.json().get('data', [])
        streams_data.extend(data)

        # Check for pagination to get the next page of data
        pagination = response.json().get('pagination', {})
        if 'cursor' in pagination:
            params['after'] = pagination['cursor']
        else:
            break  # No more pages

    return streams_data


# Function to get additional user details
def get_user_data(user_ids):

    url = 'https://api.twitch.tv/helix/users'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    user_data = []
    for user_id in user_ids:
        params = {'id': user_id}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            user_data.extend(response.json().get('data', []))

    return user_data


# Function to get game details
def get_game_data(game_ids):
    url = 'https://api.twitch.tv/helix/games'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    game_data = []
    for game_id in game_ids:
        params = {'id': game_id}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            game_data.extend(response.json().get('data', []))

    return game_data


# Fetch stream data
streams = get_streams_data()

# Extract unique user and game IDs
user_ids = list({stream['user_id'] for stream in streams})
game_ids = list({stream['game_id'] for stream in streams})

# Fetch user and game data
users = get_user_data(user_ids)
games = get_game_data(game_ids)

# Map user and game data for easier access
user_map = {user['id']: user for user in users}
game_map = {game['id']: game for game in games}

# Save data to a text file
with open('stream_data.txt', 'w', encoding='utf-8') as file:
    for stream in streams:
        user = user_map.get(stream['user_id'], {})
        game = game_map.get(stream['game_id'], {})

        # Prepare data for each stream
        stream_info = (
                f"Streamer: {user.get('display_name', 'N/A')}\n"
                f"Title: {stream['title']}\n"
                f"Viewers: {stream['viewer_count']}\n"
                f"Game: {game.get('name', 'N/A')}\n"
                f"Description: {user.get('description', 'N/A')}\n"
                f"Stream Thumbnail: {stream['thumbnail_url']}\n"
                "-" * 50 + "\n"
        )

        # Write data to file
        file.write(stream_info)

print("Stream data saved to stream_data.txt")

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
            message = parse_message(response)
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

import re
import json

def summary(transcription, chat):
    genai.configure(api_key="AIzaSyAGt_AHHj4dyhAJTN7h1BiBE8b92_wUVA8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Create a summary based on this chat and trancription in key points try to make it short"
                                      f"Here is the latest context:\n\nTranscription:\n{transcription}\n\nChat:\n{chat}\n\nCreate a summary based on this chat and trancription in key points try to make it short")
    print(response.text)
    with open("summary.txt", "a") as file:
        file.write(response.text)
    paragraph_text = (response.text)
    fig_text, ax_text = plt.subplots(figsize=(172 / 96, 306 / 96), dpi=96)
    fig_text.patch.set_facecolor('#D9D9D9')
    fig_text.patch.set_alpha(0.0)  # Transparent figure background
    ax_text.axis('off')
    ax_text.text(
        0.5, 0.5, paragraph_text,
        ha='center', va='center',
        color="#333333",
        wrap=True, fontsize=8,
        fontweight='medium',
        family="Arial",
        bbox=dict(facecolor="white", edgecolor="lightgrey", boxstyle="round,pad=0.5")
    )

    # Embedding the text box in Tkinter
    text_canvas = FigureCanvasTkAgg(fig_text, master=window)
    text_canvas.get_tk_widget().place(x=789, y=171)


def pie_chart(transcription, chat):
    genai.configure(api_key="AIzaSyAGt_AHHj4dyhAJTN7h1BiBE8b92_wUVA8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Map out the opinion of the people are they in favour or in not[its just a map to find like how many people are liking it and how many are not like a happiness score just do it] if you dont find it possible still give many things are depended upon it in percentage of 100 give output in a a python list with integers remeber no variable name should be given in the python script just the list ok two entries the people in favour and not in favour with no list"
        f"Here is the latest context:\n\nTranscription:\n{transcription}\n\nChat:\n{chat}\n\nMap out the opinion of the people just give the  python list like the in code and nothing else this response will be further used in code")
    print(response.text)
    print("done_pie")
    code_blocks = re.findall(r'```python\n(.*?)\n```', response.text, flags=re.DOTALL)
    import ast
    print(code_blocks)
    # Original string representation of a list
    list_str = code_blocks[0]


    actual_list = ast.literal_eval(list_str)
    print("here")
    sizes = actual_list  # Adjust these values as needed

    # Set up Matplotlib figure for pie chart
    fig_pie, ax_pie = plt.subplots(figsize=(252 / 96, 235 / 96), dpi=96)
    fig_pie.patch.set_alpha(0.0)  # Make figure background transparent

    # Set background color for the axes
    ax_pie.set_facecolor('#D9D9D9')  # Set the axes background color to #D9D9D9

    # Creating the pie chart
    ax_pie.pie(sizes, labels=None, colors=['green', 'red'], autopct='%1.1f%%', startangle=90, shadow=True)

    # Hide the axes for a clean look
    ax_pie.axis('off')  # Turn off the axis
    ax_pie.set(aspect="equal")  # Equal aspect ratio ensures that pie is drawn as a circle
    ax_pie.set_title(label="Opinion")
    # Embedding the pie chart in Tkinter
    pie_canvas = FigureCanvasTkAgg(fig_pie, master=window)
    pie_canvas.get_tk_widget().place(x=416, y=76)
    # Print or handle the response from ChatGPT as needed

def bar_graph(transcription, chat):
    genai.configure(api_key="AIzaSyAGt_AHHj4dyhAJTN7h1BiBE8b92_wUVA8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        "Map out the mood of the people in the chat in this way: out of ten keys being the mood and value being the percentage out of 10(make sure its an integer) in the python output you give just give the dict with no variables'    Happy: 8,   Sad: 4,   Excited: 6,  Calm: 7   Angry: 3' just with 5 keys"
        f"here is the chat Here is the latest context:\n\nTranscription:\n{transcription}\n\nChat:\n{chat}\n\n please dont add anything extra in it many further codes are linked to it")
    code_blocks = re.findall(r'```python\n(.*?)\n```', response.text, flags=re.DOTALL)
    h = code_blocks[0]
    mood_data = ast.literal_eval(h)
    fig, ax = plt.subplots(figsize=(235 / 96, 312 / 96), dpi=96)
    fig.patch.set_facecolor('#D9D9D9')
    fig.patch.set_alpha(0.0)  # Transparent figure background

    # Plotting the bar chart
    x_labels = list(mood_data.keys())
    y_values = list(mood_data.values())
    print("done_bar")
    bars = ax.bar(x_labels, y_values, color="#453EFF", alpha=0.7)
    ax.set_ylim(0, 10)
    ax.set_facecolor('#D9D9D9')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.grid(visible=True, color='white', linestyle='--', linewidth=0.5)

    # Adding labels to bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.2, int(yval), ha='center', va='bottom', color="#333333")

    # Embedding the Matplotlib figure in Tkinter
    bar_canvas = FigureCanvasTkAgg(fig, master=window)
    bar_canvas.get_tk_widget().place(x=52, y=171)

def radar_map(transcription, chat):
    genai.configure(api_key="AIzaSyAGt_AHHj4dyhAJTN7h1BiBE8b92_wUVA8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        "Map out the 5 most imporatant topics being talked about in the chat in this way: out of ten keys being the topicd and value being the percentage out of 10(make sure its an integer) in the python output you give just give the dict with no variables'    Happy: 8,   Sad: 4,   Excited: 6,  Calm: 7   Angry: 3' just with 5 keys"
        f"here is the chat Here is the latest context:\n\nTranscription:\n{transcription}\n\nChat:\n{chat}\n\n please dont add anything extra in it many further codes are linked to it")

    code_blocks = re.findall(r'```python\n(.*?)\n```', response.text, flags=re.DOTALL)
    h = code_blocks[0]
    data = ast.literal_eval(h)

    import numpy as np
    print("done_radar")
    # Sample data dictionary for the radar chart

    # Preparing data for the radar chart
    labels = list(data.keys())
    values = list(data.values())
    values += values[:1]  # Close the loop by repeating the first value at the end

    # Number of variables
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    # Set up the figure with specified size
    fig_radar, ax_radar = plt.subplots(figsize=(416 / 96, 260 / 96), dpi=96, subplot_kw=dict(polar=True))
    fig_radar.patch.set_alpha(0.0)  # Transparent figure background

    # Draw the radar chart with transparency
    ax_radar.fill(angles, values, color='skyblue', alpha=0.3)  # Transparent fill
    ax_radar.plot(angles, values, color='blue', linewidth=1)  # Line of the radar chart

    # Customize the radar chart appearance
    ax_radar.set_facecolor('#D9D9D9')  # Set the background color to #D9D9D9
    ax_radar.spines['polar'].set_visible(False)  # Hide the polar spine for a cleaner look
    ax_radar.set_yticklabels([])  # Hide radial axis labels
    ax_radar.grid(color="white", linestyle='--', linewidth=0.5)  # Light grid lines

    # Add labels for each metric at the end of each axis
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(labels, color="black", fontsize=5, fontweight='bold')
    ax_radar.set_title(label="Topics", fontsize=6)
    # Embedding the radar chart in Tkinter
    radar_canvas = FigureCanvasTkAgg(fig_radar, master=window)
    radar_canvas.get_tk_widget().place(x=340, y=300)  # Position of the radar chart


def combine_context(interval):
    """Combines and sends transcriptions and chat messages every specified interval."""
    global latest_transcription, latest_chat
    while True:
        time.sleep(interval)  # Use the specified interval
        if transcriptions or messages:
            # Combine transcriptions and messages
            latest_transcription = " ".join(transcriptions)
            latest_chat = "\n".join(messages)

            # Send to ChatGPT
            summary(latest_transcription, latest_chat)
            time.sleep(2.5)
            bar_graph(latest_transcription, latest_chat)
            time.sleep(2.5)
            radar_map(latest_transcription, latest_chat)
            time.sleep(2.5)
            pie_chart(latest_transcription, latest_chat)

            # Clear lists for the next interval
            transcriptions.clear()
            messages.clear()
            window.mainloop()


# Set the interval as an input
interval = int(input("Enter interval (in seconds) for context updates: "))
from tkinter import Tk, Canvas, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\twitch hackathon\pythonProject2\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1000x550")
window.configure(bg="#FFFFFF")

# Create the canvas for the GUI
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=550,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Add images and text elements to the Tkinter canvas
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(500.0, 36.0, image=image_image_1)

canvas.create_text(
    65.0,
    17.0,
    anchor="nw",
    text="Chat",
    fill="#FFFFFF",
    font=("Inter Bold", 32 * -1)
)

canvas.create_rectangle(
    16.0,
    4.0,
    65.0,
    67.0,
    fill="#FFFFFF",
    outline=""
)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(876.0, 303.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(172.0, 306.0, image=image_image_3)

canvas.create_text(
    821.0,
    122.0,
    anchor="nw",
    text="Chat Summary",
    fill="#FFFFFF",
    font=("Inter Bold", 16 * -1)
)

canvas.create_text(
    129.0,
    125.0,
    anchor="nw",
    text="Chat Mood",
    fill="#FFFFFF",
    font=("Inter Bold", 15 * -1)
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(535.0, 418.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(535.0, 196.0, image=image_image_5)

canvas.create_text(
    509.0,
    338.0,
    anchor="nw",
    text="Topics",
    fill="#453EFF",
    font=("Inter Bold", 16 * -1)
)

canvas.create_text(
    509.0,
    100.0,
    anchor="nw",
    text="Opinion",
    fill="#453EFF",
    font=("Inter Bold", 16 * -1)
)

# Start threads for transcription, chat listening, and context combination
threading.Thread(target=real_time_transcribe, daemon=True).start()
threading.Thread(target=listen_twitch_chat, daemon=True).start()

combine_context(interval)

 # Run in main thread to manage periodic output
