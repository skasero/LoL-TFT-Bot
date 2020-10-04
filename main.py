import os 
import numpy as np
import pyautogui
import cv2

import time


def findImage(imagePath):
    # start = time.time()

    screenshot = pyautogui.screenshot()
    ssGrey = cv2.cvtColor(np.array(screenshot),cv2.COLOR_BGR2GRAY)
    # print(ssGrey.shape)

    template = cv2.imread(imagePath,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(ssGrey,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    middle = (top_left[0] + (w // 2), top_left[1] + (h // 2))


    print(top_left)
    print(bottom_right)
    print(middle)
    cv2.rectangle(ssGrey,top_left, bottom_right, 255, 1)
    cv2.rectangle(ssGrey,middle, middle, 255, 6)

    cv2.imwrite('output.png',ssGrey)


    # end = time.time()
    # print(end - start)
    pass


if __name__ == '__main__':
    findImage('images/a.png')
    pass