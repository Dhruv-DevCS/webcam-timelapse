import cv2
import time
import os
import glob
from datetime import datetime

# Configuration
SAVE_DIR = r"F:\Time Lapse Recordings"
CAMERA_INDEX = 0
FRAME_WIDTH = 854
FRAME_HEIGHT = 480
INTERVAL = 2  # Seconds between saved frames
VIDEO_FPS = 30  # Speed of the final time-lapse video

# Ensure output directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# 1. LOCK DATE AND SEGMENT NUMBER (n) AT START
start_time = datetime.now()
date_str = start_time.strftime("%d-%m-%y")

# Count existing videos for today to calculate 'n'
existing_today_videos = glob.glob(os.path.join(SAVE_DIR, f"{date_str}_*.mp4"))
n = len(existing_today_videos) + 1

# Target video path
video_filename = f"{date_str}_{n}.mp4"
video_path = os.path.join(SAVE_DIR, video_filename)

# Initialize webcam
cap = cv2.VideoCapture(CAMERA_INDEX)

# OPTIMIZATION: At higher resolutions (e.g. 1080p), many USB webcams only
# reach a smooth frame rate if asked to deliver MJPG (compressed) frames.
# Without this, some cameras silently drop to a very low fps at 1080p.
# If the camera doesn't support MJPG, this line is simply ignored.
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# BUGFIX: Confirm the webcam actually opened before doing anything else
if not cap.isOpened():
    print(f"Error: Could not open webcam at index {CAMERA_INDEX}. "
          f"Check that it's connected and not in use by another program.")
    raise SystemExit(1)

# BUGFIX: Cameras often ignore the requested resolution and return frames
# in their own native size. Read back the ACTUAL size so the VideoWriter
# is created with dimensions that match the frames we'll actually get.
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if (actual_width, actual_height) != (FRAME_WIDTH, FRAME_HEIGHT):
    print(f"Note: Camera provided {actual_width}x{actual_height} instead of "
          f"the requested {FRAME_WIDTH}x{FRAME_HEIGHT}. Using the actual size.")

# Initialize Video Writer directly at script start, using the ACTUAL frame size
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_path, fourcc, VIDEO_FPS, (actual_width, actual_height))

# BUGFIX: Confirm the video file could actually be created (e.g. codec available)
if not video_writer.isOpened():
    print("Error: Could not create the video file. The 'mp4v' codec may not "
          "be available on this system.")
    cap.release()
    raise SystemExit(1)

last_saved_time = 0
frames_captured = 0

print(f"Recording direct time-lapse stream to: {video_path}")
print("Press 'q' in preview window or 'Ctrl+C' in terminal to stop.")

# OPTIMIZATION: Clock text settings and size never change between frames
# (it's always "HH:MM"), so compute them once instead of on every save.
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
thickness = 2
color = (255, 255, 255)  # White text
(text_w, text_h), baseline = cv2.getTextSize("00:00", font, font_scale, thickness)
margin_right = 15
margin_top = 30
x = actual_width - text_w - margin_right
y = margin_top

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame from webcam.")
            break

        current_time = time.time()

        # Capture frame every INTERVAL seconds
        if current_time - last_saved_time >= INTERVAL:
            time_str = datetime.now().strftime("%H:%M")
            frame_to_save = frame.copy()

            # Black outline + white text
            cv2.putText(frame_to_save, time_str, (x + 1, y + 1), font, font_scale, (0, 0, 0), thickness + 1)
            cv2.putText(frame_to_save, time_str, (x, y), font, font_scale, color, thickness)

            # WRITE DIRECTLY TO MP4 FILE (No temp files created)
            video_writer.write(frame_to_save)
            frames_captured += 1
            print(f"Captured frame #{frames_captured} directly into {video_filename}")

            last_saved_time = current_time

        # Live Preview Window
        # OPTIMIZATION: only resize if the frame isn't already the display size
        if (frame.shape[1], frame.shape[0]) != (640, 480):
            preview_frame = cv2.resize(frame, (640, 480))
        else:
            preview_frame = frame

        cv2.imshow("Webcam Live Preview (Press 'q' to Quit)", preview_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nScript interrupted by user via terminal.")
finally:
    # Safely release resources
    cap.release()
    video_writer.release()  # Closes and saves the MP4 cleanly
    cv2.destroyAllWindows()

    print(f"\nSuccess! Time-lapse finished with {frames_captured} frames.")
    print(f"Video file saved instantly to: {video_path}")
