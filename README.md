# League of Legends TFT Bot
A simple bot to play LoL TFT (Teamfight Tacticts) games for you to quickly level up your TFT Pass. The bot will queue matches and surrender as soon as possible (10 minutes) before starting a new queue. Based on the current seasons, you need to play about 200 matches assuming you get no points from any missions. 

## Installation
There is no need to install anything, this bot is in written in Python and compiled into an executable to run for Microsoft Windows. 

## Usage
To use this bot, the LoL launcher will need to have already been open and at the point where you can click "Find Match" for a TFT game. Be in the same spot as the image below.  
<img src=https://github.com/skasero/LoL-TFT-Bot/blob/main/GitHub%20Resources/START.png width="60%" height="60%">

You can either double-click on the TFT-Bot.exe or you can use use Windows Command Prompt (CMD) to start the bot.  
<!--Go to where you downloaded the TFT-Bot.exe file and launch a Command Prompt.  -->
The bot can take an optional parameter which is the number of iterations to run the bot for if you use CMD.

```bash
TFT-Bot.exe <iterations>
```

##### ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `Note:` This bot uses image processing. Do NOT cover the LoL launcher with another application.

Once you execute the bot, the program does a search to see what resolution you have set for the LoL launcher. Currently supported resolutions are:   
1600 x 900  
1280 x 720  
1024 x 576

These resolutions are for the launcher and not once in-game.

## Video
This is how to use the bot when using the CMD.  

<img src=https://j.gifs.com/ANw9Pj.gif width="50%" height="50%">

[Video Usage](https://streamable.com/sid1jy)

## Known Issues
I have run into an issue where the bot will get stuck in an infinite queue timer. It seems that once the LoL launcher gets in this state, the user cannot exit queue and has to force close the LoL launcher.

## TODO
~~Add the ability for the user to click on the executable file and ask the user to input how many iterations to run the bot for.~~ -Added in v1.1.6
<!--Using pyinstaller to create '.exe'  
Command: pyinstaller -F --icon "images/icon.ico" --add-data "images/*.png;." --name TFT-Bot main.py-->
