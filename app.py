# Thank you Chat
import streamlit as st
import tempfile
import os
from PIL import Image
import imageio

def get_frame(video_reader, point):
    try:
        frame = video_reader.get_data(point)
        return Image.fromarray(frame)
    except Exception as e:
        st.error(f"Error extracting frame at {point} frames: {e}")
        return None

def frame_time(video_reader, point):
    return video_reader.get_meta_data()['duration'] * (point / video_reader.count_frames())

def count_frames(video_reader):
    return video_reader.count_frames()

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.caption("*potentially a little inaccurate, currently debugging")
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
        video_reader = imageio.get_reader(video_path)
        total_frames = count_frames(video_reader)

        # Select start and end points with frame preview
        start_point = st.slider("Select start frame (line up blade tip and start line in preview image)", 0, total_frames - 1, 0, 1)
        start_frame = get_frame(video_reader, start_point)
        start_time = frame_time(video_reader, start_point)
        if start_frame:
            st.image(start_frame, caption=f"Start Frame at {start_time:.3f} seconds", use_column_width=True)

        end_point = st.slider("Select end frame", 0, total_frames - 1, total_frames - 1, 1)
        end_frame = get_frame(video_reader, end_point)
        end_time = frame_time(video_reader, end_point)
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
        os.unlink(temp_file.name)

if __name__ == "__main__":
    main()
