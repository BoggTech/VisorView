# Visor-View
Originally a quick program I threw together for a friend, VisorView allows you to view, pose and screenshot animations 
on Toontown Rewritten cogs.

# Usage
## Prerequisites
Please ensure you have [Python 3](https://www.python.org/downloads/) installed before continuing. As well as this, please ensure you have Panda3D 
installed as a python module by running `py -m pip install Panda3D` (replace py if you know you use a different alias, 
i.e. python3, python). 

This command should be run in your **terminal**, if you use Linux, or your **command prompt** if you use Windows. The 
command prompt can be accessed by accessing the run dialog (Ctrl + R) and typing `cmd.exe`.

## Running
You can run the program by double-clicking the provided .bat file in the `scripts` directory (on windows) or by running 
`py main.py`, from the main directory, in your terminal/command prompt. You should be greeted with a graphics window 
displaying a t-posing cog. If you have a custom Toontown Rewritten install location, you will instead be prompted to
locate your game files manually.

![A windows error prompt, asking the user if they wish to locate their game files manually after the program
had failed to find them.](assets/prompt.png)

## Controls
The following inputs are available:
Key              | Action
---------------- | -------------
Space            | Cycle between current set of cogs.
Left/Right Arrow | Ditto, but left arrow will allow you to back to a previous cog in the set.
Up/Down Arrow    | Cycle through available cog sets.
1                | Switch active set to Supervisors.
2                | Switch active set to Sellbots.
3                | Switch active set to Cashbots.
4                | Switch active set to Lawbots.
5                | Switch active set to Bossbots.
6                | Switch active set to Cog Bosses.
7                | Switch active set to Misc.
S                | Toggle Shadow. The drop-shadow below the cog will be toggled on/off (if possible).
Control+S        | Toggle Skelecog (if possible)
Control+H        | Toggle Head. The cog's head will be toggled on/off (if possible).
Control+B        | Toggle Body. The cog's body/suit will be toggled on/off (if possible).
A                | View animation list. This list can be scrolled, and entries can be clicked to switch the active animation. **Some controls are disabled when this menu is open!**
P                | Toggle Pose Mode. When pose mode is active, the cog's animation will pause, and the scrollwheel can be used to cycle through the animation's frames. Pressing it again disables posing, and the actor/part will hang on the last frame you posed it at.
B                | Toggle animation smoothing.
F9               | Take screenshot. This will be stored to the `screenshots` directory by default.
Control+Z        | Reset to default camera position, positioning it directly in front of the cog.
Mousewheel       | Can be used with the animations menu or pose mode. See **p** and **a** controls for instructions.

See the gif below for controlling the camera with your mouse.

![An animated gif of a Toontown Rewritten cog. The camera is being manipulated by the mouse movement, both rotationally 
and positionally.](assets/camera.gif)

# USAGE FAQ
## What cogs are available?
From top to bottom:
- Five supervisors, including angry foreman.
- All sellbots, including the foreman and V.P.
- All cashbots, including the auditor and C.F.O.
- All lawbots, including the clerk and C.J.
- All bossbots, including the president and C.E.O.
- Misc actors: Goons, The Boiler and the Field Office.
- Bosses: V.P., C.F.O., C.J., C.E.O.

Sets of cogs can be traversed with the up/down arrow keys. Individual cogs can be traversed with left/right.

Additionally, each standard cog can be swapped with their skelecog using Control+S.

## How do I animate the cog? How do I use "pose mode"?
Pressing **A** on your keyboard will bring up a scrolling menu of valid animation names to use. Press any to apply it to
the actor. When an animation is applied to the actor, you can then press **P** to pose them on any frame. Use your
mousewheel to increase or decrease the frame you're on.

Please note that multi-part actors, such as the cog bosses, will first prompt you to select a part of the model to
animate/pose.

# TECHNICAL FAQ
## I'm not familiar with GitHub. How do I download the code?
If you don't know how to use git, you can download a zipped version of the code from the main page:

![An animated gif of the main repository page where a cursor comes up from the bottom of the screen, clicks the green 
'code' button and moves down to click 'Download ZIP'.](assets/downloading.gif)

You can also [click here](https://github.com/BoggTech/VisorView/archive/refs/heads/main.zip) to download the zip.

Extract this into a folder of your choosing, and follow the steps outlined in **Usage**.

## I did everything, but I'm having errors.

Feel free to register a github account and write an [issue](https://github.com/BoggTech/VisorView/issues/new/choose). I'll try fix it if it's a problem, or guide you if 
it's not.

# Acknowledgements

Special thanks to Panda3D, Python and their contributors. 

Toontown Online and Toontown Rewritten assets belong to their respective owners. Thank you to all of the artists and 
animators for their work on the cogs, as well as the rest of the Toontown team!