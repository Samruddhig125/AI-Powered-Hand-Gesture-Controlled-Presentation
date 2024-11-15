from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

# Parameters
width, height = 900, 700
gestureThreshold = 250
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = []
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = [[]]
annotationNumber = -1
annotationStart = False
hs, ws = int(160 * 1), int(200 * 1)
zoomFactor = 1.0  # Initial zoom factor
maxZoom = 2.0     # Maximum zoom level
minZoom = 1.0     # Minimum zoom level
initialDistance = None
zooming = False
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)]  # Red, Green, Blue, Yellow
colorIndex = 0
brushSizes = [5, 10, 15, 20]
brushSizeIndex = 0
# Accuracy tracking
correctGestures = 0  # Counter for correct gestures
totalGestures = 0    # Total gestures attempted

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        # Slide Navigation
        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                correctGestures += 1
                totalGestures += 1
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                correctGestures += 1
                totalGestures += 1

        # Drawing
        if fingers == [0, 1, 0, 0, 0]:  # Index finger up for drawing
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])

            annotations[annotationNumber].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, brushSizes[brushSizeIndex], colors[colorIndex], cv2.FILLED)

        else:
            annotationStart = False

        # Clear Last Annotation
        if fingers == [0, 1, 1, 1, 0]: # Three Fingers up
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

        # Change brush color (four fingers up)
        if fingers == [1, 1, 1, 1, 0] and buttonPressed is False:
            colorIndex = (colorIndex + 1) % len(colors)
            buttonPressed = True
            correctGestures += 1
            totalGestures += 1

        # Change brush size (five fingers up)
        if fingers == [1, 1, 1, 1, 1] and buttonPressed is False:
            brushSizeIndex = (brushSizeIndex + 1) % len(brushSizes)
            buttonPressed = True
            correctGestures += 1  
            totalGestures += 1

        # Zoom using thumb and index finger pinch
        if fingers == [1, 1, 0, 0, 0]:  # Thumb and index finger up for zooming
            x1, y1 = lmList[4][0], lmList[4][1]  # Thumb tip
            x2, y2 = lmList[8][0], lmList[8][1]  # Index finger tip
            distance = np.hypot(x2 - x1, y2 - y1)

            if initialDistance is None:
                initialDistance = distance
            zoomFactor += (distance - initialDistance) / 200
            zoomFactor = np.clip(zoomFactor, minZoom, maxZoom)

            print("Zoom Factor:", zoomFactor)
            initialDistance = distance
            zooming = True
        else:
            initialDistance = None
            zooming = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # Apply Zoom
    imgCurrent = cv2.resize(imgCurrent, (0, 0), fx=zoomFactor, fy=zoomFactor)
    zoomH, zoomW, _ = imgCurrent.shape
    if zoomFactor > 1.0:
        # Center cropped region of zoomed image to fit screen
        startX = (zoomW - width) // 2
        startY = (zoomH - height) // 2
        imgCurrent = imgCurrent[startY:startY + height, startX:startX + width]

    # Draw annotations
    for annotation in annotations:
        for i in range(1, len(annotation)):
            if annotation[i - 1] and annotation[i]:
                cv2.line(imgCurrent, annotation[i - 1], annotation[i], colors[colorIndex], brushSizes[brushSizeIndex])

    # Display the small camera feed in the presentation
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    imgCurrent = cv2.resize(imgCurrent, (width, height))

    # Calculate accuracy
    if totalGestures > 0:
        accuracy = (correctGestures / totalGestures) * 100
        cv2.putText(imgCurrent, f"Accuracy: {accuracy:.2f}%", (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
