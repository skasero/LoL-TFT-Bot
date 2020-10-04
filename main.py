import os 
import numpy as np
import pyautogui
import cv2

import time

def runner(imagePath,iterations = 10):
    if(imagePath[-1] != '/'):
        imagePath = imagePath + '/'

    imageArray = ['find_match.png', 'accept.png', 'surrender_p1.png', 'surrender_p2.png', 'ok.png', 'play_again.png']
    gameStartImage = imagePath + 'start.png'

    for i in range(iterations):
        for image in imageArray:
            imageFile = imagePath + image
            if(image == 'accept.png'):
                location = findImageLoop(imageFile,sleepTime=8,accuracy=0.85)
                clickImage(location[0],location[1])

                checkLocation = findImage(gameStartImage)
                while(checkLocation[0] == -1):
                    location = findImage(imageFile)
                    clickImage(location[0],location[1],duration=0)
                    time.sleep(8)
                    checkLocation = findImage(gameStartImage)
            elif(image == 'surrender_p1.png'):
                print("The game has started, sleeping for 10 minutes and 30 seconds...")
                waitTime = (60*10) + 30 # 10 minutes + 30 seconds for safety
                time.sleep(waitTime)
                pyautogui.press('esc')
                location = findImageLoop(imageFile,sleepTime=3,accuracy=0.85)
                clickImage(location[0],location[1])
            else:  
                location = findImageLoop(imageFile,sleepTime=30,accuracy=0.85)
                clickImage(location[0],location[1])

def clickImage(x, y, duration = 0.5):
    if(x != -1 and y != -1):
        print(f"Moving mouse to x: {x}, y: {y}")
        pyautogui.moveTo(x,y,duration)
        pyautogui.click(button='left')

def findImage(imagePath, accuracy = 0.85):
    # start = time.time()

    screenshot = pyautogui.screenshot()
    ssGrey = cv2.cvtColor(np.array(screenshot),cv2.COLOR_BGR2GRAY)
    # print(ssGrey.shape)

    template = cv2.imread(imagePath,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(ssGrey,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    middle = (top_left[0] + (w // 2), top_left[1] + (h // 2))

    # print(top_left)
    # print(bottom_right)
    print(middle)
    cv2.rectangle(ssGrey,top_left, bottom_right, 255, 1)
    cv2.rectangle(ssGrey,middle, middle, 255, 6)

    # cv2.imwrite('output.png',ssGrey)

    # end = time.time()
    # print(end - start)
    if(max_val < accuracy):
        return (-1,-1)
    return middle

def findImageLoop(image, sleepTime = 30, accuracy = 0.85):
    location = findImage(image,accuracy)
    while(location[0] == -1):
        print(f"Image: {image} was not found... sleeping for {sleepTime} seconds")
        time.sleep(sleepTime)
        location = findImage(image,accuracy)
    return location

if __name__ == '__main__':
    imagePath = 'images/'
    runner(imagePath)
    # location = findImage('images/a.png')
    # clickImage(location[0],location[1])
    pass