import numpy as np
import cv2 as cv
import sys

tracker = cv.TrackerKCF_create()
video = cv.VideoCapture(0)

while True:
    k, frame = video.read()
    cv.imshow('Tracking', frame)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

#selectROI settings
fromCenter = False
showCrosshair = False

bbox = cv.selectROI(frame, fromCenter, showCrosshair)
ok = tracker.init(frame, bbox)
cv.destroyWindow('ROI selector')

lines = 5
scale_x = int(bbox[2]) / lines
scale_y = int(bbox[3]) / lines

x = np.linspace(start = int(bbox[0]), stop = int(bbox[0] + bbox[2]), num = lines)
y = np.linspace(start = int(bbox[1]), stop = int(bbox[1] + bbox[3]), num = lines)

while True:
    ok, frame = video.read()
    ok, bbox = tracker.update(frame)
    
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]),
          int(bbox[1] + bbox[3]))

    cv.rectangle(frame, p1, p2, (0, 0, 255), 2, 2)

    for line in np.arange(0, lines):

        vline_p1 = (int(bbox[0] + (scale_x * line)), int(bbox[1]))
        vline_p2 = (int(bbox[0] + (scale_x * line)), int(bbox[1] + bbox[3]))
        hline_p1 = (int(bbox[0]), int(bbox[1] + (scale_y * line)))
        hline_p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + (scale_y * line)))

        cv.line(frame, vline_p1, vline_p2, (0, 0, 255), 2, 2)
        cv.line(frame, hline_p1, hline_p2, (0, 0, 255), 2, 2)

    cv.imshow('Tracking', frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
