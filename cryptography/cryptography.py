import random

import cv2
import numpy as np

img = cv2.imread('/home/djikey/IdeaProjects/computer_vision/cat.jpg')

# Prepare image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
im_bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
arr = np.array(im_bw, np.uint8)

black_ciphers = [
    ([1, 0, 1, 0], [0, 1, 0, 1]),
    ([1, 0, 0, 1], [0, 1, 1, 0]),
    ([1, 1, 0, 0], [0, 0, 1, 1]),
    ([0, 0, 1, 1], [1, 1, 0, 0]),
    ([0, 1, 1, 0], [1, 0, 0, 1]),
    ([0, 1, 0, 1], [1, 0, 1, 0])
]
white_ciphers = [
    ([1, 0, 1, 0], [1, 0, 1, 0]),
    ([1, 0, 0, 1], [1, 0, 0, 1]),
    ([1, 1, 0, 0], [1, 1, 0, 0]),
    ([0, 0, 1, 1], [0, 0, 1, 1]),
    ([0, 1, 1, 0], [0, 1, 1, 0]),
    ([0, 1, 0, 1], [0, 1, 0, 1])
]


def encrypt(pixel):
    if (pixel == 255):
        return black_ciphers[random.randint(0, len(black_ciphers) - 1)]
    else:
        return white_ciphers[random.randint(0, len(white_ciphers) - 1)]

private = {}
public = {}

rows, cols = arr.shape
for i in range(rows):
    for j in range(cols):
        pixel = arr[i,j]
        print(i, j, pixel)
        encr_private, encr_public = encrypt(pixel)
        private[(i,j)] = encr_private
        public[(i,j)] = encr_public

