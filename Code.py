import cv2
import numpy as np
import pyautogui
import time

# Constants
MIN_AREA = 10000 # Minimum contour area to be considered as motion

APP_CHANGE_DELAY = 1  # Delay in seconds before switching apps

# Initialize camera
cap = cv2.VideoCapture(0)

# Create background subtractor
background_subtractor = cv2.createBackgroundSubtractorMOG2() 

# Capture the initial frame for reference
ret, prev_frame = cap.read()

# Convert the initial frame to grayscale
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Flag to track if app change has occurred
app_changed = False

# Start the main loop
while True:
    
    # Capture current frame
    ret, frame = cap.read()

    # Convert current frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(prev_gray, gray)

    # Apply thresholding to remove noise and enhance the motion areas
    _, thresh = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)

    # Perform morphological operations to further reduce noise
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=2)

    # Find contours of the motion areas
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize motion detected flag
    motion_detected = False

    # Iterate over the contours and check if they meet the minimum area criterion
    for contour in contours:
        if cv2.contourArea(contour) > MIN_AREA:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            motion_detected = True

    # Display the resulting frame
    cv2.imshow("Motion Detection", frame)

    # Check if motion is detected and perform app change if it hasn't already occurred
    if motion_detected and not app_changed:
        print("Motion detected! Changing app...")
        pyautogui.hotkey('space') 
        pyautogui.hotkey('alt', 'tab')  # Simulate Alt + Tab key press
        pyautogui.hotkey('space') 
        app_changed = True

        # Wait for a few seconds before stopping the program
        cv2.waitKey(int(APP_CHANGE_DELAY * 1000))
        break

    # Update the previous frame and previous gray frame
    prev_frame = frame.copy()
    prev_gray = gray.copy()

    

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
