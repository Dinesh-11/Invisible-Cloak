# Import Library
import cv2
import numpy as np
import time

# Access webcam - 0:Default webcam
cap = cv2.VideoCapture("Resources/input.mp4")
time.sleep(3)

background = 0
# Captured background
for i in range(30):
    success, background = cap.read()

# Runs until the webcam is activated
while (cap.isOpened()):

    success, img = cap.read()
    if (not success):
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # HSV values range for detecting red
    lower_red = np.array([0, 120, 70])
    higher_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, higher_red)

    lower_red = np.array([170, 120, 70])
    higher_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, higher_red)

    mask1 = mask1 + mask2

    # remove noise
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=2)

    # everything except clock
    mask2 = cv2.bitwise_not(mask1)

    result1 = cv2.bitwise_and(background, background, mask=mask1)
    result2 = cv2.bitwise_and(img, img, mask=mask2)
    final_output = cv2.addWeighted(result1, 1, result2, 1, 0)

    cv2.imshow("Output", final_output)
    k = cv2.waitKey(30)
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
