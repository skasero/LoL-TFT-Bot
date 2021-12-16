import os
import sys
import numpy as np
import pyautogui
import cv2
import time
import imutils
import datetime

# Default verbose value
VERBOSE = 0

class TFTBot:
    client_scale = None
    ingame_scale = None
    imagePath = None

    # Used to get scale of client
    def __init__(self, imagePath):
        self.imagePath = imagePath

        img_init = self.imagePath + 'find_match.png'
        print("Starting up TFT-Bot")
        self.setScale(img_init,0)

    def setScale(self,image,scale_version):
        # This screenshot of one monitor only
        screenshot = pyautogui.screenshot()
        ssGrey = cv2.cvtColor(np.array(screenshot),cv2.COLOR_BGR2GRAY)

        template = cv2.imread(image,0)

        best_scale = None
        best_max_val = -1

        for scale in np.linspace(0.4, 1.0, 75)[::-1]:
            resized = imutils.resize(template, width = int(
                template.shape[1] * scale))
            res = cv2.matchTemplate(ssGrey,resized,cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if (VERBOSE >= 2):
                print(f"Matching value to image is: {max_val}")
            if(max_val > best_max_val):
                best_max_val = max_val
                best_scale = scale

        if(best_max_val >= 0.80):
            if (VERBOSE >= 1):
                print(f"Best Scale value: {best_scale} with best image",
                      f"accuracy of: {best_max_val}")
            # This is for the client_scale
            if(scale_version == 0):
                self.client_scale = best_scale
            # This is for the ingame_scale
            elif(scale_version == 1):
                self.ingame_scale = best_scale
        else:
            raise Exception("Could NOT find image scaling, unable to continue.")

    def runner(self, iterations = 3):
        client_imageArray= ['find_match.png', 'accept.png', 'ok.png',
                            'play_again.png']
        ingame_imageArray= ['settings.png', 'surrender_p1.png',
                            'surrender_p2.png']
        full_imageArray = ['find_match.png', 'accept.png', 'settings.png',
                           'surrender_p1.png', 'surrender_p2.png', 'ok.png',
                           'play_again.png']
        gameStartImage = self.imagePath + 'start.png'
        playAgainImage = self.imagePath + 'play_again.png'
        cancelQueueImage = self.imagePath + 'cancel_queue.png'
        surrenderP1Image = self.imagePath + 'surrender_p1.png'

        for i in range(iterations):
            print(f"Iteration: {i+1} / {iterations}")
            time.sleep(2)

            for attempt in range(3):
                gameStarted = False

                for image in full_imageArray:
                    location = (-1,-1) # null tuple
                    imageFile = self.imagePath + image
                    time.sleep(0.5)
                    if(image == 'accept.png'):
                        # acceptLocation = self.findImageLoop(imageFile,self.client_scale,sleepTime=8,accuracy=0.80)
                        # self.clickImage(acceptLocation[0],acceptLocation[1])
                        print("Waiting for the game to start")

                        # This loop is used for if a user gets stuck in queue
                        # for more than 5 minutes, it will attempt to try and
                        # cancel the queue and restart 3 times before exiting
                        # the programming
                        fiveMinQueue = datetime.datetime.now() + \
                            datetime.timedelta(minutes=5)

                        # This loop is meant for both the accept button and to
                        # get the in_game scale.
                        while(datetime.datetime.now() < fiveMinQueue):
                            try:
                                # Accept button
                                location = self.findImage(imageFile,
                                                          self.client_scale)

                                # Used to reset timer
                                if(location[0] != -1):
                                    fiveMinQueue = datetime.datetime.now() + \
                                        datetime.timedelta(minutes=5)

                                self.clickImage(location[0], location[1],
                                                duration=0)
                                time.sleep(6)
                                # Used to get in_game scale
                                self.setScale(gameStartImage,1)
                                # Also this part of the code will not reach
                                # unless setScale() passes and find the image
                                # in-game
                                location = self.findImage(gameStartImage,
                                                          self.ingame_scale)
                                gameStarted = True
                                break
                            except:
                                pass

                        # This is the case where the bot got stuck in queue, restart the queue
                        if(gameStarted == False):
                            print(f"Bot got stuck trying to find a game,",
                                  f"restarting queue now.",
                                  f"Attempts: {attempt+1} / 3")
                            cancelQueueLocation = self.findImage(
                                cancelQueueImage, self.client_scale)
                            self.clickImage(cancelQueueLocation[0],
                                            cancelQueueLocation[1], duration=0)
                            break

                        # location = self.findImage(gameStartImage)
                        # while(location[0] == -1):
                        #     acceptLocation = self.findImage(imageFile)
                        #     self.clickImage(acceptLocation[0],acceptLocation[1],duration=0)
                        #     time.sleep(8)
                        #     location = self.findImage(gameStartImage)
                    elif(image == 'settings.png'):
                        print("The game has started, sleeping for 10 minutes")
                        for j in range(10):
                            print(f"Sleeping for {j+1} out of 10 minutes...",
                                  end='\r')
                            time.sleep(60)
                        print("")
                        time.sleep(5) # Extra 5 seconds just in case
                        location = self.findImageLoop(imageFile,
                                                      self.ingame_scale,
                                                      sleepTime=3,
                                                      accuracy=0.80)
                    elif(image == 'ok.png'):
                        playAgainLocation = self.findImage(playAgainImage,
                                                           self.client_scale)
                        while(playAgainLocation[0] == -1):
                            location = self.findImage(imageFile,
                                                      self.client_scale)
                            self.clickImage(location[0],
                                            location[1])
                            time.sleep(5)
                            playAgainLocation = self.findImage(
                                playAgainImage, self.client_scale)
                    elif(image in client_imageArray):
                        location = self.findImageLoop(imageFile,
                                                      self.client_scale,
                                                      sleepTime=15,
                                                      accuracy=0.80)
                    elif(image in ingame_imageArray):
                        location = self.findImageLoop(imageFile,
                                                      self.ingame_scale,
                                                      sleepTime=15,
                                                      accuracy=0.80)
                    else:
                        raise Exception("This should never be reached and "
                                        "something wrong has happened")

                    self.clickImage(location[0],location[1])

                    # This is a special case where sometimes settings isn't
                    # clicked on
                    if(image == 'settings.png'):
                        surrenderLocation = self.findImage(surrenderP1Image,
                                                           self.ingame_scale)
                        while(surrenderLocation[0] == -1):
                            location = self.findImage(imageFile,
                                                      self.ingame_scale)
                            self.clickImage(location[0], location[1])
                            time.sleep(1)
                            surrenderLocation = self.findImage(
                                surrenderP1Image, self.ingame_scale)

                # This means that it didn't find a game before the last iteration
                if(attempt == 2 and gameStarted == False):
                    raise Exception("Bot got stuck in infinite queue, please "
                                    "wait and restart bot.")

                # This if for when the bot runs correctly
                if(gameStarted == True):
                    break

    def clickImage(self, x, y, duration = 0.5):
        if(x != -1 and y != -1):
            if (VERBOSE >= 1):
                print(f'Moving mouse to x: {x}, y: {y}')
            pyautogui.moveTo(x,y,duration)
            # This doesn't click in league, it maybe too fast
            # pyautogui.click(button='left')

            # Added a right click to make sure that the bot is clicked ingame
            # before executing a left click
            pyautogui.mouseDown(button='right')
            pyautogui.mouseUp(button='right')
            time.sleep(0.25)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

    def findImage(self, imagePath, scale, accuracy = 0.80):
        # start = time.time()

        # This screenshot of one monitor only
        screenshot = pyautogui.screenshot()
        ssGrey = cv2.cvtColor(np.array(screenshot),cv2.COLOR_BGR2GRAY)

        template = cv2.imread(imagePath,0)
        resized = imutils.resize(template, width = int(
            template.shape[1] * scale))
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(ssGrey,resized,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if (VERBOSE >= 1):
            print(f'Matching value to image is: {max_val}')

        wScale = int(w * scale)
        hScale = int(h * scale)

        top_left = max_loc
        bottom_right = (top_left[0] + wScale, top_left[1] + hScale)
        middle = (top_left[0] + (wScale // 2), top_left[1] + (hScale // 2))

        # print(top_left)
        # print(bottom_right)
        # print(middle)
        # cv2.rectangle(ssGrey,top_left,bottom_right,255,1)
        # cv2.rectangle(ssGrey,middle,middle,255,6)

        # cv2.imwrite('output.png',ssGrey)

        # end = time.time()
        # print(end - start)
        if(max_val < accuracy):
            return (-1,-1)
        return middle

    def findImageLoop(self, image, scale, sleepTime = 15, accuracy = 0.80):
        base=os.path.basename(image)
        location = self.findImage(image,scale,accuracy)
        while(location[0] == -1):
            print(f"Image: {base} was not found... sleeping for",
                  f"{sleepTime} seconds")
            time.sleep(sleepTime)
            location = self.findImage(image,scale,accuracy)
        return location

    def findImageIterations(self, image, scale, iterations = 5, sleepTime = 5, accuracy = 0.80):
        base=os.path.basename(image)
        for i in range(iterations):
            location = self.findImage(image, scale, accuracy)
            if(location[0] != -1):
                return location
            print(f"Image: {base} was not found... sleeping for ",
                  f"{sleepTime} seconds")
            time.sleep(sleepTime)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    iterations = 0
    if (len(sys.argv) == 2):
        if (sys.argv[1] != '-v' and sys.argv[1] != '-vv'):
            iterations = int(sys.argv[1])
    else:
        iterations = int(input('Enter the number of iterations to run the TFT-Bot for: '))

    if (len(sys.argv) == 2):
        if (sys.argv[1] != '-v'):
            VERBOSE = 1
        elif (sys.argv[1] != '-vv'):
            VERBOSE = 2

    # Used for non-pyinstaller version
    imagePath = resource_path('images/')

    # Used for pyinstaller version
    # imagePath = resource_path('')

    tft = TFTBot(imagePath)
    tft.runner(iterations)

    print("TFT-Bot has finished")