import streamlit as st
import streamlit.components.v1 as components
import math
import random

st.title("YouTube Video Viewer - Dynamic Screens with Random IPs")

# Input YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:")

# Ask user how many screens
num_screens_input = st.text_input("Enter number of screens to display:")

# Button to play all videos
play_all = st.button("Play All Videos")

# Function to convert YouTube URL to embed URL with autoplay
def get_embed_url(url):
    if "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    else:
        return None

# Function to generate a random IPv4 address
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Convert number of screens
try:
    num_screens = int(num_screens_input)
except:
    num_screens = 0

# Safety limit
MAX_SCREENS = 500  # Adjust to prevent browser crash
if num_screens > MAX_SCREENS:
    st.warning(f"Too many screens! Showing only first {MAX_SCREENS} screens.")
    num_screens = MAX_SCREENS

# Display videos if URL valid and button clicked
if youtube_url and play_all and num_screens > 0:
    embed_url = get_embed_url(youtube_url)
    if embed_url:
        screens_per_row = 5
        total_rows = math.ceil(num_screens / screens_per_row)
        for row in range(total_rows):
            cols = st.columns(screens_per_row)
            for col_idx, col in enumerate(cols):
                screen_number = row*screens_per_row + col_idx + 1
                if screen_number > num_screens:
                    break
                with col:
                    ip = random_ip()  # Generate random IP
                    st.markdown(f"**Screen {screen_number}** | IP: {ip}")
                    components.html(
                        f"""
                        <iframe width="250" height="140"
                        src="{embed_url}" 
                        title="YouTube video player" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                        </iframe>
                        """,
                        height=160,
                    )
    else:
        st.warning("Invalid YouTube URL")
elif not youtube_url:
    st.info("Enter a YouTube URL to start.")
elif num_screens <= 0:
    st.info("Enter a valid number of screens.")
