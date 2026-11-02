# Webcam Time-Lapse Recorder

> **Capture less. Preserve what matters.**

A Python-based webcam time-lapse recorder built with OpenCV. Designed to reduce unnecessary video recording by capturing frames at controlled intervals and encoding them directly into an MP4 video.

Instead of continuously saving every frame, the application samples the webcam feed, adds timestamps, and generates a time-lapse video in real time.

## Overview

Traditional video recording captures and stores continuous footage, even when most individual frames aren't necessary.

This project takes a different approach:

- Capture only one frame at a specified interval.
- Control the playback speed independently through video FPS.
- Request a specific webcam resolution.
- Add timestamps directly to captured frames.
- Write frames straight into an MP4 file.
- Avoid creating temporary image files.

The goal is to provide a lightweight and practical solution for long-duration visual monitoring and time-lapse recording.

## Features

- **Interval-based frame capture:** Capture frames at configurable time intervals.
- **Playback FPS control:** Determine how quickly the final time-lapse plays.
- **Resolution control:** Request a desired webcam resolution and detect the actual resolution provided by the camera.
- **Direct MP4 encoding:** Write captured frames directly into the output video.
- **Timestamp overlay:** Automatically display the capture time on each saved frame.
- **Live webcam preview:** Monitor the camera feed while recording.
- **Automatic file organization:** Generate date-based filenames and separate recording sessions.
- **Resource management:** Release the webcam, video writer, and preview window when recording ends.
- **Compatibility checks:** Detect webcam initialization and video writer failures.

## How It Works

The application continuously reads frames from the webcam but only saves a frame when the configured capture interval has elapsed.

Each selected frame is timestamped and passed directly to OpenCV's video writer.

```text
Webcam Input
     |
     v
Continuous Frame Reading
     |
     v
Capture Interval Check
     |
     v
Frame Selection
     |
     v
Timestamp Overlay
     |
     v
Direct MP4 Encoding
     |
     v
Final Time-Lapse Video
```

The live preview operates independently of the frame-saving interval.

## Understanding the Recording Parameters

One of the central design decisions in this project is separating **capture frequency** from **video playback FPS**.

| Parameter    | Description                     | Current value |
| ------------ | ------------------------------- | ------------- |
| FRAME_WIDTH  | Requested recording width       | 854 px        |
| FRAME_HEIGHT | Requested recording height      | 480 px        |
| INTERVAL     | Seconds between captured frames | 2 seconds     |
| VIDEO_FPS    | Playback frames per second      | 30 FPS        |

### Capture Interval vs. Playback FPS

The time-lapse speed is determined by the relationship between these two parameters.

**Time-lapse speed multiplier:**

`Capture Interval × Video FPS`

With the current configuration:

`2 × 30 = 60×`

This means approximately 60 seconds of real-world activity are compressed into one second of video.

### Example

| Real-world duration | Final video duration |
| ------------------- | -------------------- |
| 1 minute            | 1 second             |
| 10 minutes          | 10 seconds           |
| 30 minutes          | 30 seconds           |
| 1 hour              | 1 minute             |
| 8 hours             | 8 minutes            |

These are theoretical durations assuming consistent capture intervals.

## Storage Efficiency

The application avoids recording and storing continuous footage when only periodic visual samples are required.

Instead of generating thousands of individual image files, captured frames are written directly into a single MP4 file.

This approach provides two practical benefits:

1. No separate image-storage directory is required.
2. No additional post-recording image-to-video compilation process is necessary.

Actual storage consumption depends on resolution, image complexity, codec behavior, and recording duration.

## Technology Stack

| Technology | Purpose                                            |
| ---------- | -------------------------------------------------- |
| Python     | Application logic                                  |
| OpenCV     | Webcam access, image processing and video encoding |
| Time       | Capture interval management                        |
| OS         | Directory creation and file management             |
| Glob       | Existing recording discovery                       |
| Datetime   | Timestamp and filename generation                  |

## Installation

### Requirements

- Python 3
- A working webcam
- OpenCV

Install the dependency:

```bash
pip install opencv-python
```

### Run the application

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/webcam-timelapse.git
```

Navigate into the project:

```bash
cd webcam-timelapse
```

Run:

```bash
python main.py
```

Before running, configure the `SAVE_DIR` variable in `main.py` to a valid output directory on your system.

## Configuration

The primary recording settings are located at the beginning of `main.py`.

```python
SAVE_DIR = r"F:\Time Lapse Recordings"

CAMERA_INDEX = 0

FRAME_WIDTH = 854
FRAME_HEIGHT = 480

INTERVAL = 2

VIDEO_FPS = 30
```

Modify these values to change the recording behavior.

The requested camera resolution may differ from the actual resolution supported by your webcam. The application reads back the camera's reported dimensions and uses them when initializing the video writer.

## Output Structure

Recordings are organized using the date and session number.

```text
Time Lapse Recordings/
│
├── 02-11-26_1.mp4
├── 02-11-26_2.mp4
├── 02-11-26_3.mp4
│
└── 03-11-26_1.mp4
```

Each execution creates a separate recording session.

## Controls

| Action           | Function                                  |
| ---------------- | ----------------------------------------- |
| Press `Q`        | Stop recording through the preview window |
| Press `Ctrl + C` | Interrupt recording through the terminal  |

The application releases its camera and video-writing resources when recording stops.

## Current Implementation Details

- Webcam input format requested: MJPG
- Output video container: MP4
- Output codec requested: MP4V
- Timestamp format: HH
- Default capture interval: 2 seconds
- Default playback speed: 30 FPS
- Preview dimensions: 640 × 480

## Future Improvements

Potential development directions:

- [ ] Improve automatic recording segment numbering.
- [ ] Add command-line configuration.
- [ ] Support multiple webcam devices.
- [ ] Add configurable timestamp formats.
- [ ] Preserve preview aspect ratio.
- [ ] Add recording statistics and estimated storage consumption.
- [ ] Add more advanced video quality and encoding controls.
- [ ] Improve recovery and reporting after unexpected recording failures.

## Project Motivation

This project was developed to solve a practical problem: continuously recording video is often unnecessary when the objective is to observe gradual changes over time.

The implementation explores how frame sampling, video encoding, resolution selection, and playback FPS can be combined to produce a useful time-lapse recording without the overhead of storing continuous footage or intermediate images.

It is also an exploration of applying Python and OpenCV to a real-world problem rather than limiting development to isolated programming exercises.

---

**Built with Python and OpenCV.**
