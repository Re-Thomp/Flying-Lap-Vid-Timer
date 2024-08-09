# Thank you Chat for the help
import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os
from PIL import Image

def preview_frame(video, time):
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

        # Load video and find stats
        video_path = temp_file.name
        video = VideoFileClip(video_path)
        fps = video.fps
        duration = video.duration

        # Initialize session state for start_time and end_time if not already set
        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0.0
        if 'end_time' not in st.session_state:
            st.session_state.end_time = duration

        # Define increment
        increment = 0.1

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Previous Frame"):
                st.session_state.start_time = max(0, st.session_state.start_time - 1 / fps)
                st.session_state.end_time = max(0, st.session_state.end_time - 1 / fps)

            if st.button("Previous 0.1s"):
                st.session_state.start_time = max(0, st.session_state.start_time - increment)
                st.session_state.end_time = max(0, st.session_state.end_time - increment)

        with col2:
            if st.button("Next Frame"):
                st.session_state.start_time = min(duration, st.session_state.start_time + 1 / fps)
                st.session_state.end_time = min(duration, st.session_state.end_time + 1 / fps)

            if st.button("Next 0.1s"):
                st.session_state.start_time = min(duration, st.session_state.start_time + increment)
                st.session_state.end_time = min(duration, st.session_state.end_time + increment)

        # Sliders to select start and end times
        start_time = st.slider(
            "Select start (seconds): align blade with start line in preview", 
            0.0, duration, st.session_state.start_time, 0.01
        )
        end_time = st.slider(
            "Select finish (seconds)", 
            0.0, duration, st.session_state.end_time, 0.01
        )

        # Update session state based on slider changes
        st.session_state.start_time = start_time
        st.session_state.end_time = end_time

        # Update frame previews
        start_frame = preview_frame(video, st.session_state.start_time)
        if start_frame:
            st.image(start_frame, caption=f"Start frame at {st.session_state.start_time:.2f} seconds", use_column_width=True)

        end_frame = preview_frame(video, st.session_state.end_time)
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
