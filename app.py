# Thank you Chat
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from PIL import Image
import numpy as np

def get_frame_at_time(video, time):
    """Extracts a frame from the video at the specified time."""
    try:
        frame = video.get_frame(time)
        return Image.fromarray(frame)
    except Exception as e:
        st.error(f"Error extracting frame at {time} seconds: {e}")
        return None

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.markdown("***")

    # Page 1: Import video
    uploaded_file = st.file_uploader("Choose a video file (crop or compress files larger than 200mb)", type=["mp4", "mov", "avi", "mkv"])
    st.caption("*Please be patient while the video is uploading")
    st.markdown("***")
    
    if uploaded_file is not None:
        # Save the uploaded video file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()
        
        # Load video using moviepy
        video = VideoFileClip(temp_file.name)
        fps = video.fps
        duration = video.duration

        # Adjust the duration to remove the last frame
        adjusted_duration = duration - (1 / fps)

        # Select start and end points with frame preview
        start_time = st.slider("Select start time (line up blade tip with start line in preview)", 0.0, adjusted_duration, 0.0, 0.01)
        start_frame = get_frame_at_time(video, start_time)
        if start_frame:
            st.image(start_frame, caption=f"Start Frame at {start_time:.2f} seconds", use_column_width=True)

        end_time = st.slider("Select end time", 0.0, adjusted_duration, adjusted_duration, 0.01)
        end_frame = get_frame_at_time(video, end_time)
        if end_frame:
            st.image(end_frame, caption=f"End Frame at {end_time:.2f} seconds", use_column_width=True)

        if st.button("Calculate Time Elapsed"):
            if start_time < end_time:
                time_elapsed = end_time - start_time
                st.success(f"Time Elapsed: {time_elapsed:.2f} seconds")

        st.markdown("***")
        st.subheader("Restart web page to time another video")

        # Clean up the temporary file
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()
