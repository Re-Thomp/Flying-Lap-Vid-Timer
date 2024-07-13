# Thank you Chat
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from PIL import Image
import numpy as np
import cv2

def get_frame_at_time(video, time):
    # Extracts an image from the video given time
    try:
        frame = video.get_frame(time)
        return Image.fromarray(frame)
    except Exception as e:
        st.error(f"Error extracting frame at {time} seconds: {e}")
        return None

def frames_count(handler):
    frames = 0
    while True:
        status, frame = handler.read()
        if not status:
            break
        frames += 1
    return frames 

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.markdown("***")

    # Import video
    uploaded_file = st.file_uploader("Choose a video file (crop or compress files larger than 200mb)", type=["mp4", "mov", "avi", "mkv"])
    st.caption("*May take some time to upload")
    st.markdown("***")
    
    if uploaded_file is not None:
        # Save uploaded video file to temp
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()
        
        # Load video and find stats
        video_path = temp_file.name
        video = VideoFileClip(temp_file.name)
        fps = video.fps
        total = frames_count(cv2.VideoCapture(video_path))
        framesit = total - 1
        duration = framesit * fps

        # Select start and end points with frame preview
        start_point = st.slider("Select start frame (line up blade tip and start line in preview image)", 0, framesit, 0, 1)
        start_time = start_point / fps
        start_frame = get_frame_at_time(video, start_time)
        if start_frame:
            st.image(start_frame, caption=f"Start Frame at {start_time:.4f} seconds", use_column_width=True)

        end_point = st.slider("Select end frame", 0, framesit, framesit, 1)
        end_time = end_point / fps
        end_frame = get_frame_at_time(video, end_time)
        if end_frame:
            st.image(end_frame, caption=f"End Frame at {end_time:.4f} seconds", use_column_width=True)

        if st.button("Calculate lap time"):
            if start_time < end_time:
                time_elapsed = end_time - start_time
                st.success(f"Your lap time is {time_elapsed:.2f} seconds!")

        st.markdown("***")
        st.caption("Restart web page to time another video")

        # Clean up temporary file
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()
