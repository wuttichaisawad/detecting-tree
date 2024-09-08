import cv2
import numpy as np
import os

def process_image(filepath, filename, upload_folder):
    img = cv2.imread(filepath)
    height, width, _ = img.shape
    boundaries = [height * i // 4 for i in range(1, 4)]

    for boundary in boundaries:
        cv2.line(img, (0, boundary), (width, boundary), (0, 0, 255), 1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 175])
    upper_white = np.array([270, 50, 255])

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    kernel = np.ones((2, 2), np.uint8)
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 20
    counts = {"Top": 0, "Middle": 0, "Bottom": 0, "Footer": 0}

    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            M = cv2.moments(cnt)
            cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            result = ("Top" if cY < boundaries[0] else
                      "Middle" if cY < boundaries[1] else
                      "Bottom" if cY < boundaries[2] else
                      "Footer")

            counts[result] += 1
            cv2.putText(img, result, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)

    result_filename = 'result_' + filename
    result_image_path = os.path.join(upload_folder, result_filename)
    cv2.imwrite(result_image_path, img)
    
    return result_image_path, counts
