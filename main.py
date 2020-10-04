import os 
import numpy as np
import pyautogui
import cv2

import time

def runner(imagePath,iterations = 10):
    if(imagePath[-1] != '/'):
        imagePath = imagePath + '/'

    imageArray = ['find_match.png', 'accept.png', 'settings.png', 'surrender_p1.png', 'surrender_p2.png', 'ok.png', 'play_again.png']
    gameStartImage = imagePath + 'start.png'

    for i in range(iterations):
        print(f"Iteration: {i+1} / {iterations}")
        time.sleep(0.250)
        for image in imageArray:
            imageFile = imagePath + image
            if(image == 'accept.png'):
                acceptLocation = findImageLoop(imageFile,sleepTime=8,accuracy=0.85)
                clickImage(acceptLocation[0],acceptLocation[1])

                location = findImage(gameStartImage)
                while(location[0] == -1):
                    acceptLocation = findImage(imageFile)
                    clickImage(acceptLocation[0],acceptLocation[1],duration=0)
                    time.sleep(8)
                    location = findImage(gameStartImage)
            elif(image == 'settings.png'):
                print("The game has started, sleeping for 10 minutes...")
                for j in range(10):
                    print(f"Sleeping for {j+1} out of 10 minutes...", end='\r')
                    time.sleep(60)
                time.sleep(5) # Extra 5 seconds just in case
                location = findImageLoop(imageFile,sleepTime=3,accuracy=0.85)
            elif(image == 'ok.png'):
                location = findImageIterations(imageFile,iterations=6,sleepTime=5,accuracy=0.85)
            else:  
                location = findImageLoop(imageFile,sleepTime=20,accuracy=0.85)

            clickImage(location[0],location[1])

def clickImage(x, y, duration = 0.5):
    if(x != -1 and y != -1):
        print(f"Moving mouse to x: {x}, y: {y}")
        pyautogui.moveTo(x,y,duration)
        # pyautogui.click(button='left') # This doesn't click in league, it maybe too fast
        pyautogui.mouseDown()
        pyautogui.mouseUp()

def findImage(imagePath, accuracy = 0.85):
    # start = time.time()

    screenshot = pyautogui.screenshot()
    ssGrey = cv2.cvtColor(np.array(screenshot),cv2.COLOR_BGR2GRAY)
    # print(ssGrey.shape)

    template = cv2.imread(imagePath,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(ssGrey,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(f"Matching value to image is: {max_val}")

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    middle = (top_left[0] + (w // 2), top_left[1] + (h // 2))

    # print(top_left)
    # print(bottom_right)
    # print(middle)
    cv2.rectangle(ssGrey,top_left, bottom_right, 255, 1)
    cv2.rectangle(ssGrey,middle, middle, 255, 6)

    # cv2.imwrite('output.png',ssGrey)

    # end = time.time()
    # print(end - start)
    if(max_val < accuracy):
        return (-1,-1)
    return middle

def findImageLoop(image, sleepTime = 20, accuracy = 0.85):
    location = findImage(image,accuracy)
    while(location[0] == -1):
        print(f"Image: {image} was not found... sleeping for {sleepTime} seconds")
        time.sleep(sleepTime)
        location = findImage(image,accuracy)
    return location

def findImageIterations(image, iterations = 5, sleepTime = 5, accuracy = 0.85):
    for i in range(iterations):
        location = findImage(image,accuracy)
        if(location[0] != -1):
            break
        print(f"Image: {image} was not found... sleeping for {sleepTime} seconds")
        time.sleep(sleepTime)
    return location

if __name__ == '__main__':
    imagePath = 'images/'
    runner(imagePath)
    # time.sleep(2)
    # location = findImage('images/t.png')
    # clickImage(location[0],location[1])
    pass