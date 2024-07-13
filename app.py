# Thank you Chat
import streamlit as st
import tempfile
import os
from PIL import Image
import numpy as np
import cv2

def get_frame_at_time(video_cap, point):
    # Extracts an image from the video given the frame number
    video_cap.set(cv2.CAP_PROP_POS_FRAMES, point)
    _, frame = video_cap.read()
    if frame is not None:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
        st.error(f"Error extracting frame at {point} frames.")
        return None

def get_time(vid, length):
    if vid.set(cv2.CAP_PROP_POS_FRAMES, length):
        return vid.get(cv2.CAP_PROP_POS_MSEC)
    return None

def count_frames(video):
    total_frames = 0
    while True:
        ret, _ = video.read()
        if not ret:
            break
        total_frames += 1
    video.release()
    return total_frames
    

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.caption("*potentially a little innacurate, currently debugging")
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
        cap = cv2.VideoCapture(video_path)
        total_frames = count_frames(cap) 
        fps = total_frames / (get_time(cap, total_frames)/100)

        # Select start and end points with frame preview
        start_point = st.slider("Select start frame (line up blade tip and start line in preview image)", 0, total_frames, 0, 1)
        start_time = start_point / float(fps)
        start_frame = get_frame_at_time(cap, start_point)
        if start_frame:
            st.image(start_frame, caption=f"Start Frame at {start_time:.3f} seconds", use_column_width=True)
            legacyfps = cap.get(cv2.CAP_PROP_FPS)
            st.caption(f"Legacy video FPS: {legacyfps}")
            st.caption(f"New FPS: {fps}")

        end_point = st.slider("Select end frame", 0, total_frames, total_frames, 1)
        end_time = end_point / float(fps)
        end_frame = get_frame_at_time(cap, end_point)
        if end_frame:
            st.image(end_frame, caption=f"End Frame at {end_time:.3f} seconds", use_column_width=True)
            st.caption(f"End Point: {end_point}")

        if st.button("Calculate lap time"):
            if start_time < end_time:
                time_elapsed = end_time - start_time
                st.success(f"Your lap time is {time_elapsed:.2f} seconds!")
            if start_time == end_time:
                st.success(f"Zero seconds?")
            if start_time > end_time:
                time_elapsed = start_time - end_time
                st.success(f"Your lap time is -{time_elapsed:.2f} seconds?")

        st.markdown("***")
        st.caption("Restart web page to time another video")

        # Clean up
        cap.release()
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()
