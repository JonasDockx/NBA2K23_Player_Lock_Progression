# NBA2K23_Player_Lock_Progression
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

### The Python Pillow library
This is a Python library that is necessary to run this script.  
It is very easy to install.  
Open the Command Prompt and type `pip install Pillow`.  
Once you've done this, you can run the Python script by double-clicking it.  
This will start the player progress tracker.  

#### The Wembanyama icon (optional)
Place the Wembanyama.ico file in the same directory as NBA2K23.py.
