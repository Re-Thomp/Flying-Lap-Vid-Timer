# Thank you Chat for the help
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from PIL import Image

def preview_frame(video, time):
# Gets a preview frame given time, compensates for moviepy last frame error
    error_time = time
    try:
        frame = video.get_frame(time)
        return Image.fromarray(frame)
    except Exception as e:
        if isinstance(time, float):
            for i in range(15):
                time -= 0.01
                try:
                    frame = video.get_frame(time)
                    return Image.fromarray(frame)
                except Exception as e:
                    continue
            st.error(f"Error extracting frame at {error_time:.2f} seconds: {e}")
            return None

        else:
            st.error(f"Error extracting frame at {time:.2f} seconds: {e}")
            return None

def main():
    st.title("Flying Lap Video Timer")
    st.text("By Reno T.")
    st.caption("*For information about accuracy, see bottom of page")
    st.markdown("***")

    # Video import window
    uploaded_file = st.file_uploader("Upload a video file (crop or compress files larger than 200mb)", type=["mp4", "mov", "avi", "mkv"])
    st.caption("May take some time to upload")
    st.markdown("***")

    if uploaded_file is not None:
        # Save uploaded video file to temp
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()

        # Load video, find stats, and set increments
        video_path = temp_file.name
        video = VideoFileClip(video_path)
        fps = video.fps
        duration = video.duration
        increment = 0.01

        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0.0
        if 'end_time' not in st.session_state:
            st.session_state.end_time = duration
            
        # Select start and end points with frame preview
        left_column, right_column = st.columns(2)
        if left_column.button("Prev. 0.1", 1) and st.session_state.start_time != 0:
            st.session_state.start_time = st.session_state.start_time - increment
        if right_column.button("Next 0.1", 2) and st.session_state.start_time != duration:
            st.session_state.start_time = st.session_state.start_time + increment
        start_time = st.slider("Select start (seconds): align blade with start line in preview", 0.0, duration, st.session_state.start_time, 0.01)
        st.session_state.start_time = start_time
        start_frame = preview_frame(video, start_time)
        if start_frame:
            st.image(start_frame, caption=f"Start frame at {st.session_state.start_time:.2f} seconds", use_column_width=True)

        left_column1, right_column1 = st.columns(2)
        if left_column1.button("Prev. 0.1", 3) and st.session_state.end_time != 0:
            st.session_state.end_time = st.session_state.end_time - increment
        if right_column1.button("Next 0.1", 4) and st.session_state.end_time != duration:
            st.session_state.end_time = st.session_state.end_time + increment
        end_time = st.slider("Select finish (seconds)", 0.0, duration, st.session_state.end_time, 0.01)
        st.session_state.end_time = end_time
        end_frame = preview_frame(video, end_time)
        if end_frame:
            st.image(end_frame, caption=f"End frame at {st.session_state.end_time:.2f} seconds", use_column_width=True)

        if st.button("Calculate lap time"):
            # Results
            if st.session_state.start_time < st.session_state.end_time:
                time_elapsed = st.session_state.end_time - st.session_state.start_time
                st.success(f"Your lap time is {time_elapsed:.2f} seconds!")
            elif st.session_state.start_time == st.session_state.end_time:
                st.success(f"Zero seconds?")
            else:
                time_elapsed = st.session_state.start_time - st.session_state.end_time
                st.success(f"Your lap time is -{time_elapsed:.2f} seconds?")

        st.caption("Refresh web page to time another video")
        st.markdown("***")

        # Clean up
        video.reader.close()
        os.unlink(temp_file.name)

    st.caption("""*Disclaimer: To maximize file compatibility, this app uses time increments that may be slightly off from exact frames. 
            Example time uncertainty: approx. ±0.02s at 60fps and ±0.03s at 30fps for .mp4 with h.264.""")

if __name__ == "__main__":
    main()
