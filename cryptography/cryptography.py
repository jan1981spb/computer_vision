import random

import cv2
import numpy as np
import os

def saveShares(encrypted: dict, shape: tuple, dictFileName:str):
    rows, cols, _ = shape
    acc = []
    buffer1 = []
    buffer2 = []
    for coordinate, encoded_pixel_in_private in encrypted.items():

        x,y = coordinate
        if y == cols - 1:
            buffer1.append(encoded_pixel_in_private[0]*255)
            buffer1.append(encoded_pixel_in_private[1]*255)
            buffer2.append(encoded_pixel_in_private[2]*255)
            buffer2.append(encoded_pixel_in_private[3]*255)
            acc.append(buffer1)
            acc.append(buffer2)
            buffer1 = []
            buffer2 = []
        else:
            buffer1.append(encoded_pixel_in_private[0]*255)
            buffer1.append(encoded_pixel_in_private[1]*255)
            buffer2.append(encoded_pixel_in_private[2]*255)
            buffer2.append(encoded_pixel_in_private[3]*255)
    npArrayImage = np.array(acc)
    os.remove('/home/djikey/IdeaProjects/computer_vision/' + dictFileName)
    cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/' + dictFileName, npArrayImage)


def encryptImage(img):
    # Конвертация в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Конвертация в черно-белое представление
    im_bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
    arr = np.array(im_bw, np.uint8)
    os.remove('/home/djikey/IdeaProjects/computer_vision/original_bw.jpg')
    cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/original_bw.jpg', arr)


    black_ciphers = [
        (np.array([1, 0, 1, 0]), np.array([0, 1, 0, 1])),
        (np.array([1, 0, 0, 1]), np.array([0, 1, 1, 0])),
        (np.array([1, 1, 0, 0]), np.array([0, 0, 1, 1])),
        (np.array([0, 0, 1, 1]), np.array([1, 1, 0, 0])),
        (np.array([0, 1, 1, 0]), np.array([1, 0, 0, 1])),
        (np.array([0, 1, 0, 1]), np.array([1, 0, 1, 0]))
    ]
    white_ciphers = [
        (np.array([1, 0, 1, 0]), np.array([1, 0, 1, 0])),
        (np.array([1, 0, 0, 1]), np.array([1, 0, 0, 1])),
        (np.array([1, 1, 0, 0]), np.array([1, 1, 0, 0])),
        (np.array([0, 0, 1, 1]), np.array([0, 0, 1, 1])),
        (np.array([0, 1, 1, 0]), np.array([0, 1, 1, 0])),
        (np.array([0, 1, 0, 1]), np.array([0, 1, 0, 1]))
    ]

    def encrypt(pixel):
        if (pixel == 255):
            return black_ciphers[random.randint(0, len(black_ciphers) - 1)]
        else:
            return white_ciphers[random.randint(0, len(white_ciphers) - 1)]

    privateEncrypted = {}
    publicEncrypted = {}

    for (x,y), pixel in np.ndenumerate(arr):
            encr_private, encr_public = encrypt(pixel)
            privateEncrypted[(x, y)] = encr_private
            publicEncrypted[(x, y)] = encr_public

    saveShares(privateEncrypted, img.shape, 'private_shares.jpg')
    saveShares(publicEncrypted, img.shape, 'public_shares.jpg')

    return (privateEncrypted, publicEncrypted)



def decryptImage(privateEncrypted: dict, publicEncrypted: dict, shape: tuple):

    def identify_pixel_type(encoded_pixel_in_public, encoded_pixel_in_private):
        value = encoded_pixel_in_public.dot(encoded_pixel_in_private)
        if (value == 0):
            return 255
        else:
            return 0

    acc = []
    buffer = []
    cols = shape[1]

    for coordinate, encoded_pixel_in_private in privateEncrypted.items():
        encoded_pixel_in_public = publicEncrypted[coordinate]
        pixel = identify_pixel_type(encoded_pixel_in_public, encoded_pixel_in_private)

        x,y = coordinate
        if y == cols - 1:
            buffer.append(pixel)
            acc.append(buffer)
            buffer = []
        else:
            buffer.append(pixel)

    return np.array(acc)


img = cv2.imread('/home/djikey/IdeaProjects/computer_vision/original.jpg')

privateEncrypted, publicEncrypted = encryptImage(img)
decrypted_as_np_array = decryptImage(privateEncrypted, publicEncrypted, img.shape)

os.remove('/home/djikey/IdeaProjects/computer_vision/encoded_bw.jpg')
cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/encoded_bw.jpg', decrypted_as_np_array)



