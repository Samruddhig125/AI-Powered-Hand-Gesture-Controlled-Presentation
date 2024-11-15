# Hand Gesture-Controlled Presentation Tool

A hand gesture-controlled presentation tool using OpenCV and `cvzone` that allows users to interact with their slides seamlessly. This project uses computer vision to detect specific hand gestures for slide navigation, drawing annotations, zooming, and adjusting brush settings.

## Features

- **Slide Navigation**: Swipe gestures allow you to move forward and backward through slides.
- **Annotation Drawing**: Use your index finger to draw directly on the slides with adjustable colors and brush sizes.
- **Zooming**: Pinch gestures with the thumb and index finger adjust the zoom level.
- **Brush Customization**: Switch colors and brush sizes using hand gestures.
- **Accuracy Tracking**: Monitors and displays the accuracy of recognized gestures.

## Requirements

- Python 3.x
- OpenCV
- `cvzone` library for hand detection
- `numpy`

To install the required packages, run:

pip install opencv-python cvzone numpy mediapipe



## How To Use:

- **Set Up the Camera**: Ensure your camera is connected and accessible.

- **Load Slides**: Place your presentation images in a folder named Presentation in the project directory.

- **Run the Program**:
python main.py

## Hand Gestures:

- **Swipe Left**: Move to the previous slide.
- **Swipe Right**: Move to the next slide.
- **Index Finger Up**: Draw on the slide.
- **Three Fingers Up**: Undo the last annotation.
- **Four Fingers Up**: Change the brush color.
- **Five Fingers Up**: Change the brush size.
- **Thumb and Index Finger Pinch**: Zoom in or out on the slide.
- **Quit**: Press q to exit the program

