# GenCyber Coding Game  
  
This is a GUI Python 3 game written to display more advanced topics and abilities
Python has to offer. It was written to support Oahu's GenCyber camps to help teach
middle and high schoolers programming. 
  
# Usage  
  
`py Survival.py`  
  
The program will launch a basic login window. Enter the following user credentials:  
  
*  Username: Use any username you want, it is not checked by the program  
*  Password: magenta319clouds  
    
After successfully "logging in", the game will officially start, opening a new GUI
window. 

# How to Play  
  
The objective of the game is to complete all current quests. This is done by crafting
the necessary items and managing your health and hunger. If your hunger reaches 0, 
your health will start to decrease. If your health reaches 0, the game is over.  
  
The game is played through typing commands into the command bar at the bottom of the 
screen.  

Enter the following for help and information:  
`h` : View help menu for list of available commands.  
`q` : View current quests.  
`i` : View your current inventory.  
`c` : View crafting recipes. 

Each time a command is entered, your hunger will decrease. If you have 0 hunger, your
health will decrease with each command entered.


# Python 3 Obfuscation

This script utilizes obfuscation techniques to hide the functionality of the login
window. Some examples of obfuscation techniques used:
*  Importing libraries with nonsensical names  
*  Use string-building techniques to build names of builtins  
*  Use long, random strings for variable names or very similar names for multiple 
variables  
*  Using builtin compile and exec functions to execute strings  
*  Base64 encoding of code  
*  Hex encoding of code  
*  Anti-tampering technique that stops user from running altered login code  
   *  Program writes the hash of login code to a file in the user's temp folder, then
   validates the code against the hash written on the first run. If it doesn't match, 
   the program will exit. This can be mitigated by deleting the hash file before each
   run.  
    
survival_decoded.py is Survival game with login function deobfuscated to show exactly 
what the login function does and how it works.
