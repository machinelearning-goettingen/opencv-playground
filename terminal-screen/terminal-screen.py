#!/usr/bin/env python3

import cv2
import numpy as np


# example with working image
orig = cv2.imread("data/IMG_6209.jpg", 1)

# example with problematic image (more than 1 rect, rects with more than 4 corner points)
# orig = cv2.imread("data/IMG_6122.jpg", 1)

im = orig.copy()
height, width, channels = im.shape

# cv2.imshow('image', cv2.resize(im, (int(1800), int(1200))))

kernel = np.ones((5, 5), np.uint8)

im = cv2.dilate(im, kernel)
im = cv2.erode(im, kernel)
# im = cv2.bilateralFilter(im, 5, 2, 2)
im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
im = cv2.inRange(im, np.array(
    [180.0 / 2, 40.0, 90.0, 0.0]), np.array([250.0 / 2, 255.0, 255.0, 1.0]))

# contours = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
contours, _ = cv2.findContours(
    im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result = []
visual = orig.copy()
for cnt in contours:

    area = cv2.contourArea(cnt)
    if(area > 10000):

        hull = cv2.convexHull(cnt)
        approx2 = cv2.approxPolyDP(
            hull, 0.01*cv2.arcLength(hull, True), True)

        visual = cv2.drawContours(
            visual, [approx2], 0, (0, 0, 255), thickness=6)

        if(len(approx2) != 4):
            print("bad length: ", len(approx2))

        # FIXME: do s.th useful if there are more than 4 points
        result.append(approx2)


if(len(result) > 1):
    print("multiple rects found: ", len(result))


cv2.imshow('visual', cv2.resize(visual, (int(1800), int(1200))))


# FIXME: do s.th useful if there is more than 1 rect (for now: take the first)
corners = result[0]

# FIXME: make sure the order of corners is correct, for now ignore
src = np.array([
    [corners[0][0][0], corners[0][0][1]],
    [corners[1][0][0], corners[1][0][1]],
    [corners[2][0][0], corners[2][0][1]],
    [corners[3][0][0], corners[3][0][1]]],
    dtype="float32")

dst = np.array([
    [width - 1, 0],
    [width - 1, height - 1],
    [0, height - 1],
    [0, 0]], dtype="float32")

print("transform")
print(src)
print("to")
print(dst)
transform = cv2.getPerspectiveTransform(src, dst)
corrected = cv2.warpPerspective(orig, transform, (width, height))


cv2.imshow('corrected', cv2.resize(corrected, (int(1800), int(1200))))
cv2.waitKey(0)
cv2.destroyAllWindows()
