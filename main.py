# pip install opencv-python
import cv2
import glob
import os
import time
from emailing import send_email
from threading import Thread


def clean_images_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


def send_and_clean(image_path: str):
    send_email(image_path)
    clean_thread = Thread(target=clean_images_folder)
    clean_thread.daemon = True
    clean_thread.start()


video = cv2.VideoCapture(0)  # 0 for default camera, 4 for external camera
time.sleep(1)
initialized = False
inside = False
img_counter = 0
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
    rectangles = None
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangles = cv2.rectangle(
            frame, (x, y), (x+w, y+h), (127, 255, 127), 3)

    if rectangles is not None and rectangles.any():
        inside = True
        cv2.imwrite(f"images/intruder_{str(img_counter).zfill(8)}.png", frame)
        img_counter += 1
    elif inside:
        all_images = glob.glob("images/*.png")
        all_images.sort()
        send_and_clean_thread = Thread(target=send_and_clean, args=(
            all_images[int(len(all_images) / 2)],))  # Comma is essential; it indicates that the argument is a tuple
        send_and_clean_thread.daemon = True
        inside = False
        send_and_clean_thread.start()

    cv2.imshow("Capturing", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
