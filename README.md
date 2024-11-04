# Twitch Streamer Tools Hackathon Project

This project is a powerful, AI-driven tool for Twitch streaming that provides real-time chat analytics and visualization for streamers. Follow all instructions precisely to ensure proper setup and functionality.

---

## Table of Contents
1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Usage](#usage)
4. [Files and Assets](#files-and-assets)
5. [Requirements](#requirements)

---

## Installation
To set up this project correctly, follow these steps carefully:

1. **Clone or Download**  
   Clone or download the repository from GitHub.

2. **Install Dependencies**  
   Install all dependencies listed in the `requirements.txt` file to ensure compatibility with the code.

3. **Configuration**  
   Follow each step exactly as described. Any variations could impact functionality.

---

## Project Structure
- **`jm.py`**: The main script. This file:
  - Contains core functionality for chat data processing and analytics.
  - Accesses assets, so ensure asset locations are correctly configured.

- **`app.py`**: Handles the authorization workflow with the Twitch app.  
   *Note*: Access tokens are currently embedded in `jm.py`, but if you wish to handle authorization manually or update OAuth tokens, use `app.py` to generate new tokens and integrate them into `jm.py`.

- **`report.py`**: Run this file after the stream ends to generate a PDF report summarizing chat insights.  
   *Sample PDF Report* is included as a reference for the output format.

---

## Files and Assets
Here is a breakdown of key files and their functions:

- **Sample PDF Report**:  
  A reference PDF showing the format of the report that will be generated from chat analysis.

- **`streamdata.txt`**:  
  This file contains raw data retrieved from the Twitch stream.

- **`summary.txt`**:  
  Contains a summarized version of the chat for quick reference.

**Important**: Ensure that all assets required by `jm.py` are placed in their correct directories. Verify the file paths to avoid missing dependencies during runtime.

---

## Usage

### Main Application
1. **Run `jm.py`**  
   - This script includes the access token and will automatically fetch chat data and display live analytics.

### Authorization (Optional)
2. **Generate Access Tokens**  
   - If you prefer to manage authorization manually, run `app.py` to generate the required access tokens. Then, update `jm.py` with the new tokens as needed.

### Post-Stream Report
3. **Run `report.py`**  
   - After the stream concludes, execute `report.py` to generate a PDF report summarizing chat activity. The report includes sentiment analysis, topic trends, and other insights.

---

By following these steps, you’ll have a complete setup to monitor and analyze Twitch chat in real-time, enhancing the interactivity and engagement of your streaming experience.
