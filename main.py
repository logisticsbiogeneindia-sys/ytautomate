import streamlit as st
import os
import shutil
import datetime
from scrape_videos import scrapeVideos
from make_compilation import makeCompilation
from upload_ytvid import uploadYtvid
import googleapiclient.errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import config

# Constants (make sure you set these in your config)
num_to_month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "June", 7: "July", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_NAME = "token.json"
client_secrets_file = "googleAPI.json"

# Function to handle the routine
def routine(IG_USERNAME, IG_PASSWORD, title, TOTAL_VID_LENGTH, MAX_CLIP_LENGTH, MIN_CLIP_LENGTH, DAILY_SCHEDULED_TIME, INTRO_VID, OUTRO_VID):
    st.write("Starting the routine...")
    
    # Set up Google API credentials
    creds = None
    if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_console()
        with open(TOKEN_NAME, 'w') as token:
            token.write(creds.to_json())
    
    googleAPI = build('youtube', 'v3', credentials=creds)

    now = datetime.datetime.now()
    videoDirectory = f"./DankMemes_{num_to_month[now.month]}_{str(now.year)}_V{str(now.day)}/"
    outputFile = f"./{num_to_month[now.month]}_{str(now.year)}_v{str(now.day)}.mp4"
    
    if not os.path.exists(videoDirectory):
        os.makedirs(videoDirectory)
    
    # Scrape Videos
    st.write("Scraping Videos...")
    scrapeVideos(username=IG_USERNAME, password=IG_PASSWORD, output_folder=videoDirectory, days=1)
    st.write("Scraping complete!")

    # Make Compilation
    st.write("Making Compilation...")
    makeCompilation(path=videoDirectory,
                    introName=INTRO_VID,
                    outroName=OUTRO_VID,
                    totalVidLength=TOTAL_VID_LENGTH,
                    maxClipLength=MAX_CLIP_LENGTH,
                    minClipLength=MIN_CLIP_LENGTH,
                    outputFile=outputFile)
    st.write("Compilation complete!")

    # Upload to YouTube
    description = f"Enjoy the memes! :) \n\n#memes #dankmemes #compilation #funny #funnyvideos"
    st.write("Uploading to YouTube...")
    uploadYtvid(VIDEO_FILE_NAME=outputFile, title=title, description=description, googleAPI=googleAPI)
    st.write("Video Uploaded to YouTube!")

    # Cleanup temp files
    st.write("Cleaning up...")
    shutil.rmtree(videoDirectory, ignore_errors=True)
    try:
        os.remove(outputFile)
    except OSError as e:
        st.write(f"Error deleting temp file: {e}")
    st.write("Cleanup complete!")

# Streamlit UI Elements
st.title("Automated Video Scraper & Uploader")
st.sidebar.header("Settings")

# User Inputs
IG_USERNAME = st.sidebar.text_input("Instagram Username", value=config.IG_USERNAME)
IG_PASSWORD = st.sidebar.text_input("Instagram Password", value=config.IG_PASSWORD, type='password')
title = st.sidebar.text_input("YouTube Video Title", value="TRY NOT TO LAUGH (BEST Dank video memes) V1")
INTRO_VID = st.sidebar.text_input("Intro Video (Optional)", value="")
OUTRO_VID = st.sidebar.text_input("Outro Video (Optional)", value="")
TOTAL_VID_LENGTH = st.sidebar.slider("Total Video Length (in minutes)", min_value=1, max_value=60, value=13)
MAX_CLIP_LENGTH = st.sidebar.slider("Maximum Clip Length (seconds)", min_value=5, max_value=60, value=19)
MIN_CLIP_LENGTH = st.sidebar.slider("Minimum Clip Length (seconds)", min_value=1, max_value=60, value=5)
DAILY_SCHEDULED_TIME = st.sidebar.time_input("Scheduled Time", datetime.time(20, 0))

# Start Button
if st.sidebar.button("Start Process"):
    try:
        routine(IG_USERNAME, IG_PASSWORD, title, TOTAL_VID_LENGTH, MAX_CLIP_LENGTH, MIN_CLIP_LENGTH, DAILY_SCHEDULED_TIME, INTRO_VID, OUTRO_VID)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.sidebar.write("Made with ❤️ using Streamlit")
