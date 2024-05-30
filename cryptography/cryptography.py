import random

import cv2
import numpy as np
import os


def saveShares(privateEncrypted: np.ndarray, publicEncrypted: np.ndarray):
  #  os.remove('/home/djikey/IdeaProjects/computer_vision/' + dictFileName)
    cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/private_encrypted.jpg', privateEncrypted)
    cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/public_encrypted.jpg', publicEncrypted)



def encryptImage(img):
    # Конвертация в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Конвертация в черно-белое представление
    im_bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
    arr = np.array(im_bw, np.uint8)
#    os.remove('/home/djikey/IdeaProjects/computer_vision/original_bw.jpg')
    cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/original_bw.jpg', arr)

    black_ciphers = [
        ([255, 0, 255, 0], [0, 255, 0, 255]),
        ([255, 0, 0, 255], [0, 255, 255, 0]),
        ([255, 255, 0, 0], [0, 0, 255, 255]),
        ([0, 0, 255, 255], [255, 255, 0, 0]),
        ([0, 255, 255, 0], [255, 0, 0, 255]),
        ([0, 255, 0, 255], [255, 0, 255, 0])
    ]
    white_ciphers = [
        ([255, 0, 255, 0], [255, 0, 255, 0]),
        ([255, 0, 0, 255], [255, 0, 0, 255]),
        ([255, 255, 0, 0], [255, 255, 0, 0]),
        ([0, 0, 255, 255], [0, 0, 255, 255]),
        ([0, 255, 255, 0], [0, 255, 255, 0]),
        ([0, 255, 0, 255], [0, 255, 0, 255])
    ]

    def encrypt(pixel):
        if (pixel == 255):
            return black_ciphers[random.randint(0, len(black_ciphers) - 1)]
        else:
            return white_ciphers[random.randint(0, len(white_ciphers) - 1)]

    rows, cols, _ = img.shape
    privateEncrypted = []
    publicEncrypted = []
    privateEncryptedBuffer = []
    publicEncryptedBuffer = []

    for (x, y), pixel in np.ndenumerate(arr):
        encr_private, encr_public = encrypt(pixel)
        if y == cols - 1:
            privateEncryptedBuffer = privateEncryptedBuffer + encr_private
            publicEncryptedBuffer = publicEncryptedBuffer + encr_public
            privateEncrypted.append(privateEncryptedBuffer)
            publicEncrypted.append(publicEncryptedBuffer)
            privateEncryptedBuffer = []
            publicEncryptedBuffer = []
        else:
            privateEncryptedBuffer = privateEncryptedBuffer + encr_private
            publicEncryptedBuffer = publicEncryptedBuffer + encr_public

    return (np.array(privateEncrypted), np.array(publicEncrypted))


def identify_pixel_type(encoded_pixel_in_public, encoded_pixel_in_private):
    value = encoded_pixel_in_public.dot(encoded_pixel_in_private)
    if (value == 0):
        return 255
    else:
        return 0


def decryptImage(privateEncrypted: np.ndarray, publicEncrypted: np.ndarray):

    saveShares(privateEncrypted, publicEncrypted)

    acc = []
    rowBuffer = []
    for rowIndex, encodedPr in enumerate(privateEncrypted, 0):
        encodedPub = publicEncrypted[rowIndex]
        index = 0
        accumulatedIndex = 0
        privBuffer = []
        pubBuffer = []
        while (index < len(encodedPr)):
            privPart = encodedPr[index]
            pubPart = encodedPub[index]
            index = index + 1
            if (accumulatedIndex == 3):
                privBuffer.append(privPart)
                privChiperNp = np.array(privBuffer)
                pubBuffer.append(pubPart)
                pubChiperNp = np.array(pubBuffer)
                pixel = identify_pixel_type(privChiperNp, pubChiperNp)
                rowBuffer.append(pixel)
                privBuffer = []
                pubBuffer = []
                accumulatedIndex = 0
            else:
                privBuffer.append(privPart)
                pubBuffer.append(pubPart)
                accumulatedIndex = accumulatedIndex + 1

        acc.append(rowBuffer)
        rowBuffer = []

    return np.array(acc)

img = cv2.imread('/home/djikey/IdeaProjects/computer_vision/original.jpg')

privateEncrypted, publicEncrypted = encryptImage(img)
decrypted_as_np_array = decryptImage(privateEncrypted, publicEncrypted)

# os.remove('/home/djikey/IdeaProjects/computer_vision/encoded_bw.jpg')
cv2.imwrite('/home/djikey/IdeaProjects/computer_vision/encoded_bw.jpg', decrypted_as_np_array)
