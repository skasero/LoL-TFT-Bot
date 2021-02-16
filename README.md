# Leauge of Legends TFT Bot
A simple bot to play LoL TFT (Teamfight Tacticts) games for you to quickly level up your TFT Pass. The bot will queue matches and surrender as soon as possible (10 minutes) before starting a new queue. Based on the current seasons, you need to play about 200 matches assuming you get no points from any missions. 

## Installation
There is no need to install anything, this bot is in written in Python and compiled into an executable to run for Microsoft Windows. 

## Usage
To use this bot, the LoL client will need to have already been open and at the point where you can click "Find Match" for a TFT game. Be in the same spot as the image below.
![Image of League client](https://github.com/skasero/LoL-TFT-Bot/blob/main/GitHub%20Resources/START.png)

You will also need to use Windows Command Prompt (CMD) to start the bot.  
Go to where you downloaded the TFT-Bot.exe file and launch a Command Prompt. 
The bot does take an optional parameter which is the number of iterations to run the bot for.

```bash
TFT-Bot.exe <iterations>
```

Once you execute the bot, the program does a search to see what resolution you have set for the LoL client. Currently supported resolutions are:   
1600 x 900  
1280 x 720  
1024 x 576

These resolutions are for the client and not once in-game.

## Video
[insert video]

## Known Issues
I have run into an issue where the bot will get stuck in an infinite queue timer. It seems that once the LoL client gets in this state, the user cannot exit queue and has to force close the LoL client.

## TODO
Add the ability for the user to click on the executable file and ask the user to input how many iterations to run the bot for. 
<!--Using pyinstaller to create '.exe'  
Command: pyinstaller -F --icon "images/icon.ico" --add-data "images/*.png;." --name TFT-Bot main.py-->
