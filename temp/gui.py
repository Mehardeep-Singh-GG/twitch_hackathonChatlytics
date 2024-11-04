from tkinter import Tk, Canvas, PhotoImage
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# from pathlib import Path
#
# # Data for bar chart
# mood_data = {
#     "Happy": 8,
#     "Sad": 4,
#     "Excited": 6,
#     "Calm": 7,
#     "Angry": 3
# }
#
# # Set up Tkinter window
#
# # Set up Matplotlib figure for bar chart
# fig, ax = plt.subplots(figsize=(240 / 96, 306 / 96), dpi=96)  # Convert 240x306 px to inches
# fig.patch.set_facecolor('#D9D9D9')
# fig.patch.set_alpha(0.0)  # Transparent figure background
#
# # Plotting the data
# x_labels = list(mood_data.keys())
# y_values = list(mood_data.values())
#
# bars = ax.bar(x_labels, y_values, color="#453EFF", alpha=0.7)
# ax.set_ylim(0, 10)
# ax.set_facecolor('#D9D9D9')  # Axis background color
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.tick_params(axis='both', which='both', length=0)
# ax.grid(visible=True, color='white', linestyle='--', linewidth=0.5)
#
# # Adding labels to bars
# for bar in bars:
#     yval = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.2, int(yval), ha='center', va='bottom', color="#333333")
#
# # Embedding the Matplotlib figure in Tkinter
# bar_canvas = FigureCanvasTkAgg(fig, master=window)
# bar_canvas.get_tk_widget().place(x=52, y=177)
#


# Run Tkinter main loop
from tkinter import Tk, Canvas, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pathlib import Path

# Data for bar chart
mood_data = {
    "Happy": 8,
    "Sad": 4,
    "Excited": 6,
    "Calm": 7,
    "Angry": 3
}

# Set up Tkinter window
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/pythonProject2/assets/frame0")

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

# Set up Matplotlib figure for bar chart
fig, ax = plt.subplots(figsize=(235 / 96, 312 / 96), dpi=96)
fig.patch.set_facecolor('#D9D9D9')
fig.patch.set_alpha(0.0)  # Transparent figure background

# Plotting the bar chart
x_labels = list(mood_data.keys())
y_values = list(mood_data.values())

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
bar_canvas.get_tk_widget().place(x=52, y=171)  # Bar chart position

# Set up Matplotlib figure for text box
fig_text, ax_text = plt.subplots(figsize=(172 / 96, 306 / 96), dpi=96)
fig_text.patch.set_facecolor('#D9D9D9')
fig_text.patch.set_alpha(0.0)  # Transparent figure background
ax_text.axis('off')  # Hide axes

# Paragraph-style text box with formatted content
paragraph_text = (
    "Mood Analysis Summary:\n\n"
    "This chart illustrates the mood distribution based on chat data. "
    "The most prominent mood is 'Happy' with a value of 8, followed closely "
    "by 'Calm' and 'Excited.' Less frequent moods include 'Sad' and 'Angry,' "
    "indicating a generally positive sentiment.\n\n"
    "This analysis provides insights into the overall emotional climate "
    "within the chat, helping guide the tone of responses and content."
)
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
text_canvas.get_tk_widget().place(x=789, y=171)  # Text box position

# Run Tkinter main loop
# Sample data for the pie chart
# Sample data for the pie chart
labels = ['Positive', 'Negative']
sizes = [70, 30]  # Adjust these values as needed

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
pie_canvas.get_tk_widget().place(x=416, y=76)  # Position of the pie chart

import numpy as np

# Sample data dictionary for the radar chart
data = {
    'Metric 1': 3,
    'Metric 2': 4,
    'Metric 3': 2,
    'Metric 4': 5,
    'Metric 5': 3.5
}

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
ax_radar.set_title(label="Topics",fontsize=6)
# Embedding the radar chart in Tkinter
radar_canvas = FigureCanvasTkAgg(fig_radar, master=window)
radar_canvas.get_tk_widget().place(x=340, y=300)  # Position of the radar chart

window.mainloop()

