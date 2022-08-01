import numpy as np
import cv2


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
    return dst


def split_image(image, list_points):
    parts = []
    for points in list_points:
        part = crop_one_detail(image, points)
        parts.append(part)
    return parts
