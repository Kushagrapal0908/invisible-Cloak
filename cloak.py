import cv2
import numpy as np
import time

# In order to check the cv2 version
print(cv2.__version__)

# Taking "video.mp4" as input. Modify this path according to your needs.
capture_video = cv2.VideoCapture(0)

# Give the camera time to warm up
time.sleep(1)
count = 0
background = 0

# Capturing the background in a loop
for i in range(5):
    return_val, background = capture_video.read()
    if return_val == False:
        continue

background = np.flip(background, axis=1)  # Flipping the frame
# Define the HSV range for dark red
lower_dark_red = np.array([0, 40, 40])
upper_dark_red = np.array([10, 255, 255])

# We are reading from the video
while capture_video.isOpened():
    return_val, img = capture_video.read()
    if not return_val:
        break
    count = count + 1
    img = np.flip(img, axis=1)

    # Convert the image - BGR to HSV for better color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a mask for dark red color
    mask = cv2.inRange(hsv, lower_dark_red, upper_dark_red)

    # Refine the mask corresponding to the detected dark red color
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

    # Invert the mask to get the backgroundpip
    mask_inv = cv2.bitwise_not(mask)

    # Generate the final output
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(img, img, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Creating a window for displaying the processed video
    cv2.namedWindow("INVISIBLE MAN", cv2.WINDOW_NORMAL)

    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
    if k == 27:  # Exit the loop when the 'Esc' key is pressed
        break

# Release the video capture and close the OpenCV windows
capture_video.release()
cv2.destroyAllWindows()
