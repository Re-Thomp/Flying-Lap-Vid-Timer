# Thank you Chat
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from PIL import Image

def get_frame(video, time, length, fps):
    try:
        if time < length:
            frame = video.get_frame(time)
            return Image.fromarray(frame)
        if time >= length:
            frame = video.get_frame(length - 0.02)
            return Image.fromarray(frame)
    except Exception as e:
        st.error(f"Error extracting frame at {time:.2f} seconds: {e}")
        return None

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.caption("*currently a little inaccurate, undergoing maintenance to improve functionality")
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
        video = VideoFileClip(video_path)
        fps = video.fps
        duration = video.duration

        # Select start and end points with frame preview
        start_time = st.slider("Select start (seconds), align blade with start line in preview", 0.0, duration, 0.0, 0.01)
        start_frame = get_frame(video, start_time, duration, fps)
        if start_frame:
            st.image(start_frame, caption=f"Start Frame at {start_time:.3f} seconds", use_column_width=True)

        end_time = st.slider("Select finish (seconds)", 0.0, duration, duration, 0.01)
        end_frame = get_frame(video, end_time, duration, fps)
        if end_frame:
            st.image(end_frame, caption=f"End Frame at {end_time:.3f} seconds", use_column_width=True)

        if st.button("Calculate lap time"):
            if start_time < end_time:
                time_elapsed = end_time - start_time
                st.success(f"Your lap time is {time_elapsed:.2f} seconds!")
            elif start_time == end_time:
                st.success(f"Zero seconds?")
            else:
                time_elapsed = start_time - end_time
                st.success(f"Your lap time is -{time_elapsed:.2f} seconds?")

        st.markdown("***")
        st.caption("Restart web page to time another video")

        # Clean up
        video.reader.close()
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()
