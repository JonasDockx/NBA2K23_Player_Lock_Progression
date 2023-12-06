# NBA2K23 Player Lock Progression
Player lock progression system for NBA 2K MyLeague

This is based on an idea by [u/rustyhwe](https://www.reddit.com/r/NBA2k/comments/xl11pq/player_lock_progression_system "u/rustyhwe") on Reddit.  
Due to the MyCareer mode being so focused on VC, an alternative way of playing the game feels less like a grind.  
You can play MyLeague with Player lock, this achieves the same purpose as MyCareer, and you can upgrade attributes and badges based on how well you do in games.  

## What does this do?
Multiple players can be tracked with this Python script. They get stored in a database  
To start, you either need to create a player or select an already created player.  
Once you've done this, you get three options.  

The first option is to input the game statistics. You will be able to enter the amount of points, rebounds, assists, blocks, and steals you recorded in a game.  
You can also tick the boxes for possible awards you've won.  
Depending on the statistics you input here, you will get development points and badge points to spend.  
These can be spent on the below two things.  

The second option you get is to upgrade your attributes.  
You get an overview of all your current attributes and you can choose which ones to upgrade with your development points.  

The final option is to upgrade your badges.  
Badges can be upgraded using either development points or badge points.  

## What are the requirements?
### Python
This is a Python script. As such, it will need Python to run.  
Installing Python is fairly easy:  

**Download Python:**  
- Go to the [official Python website](https://www.python.org/downloads/).
- Click on the "Download Python" button. This will download the latest version of Python.

**Run the Installer:**  
- Once the download is complete, open the installer.
- Ensure that you check the box that says “Add Python to PATH” before clicking “Install Now”.

**Verify the Installation:**  
- Open Command Prompt and type `python --version`.
- If Python is successfully installed, you should see the version number.

#### The Python Pillow library
This is a Python library that is necessary to run this script.  
It is very easy to install.  
Open the Command Prompt and type `pip install Pillow`.  
Once you've done this, you can run the Python script by double-clicking it.  
This will start the player progress tracker.  

#### The Wembanyama icon (optional)
Place the Wembanyama.ico file in the same directory as NBA2K23.py.

## Possible future improvements - all help is welcome
### Executable (.exe) file
Making this into an executable file, would eliminate the need for people to install Python.
This is something I would like to do in the future, but I'd first want everything to be perfect.

### Have a better-looking layout
The program runs fine, the back-end should be well-established.
The front-end, however, is just based on some tkinter screens.
This does not look very modern, and can certainly be improved upon.

### Turning this into a mobile app
This would be the end goal. If people could open this app on their mobile phone, they could just run this script without Alt-Tabbing out of the game screen.
The game could just keep on running when entering all necessary information.

### User preferences
The way the program is set up now, the logic that is used is the one provided by rustyhwe on Reddit.
If people want to add more value to blocks, for example, this is not easily changed.
I would have to change the values in the script (or you could do it yourself, if you know your way around Python).
In an ideal world, someone should be able to use their own logic to determine the rate of progress.
If you want a double double to be worth 4 development points, rather than 3, who am I to disagree?
Or if you think upgrading an attribute below 70 should only cost half a development point rather than a full development point, this should be fine too.
That is all personal preference, and it would be easier if people had the choice to change the script to their preferences.

### Different game versions
This script is set up for NBA 2K23.
To use this script for NBA 2K24 should be fairly easy as well, but I would need to adjust some badges (that are present in NBA 2K24, but aren't in NBA 2K23).

### Getting game statistics automatically, thus eliminating manual input
All of this relies on manual user input.
It would be far easier if my script could just get the information straight from NBA 2K23 when it is running, especially when it comes to starting values, game statistics and awards.
I have nu clue how to go about this, so if someone could help me with this, that would be very helpful.

If that is too difficult, to get the starting values from 2kratings would already eliminate some manual input when entering a new player.
