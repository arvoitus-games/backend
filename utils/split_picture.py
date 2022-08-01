import random

import numpy as np
import cv2

# img = cv2.imread("image.png")
# pts = np.array([[10,150],[150,100],[300,150],[350,100],[310,20],[35,10]])


def crop_one_detail(image, points):

    # Crop the bounding rect
    rect = cv2.boundingRect(points)
    x, y, w, h = rect
    cropped = image[y : y + h, x : x + w].copy()

    # Make mask
    pts = points - points.min(axis=0)

    mask = np.zeros(cropped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # Do bit-op
    dst = cv2.bitwise_and(cropped, cropped, mask=mask)

    tmp = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(dst)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    # cv2.imwrite("transparent_part.png", dst)
    return dst


# crop_one_detail(img, pts)


def split_image(image, list_points):
    parts = []
    for points in list_points:
        part = crop_one_detail(image, points)
        parts.append(part)
        # cv2.imwrite(str(random.randint(0,1000))+'cropeee.png', part)
    return parts


# split_image(img, [np.array([[10,150],[150,100],[300,150],[350,100],[310,20],[35,10]]),
#                   np.array([[10,150],[150,100],[300,150],[350,100],[310,400],[0,400]]),
#                   ], )
