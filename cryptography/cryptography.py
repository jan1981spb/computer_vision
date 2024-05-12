import random

import cv2
import numpy as np

def encryptImage(img):
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

    privateEncrypted = {}
    publicEncrypted = {}

    rows, cols = arr.shape
    for i in range(rows):
        for j in range(cols):
            pixel = arr[i, j]
          #  print(i, j, pixel)
            encr_private, encr_public = encrypt(pixel)
            privateEncrypted[(i, j)] = encr_private
            publicEncrypted[(i, j)] = encr_public

    return (privateEncrypted, publicEncrypted)



def decryptImage(privateEncrypted: dict, publicEncrypted: dict, shape: tuple):

    def identify_pixel_type(encoded_pixel_in_public: list, encoded_pixel_in_private: list):
        value = 0;
        for el_public in encoded_pixel_in_public:
            for el_private in encoded_pixel_in_private:
                value = value + el_private + el_public
        if (value == 0):
            return 255
        else:
            return 0

    intermediate_arr = []
    output_arr = np.empty((shape), dtype = int)

    for coordinate, encoded_pixel_in_private in privateEncrypted.items():
        encoded_pixel_in_public = publicEncrypted[coordinate]
        pixel = identify_pixel_type(encoded_pixel_in_public, encoded_pixel_in_private)
        intermediate_arr.append((coordinate, pixel))



img = cv2.imread('/home/djikey/IdeaProjects/computer_vision/cat.jpg')
privateEncrypted, publicEncrypted = encryptImage(img)
decryptImage(privateEncrypted, publicEncrypted, img.shape)