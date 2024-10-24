# pip install opencv-python
import cv2
import time

video = cv2.VideoCapture(4)  # 0 for default camera, 4 for external camera
time.sleep(1)
initialized = False
while True:
    # Catch frames one by one and compare with the first frame
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_gau = cv2.GaussianBlur(gray, (21, 21), 0)
    # Catch the very first frame to compare with
    if not initialized:
        first_gray_gau = gray_gau
        initialized = True
        continue
    delta = cv2.absdiff(first_gray_gau, gray_gau)
    thresh_frame = cv2.threshold(delta, 100, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=5)
    contours, check = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (127, 255, 127), 3)
    cv2.imshow("Capturing", frame)
    # cv2.imshow("Capturing", dil_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()

# print(check1)
# print(frame1)
