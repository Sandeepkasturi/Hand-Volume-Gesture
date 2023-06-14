import cv2
import PySimpleGUI as sg
import pyautogui

# Constants for hand gesture recognition
UP_THRESHOLD = 150  # Raise hand above this threshold to increase volume
DOWN_THRESHOLD = 100  # Lower hand below this threshold to decrease volume

# Create GUI window
sg.theme("DarkAmber")
layout = [
    [sg.Text("Raise your hand to increase volume")],
    [sg.Text("Lower your hand to decrease volume")],
    [sg.Image(key="-IMAGE-")],
    [sg.Button("Exit")]
]
window = sg.Window("Hand Gesture Volume Control", layout)

# Initialize video capture device
cap = cv2.VideoCapture(0)

# Initialize variables
hand_detected = False

# Main loop
while True:
    event, values = window.read(timeout=20)
    
    # Check if "Exit" button is clicked or window is closed
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    
    # Read frame from video capture device
    ret, frame = cap.read()
    
    # Convert frame to grayscale for hand gesture recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect hand gestures
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Reset hand detection flag
    hand_detected = False
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:
            # Get bounding rectangle coordinates
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Check hand position and adjust volume accordingly
            if y < UP_THRESHOLD:
                pyautogui.press("volumeup")
                hand_detected = True
            elif y > DOWN_THRESHOLD:
                pyautogui.press("volumedown")
                hand_detected = True
    
    # Display the frame in the GUI window
    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["-IMAGE-"].update(data=imgbytes)

# Release the video capture device and close the GUI window
cap.release()
window.close()
