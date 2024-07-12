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
        st.error(f"Error extracting frame at {time:.2f} seconds: {e}")
        return None

def main():
    st.title("Video Timing Web Application")

    # Page 1: Import video
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if st.session_state.uploaded_file is None:
        st.header("Import Video")
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.session_state.temp_file_path = None
            st.experimental_rerun()
    else:
        st.text("Uploading...")

        if st.session_state.temp_file_path is None:
            # Save the uploaded video file to a temporary location
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(st.session_state.uploaded_file.read())
            temp_file.close()
            st.session_state.temp_file_path = temp_file.name

        try:
            video = VideoFileClip(st.session_state.temp_file_path)
            fps = video.fps
            duration = video.duration

            st.header("Select Start and End Points")
            st.text("Use the slider to select start and end points")

            # Select start and end points with frame preview
            start_time = st.slider("Select start time", 0.0, duration, 0.0, 0.01)
            start_frame = get_frame_at_time(video, start_time)
            if start_frame:
                st.image(start_frame, caption=f"Start Frame at {start_time:.2f} seconds", use_column_width=True)
            st.text(f"Start time: {start_time:.2f} seconds")

            end_time = st.slider("Select end time", 0.0, duration, duration, 0.01)
            end_frame = get_frame_at_time(video, end_time)
            if end_frame:
                st.image(end_frame, caption=f"End Frame at {end_time:.2f} seconds", use_column_width=True)
            st.text(f"End time: {end_time:.2f} seconds")

            if st.button("Calculate Time Elapsed"):
                if start_time < end_time:
                    frames_elapsed = (end_time - start_time) * fps
                    time_elapsed = frames_elapsed / fps
                    st.success(f"Time Elapsed: {time_elapsed:.2f} seconds")
                else:
                    st.error("End time must be greater than start time")
            
            if st.button("Time Another Video"):
                st.session_state.uploaded_file = None
                st.session_state.temp_file_path = None
                st.rerun()
        except Exception as e:
            st.error(f"Error processing video: {e}")

        # Clean up the temporary file
        if st.session_state.temp_file_path:
            os.unlink(st.session_state.temp_file_path)
            st.session_state.temp_file_path = None

if __name__ == "__main__":
    main()
