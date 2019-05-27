########################################################################################################################
"""
Partial game code from http://usingpython.com/programs/ 'Crafting Challenge' Game
Extended by SimplyNate

Copyright SimplyNate
Licensed under Creative Commons 4.0
https://creativecommons.org/licenses/by-sa/4.0/

Coding Module - Python Lab
Craft the items indicated in the Quests panel to win the game.
Hunger ticks down after each input by the amount indicated below.
When hunger reaches 0, Health will begin ticking down instead after each input.
When health reaches 0, the game ends.

GenCyber Hawaii SecurityX Camp 2018
"""
########################################################################################################################


# Imports dependencies required for drawing the GUI and other functions
import tkinter
from tkinter import *
from tkinter import ttk


# Class that initiates data for use in the GUI class
class Game:

    # Function that initializes variables with data
    def __init__(self):

        # EDIT VARIABLES BELOW #########################################################################################

        # List of commands - Gets displayed in the "Help" menu
        self.commands = {
            "i": "see inventory",
            "c": "see crafting options",
            "h": "see help",
            "q": "see quests",
            "craft [item] [amount]": "craft something from inventory items",
            "eat [item]": "Eat something from inventory to restore hunger",
            "gather [item]": "Increase resources in your inventory"
        }

        # an inventory of items - Gets listed in the "Inventory" menu
        # Edit the number values to change your starting amount
        self.items = {
            "flint": 50,

            "grass": 100,
            "hay": 0,

            "tree": 100,
            "log": 0,

            "sapling": 100,
            "twig": 0,

            "boulder": 30,
            "rock": 0,

            "pickaxe": 0,
            "axe": 0,

            "firepit": 0,
            "tent": 0,

            "torch": 0,
        }

        # List of Gatherable items
        # Add items from the items list below to be able to gather different items
        self.gatherable = [
            "flint",
            "grass",
            "tree",
            "sapling",
            "boulder",
        ]

        # Inventory of Food items
        # Edit the "amount" numbers to change how much you start with.
        # Edit the "restores" number to change how much each food restores hunger by.
        self.foods = {
            "potato": {
                "amount": 10,
                "restores": 5
            },
            "bread": {
                "amount": 5,
                "restores": 10
            },
            "apple": {
                "amount": 20,
                "restores": 2
            },
            "porkchop": {
                "amount": 5,
                "restores": 20
            }
        }

        # rules to make new objects
        # Change the number values to change how much resources required to craft the item
        self.craft = {
            "hay": {"grass": 1},
            "twig": {"sapling": 1},
            "log": {"axe": 1, "tree": 1},
            "axe": {"twig": 3, "flint": 1},
            "tent": {"twig": 10, "hay": 15},
            "firepit": {"boulder": 5, "log": 3, "twig": 1, "torch": 1},
            "torch": {"flint": 1, "grass": 1, "twig": 1},
            "pickaxe": {"flint": 2, "twig": 1}
        }

        # List of Quests
        # Add more quests by adding a new entry under here
        self.quests = [
            "Craft a Hay",
            "Craft a Tent",
            "Craft a Firepit",
        ]

        # Hero Statistics
        # Change the hunger value to change how much hunger you start with
        # Change the hungerDecay value to change how quickly or slowly the hunger goes down by
        # Change the health value to change how much health you start with
        # Change the healthDecay value to change how quickly or slowly your health goes down by or regenerates by
        # Change the gatherRate value to change how much resources you get when using the gather command
        self.hero = {
            "hunger": 100,
            "hungerDecay": 5,
            "health": 20,
            "healthDecay": 2,
            "gatherRate": 2,
        }

########################################################################################################################
# End Recommended Editable Area                                                                                        #
########################################################################################################################


# Class that draws the GUI and runs the game logic and functions
class Gui:
    argument = ""
    history = []
    index = -1
    qtimes = 0
    itimes = 0
    ctimes = 0
    htimes = 0

    game = Game()
    g = Game()  # Reference variable

    def __init__(self, master):

        # Window itself
        self.master = master
        master.title("Python Game")
        master.geometry("960x480")
        master.resizable(False, False)
        master.configure(background='black')

        # Health and Hunger bar themes
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
        self.s.configure("green.Horizontal.TProgressbar", foreground="green", background="green")
        self.s.configure("yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        self.s.configure("brown.Horizontal.TProgressbar", foreground="brown", background="brown")

        # Title Label
        self.title = Label(master, text="Generic Survival Game", bg="black", fg="white", font=("Impact", 48))
        self.title.place(x=180, y=13)

        # Subtitle Label
        self.subtitle = Label(master, text="Written entirely in Python", bg="black", fg="white", font=("Georgia", 16))
        self.subtitle.place(x=350, y=90)

        # Another Label below the Subtitle
        self.instruction = Label(master, text="Survive the Night!", bg="black", fg="white", font=("Georgia", 24))
        self.instruction.place(x=340, y=200)

        # Button that starts or restarts the game
        self.start = Button(master, text="Start", command=self.startgame, font=("Impact", 28))
        self.start.place(x=230, y=350, width=200, height=100)

        # Button that quits the game
        self.quit = Button(master, text="Quit", command=quit, font=("Impact", 28))
        self.quit.place(x=530, y=350, width=200, height=100)

        # Label telling where to put command
        self.command = Label(master, text="Enter Your Command:", bg="black", fg='white')
        self.command.configure(highlightbackground='white')

        # Top divider between user entry and rest of game
        self.div = Label(master, text="", bg="white")

        # Divider between Label and User entry box
        self.div2 = Label(master, text="", bg="white")

        # Where the user types their arguments
        self.userCommand = Entry(master, bg="black", fg="white", font=("Georgia", 14), borderwidth=0)

        # Output box that gives user more info
        self.outbox = Text(master, wrap="word", state="disabled", font=("Georgia", 12))

        # Quests "button"
        self.quests = Label(master, text="[Q]uests", bg="black", fg="white", borderwidth=2, relief="groove")

        # Inventory "button"
        self.inventory = Label(master, text="[I]nventory", bg="black", fg="white", borderwidth=2, relief="groove")

        # Crafting "button"
        self.crafting = Label(master, text="[C]rafting", bg="black", fg="white", borderwidth=2, relief="groove")

        # Help "Button"
        self.help = Label(master, text="[H]elp", bg="black", fg="white", borderwidth=2, relief="groove")

        # Boxes
        self.questbox = Text(master, wrap="word", state="disabled", font=("Georgia", 12))
        self.inventorybox = Text(master, wrap="word", state="disabled", font=("Georgia", 12))
        self.craftbox = Text(master, wrap="word", state="disabled", font=("Georgia", 12))
        self.helpbox = Text(master, wrap="word", state="disabled", font=("Georgia", 12))

        # Health display
        self.health = Label(master, text=("Health: " + str(Gui.game.hero["health"])), bg="black", fg="white",
                            font=("Georgia", 16))

        # Hunger display
        self.hunger = Label(master, text="Hunger: " + str(Gui.game.hero["hunger"]), bg="black", fg="white",
                            font=("Georgia", 16))

        # Popup notificatin
        self.popup = Label(master, text="You survived!", bg="black", fg="white", borderwidth=2, relief="groove")

        # Health Bar
        self.hbar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")

        # Hunger Bar
        self.hungerbar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")

    def startgame(self):

        # Get new instance of Game
        Gui.game = Game()

        # Place UI Elements
        self.command.place(x=10, y=448, height=32)
        self.div.place(y=447, height=1, width=960)
        self.div2.place(y=448, x=140, height=32)
        self.userCommand.place(x=150, y=448, height=32, width=820)
        self.userCommand.focus()

        # Binds key to perform a specific function
        self.master.bind('<Return>', self.parse)  # Sends data
        self.master.bind('<Up>', self.gethistoryup)  # Gets previous args
        self.master.bind('<Down>', self.gethistorydown)  # Gets previous args

        # Places rest of UI
        self.outbox.place(y=340, width=960, height=106)
        self.quests.place(x=0, y=300, width=240, height=40)
        self.inventory.place(x=240, y=300, width=240, height=40)
        self.crafting.place(x=480, y=300, width=240, height=40)
        self.help.place(x=720, y=300, width=240, height=40)
        self.health.place(x=200, y=130)
        self.hunger.place(x=200, y=160)
        self.hunger.config(text="Hunger: " + str(Gui.game.hero["hunger"]))
        self.health.config(text="Health: " + str(Gui.game.hero["health"]))

        # Forget buttons and instruction
        self.start.place_forget()
        self.quit.place_forget()
        self.instruction.place_forget()

        self.hbar.place(x=340, y=137)
        self.hbar.config(style="green.Horizontal.TProgressbar")
        self.hbar["value"] = Gui.game.hero["health"]
        self.hbar["maximum"] = Gui.game.hero["health"]

        self.hungerbar.place(x=340, y=167)
        self.hungerbar.config(style="brown.Horizontal.TProgressbar")
        self.hungerbar["value"] = Gui.game.hero["hunger"]
        self.hungerbar["maximum"] = Gui.game.hero["hunger"]

    def endgame(self, endtext):
        Gui.argument = ""
        Gui.history = []
        Gui.index = -1
        Gui.qtimes = 0
        Gui.itimes = 0
        Gui.ctimes = 0
        Gui.htimes = 0
        Gui.game = Game()  # Needed
        self.start.config(text="Restart")
        self.start.place(x=230, y=350, width=200, height=100)
        self.quit.place(x=530, y=350, width=200, height=100)
        if endtext == "lose":
            self.instruction.config(text="You have Died!")
            self.instruction.place(x=370, y=200)
        elif endtext == "win":
            self.instruction.config(text="You have Survived!")
            self.instruction.place(x=330, y=200)

        self.command.place_forget()
        self.div.place_forget()
        self.div2.place_forget()
        self.userCommand.place_forget()
        self.outbox.config(state="normal")
        self.outbox.delete("1.0", END)
        self.outbox.config(state="disabled")
        self.outbox.place_forget()
        self.quests.config(relief="groove", bg="black", fg="white")
        self.quests.place_forget()
        self.inventory.config(relief="groove", bg="black", fg="white")
        self.inventory.place_forget()
        self.crafting.config(relief="groove", bg="black", fg="white")
        self.crafting.place_forget()
        self.help.config(relief="groove", bg="black", fg="white")
        self.help.place_forget()
        self.health.place_forget()
        self.hunger.place_forget()
        self.inventorybox.place_forget()
        self.questbox.place_forget()
        self.helpbox.place_forget()
        self.craftbox.place_forget()
        self.hungerbar.place_forget()
        self.hbar.place_forget()

    # Gets the text inputted by the user and parses accordingly
    def parse(self, event):
        keypress = event  # Stores data about keypress, not necessary
        Gui.index = -1
        Gui.argument = self.userCommand.get()
        self.userCommand.delete(0, 'end')
        if Gui.argument is not "" and Gui.argument is not " ":
            Gui.history.insert(0, Gui.argument)
            if len(Gui.history) > 100:
                try:
                    Gui.history.remove(-1)
                except ValueError:
                    pass

        Gui.argument = Gui.argument.strip().lower()  # Normalizes input

        if "craft" in Gui.argument and len(Gui.argument.split(" ")) > 1:
            Gui.play(self, Gui.argument)  # Runs rest of game logic

        elif "eat " in Gui.argument:
            tokens = Gui.argument.split(" ")
            self.writeToOutbox("Eating " + tokens[1])
            Gui.eat(self, tokens[1])

        elif "gather " in Gui.argument:
            tokens = Gui.argument.split(" ")
            self.writeToOutbox("Gathering " + tokens[1])
            Gui.gather(self, tokens[1])

        elif "quests" in Gui.argument or "q" in Gui.argument and len(Gui.argument) == 1:
            Gui.qtimes += 1
            if Gui.qtimes is 1:
                self.quests.config(relief="sunken", bg="white", fg="black")
                self.questbox.config(state="normal")
                self.questbox.delete("1.0", END)
                a = geteverything(Gui.game.quests)  # Different way to do it
                self.questbox.insert(INSERT, a)
                self.questbox.place(x=0, y=210, height=100, width=240)
                self.questbox.config(state="disabled")

                # Output Box
                self.writeToOutbox("Opened Quests menu")
            else:
                Gui.qtimes = 0
                self.quests.config(relief="groove", bg="black", fg="white")
                self.questbox.place_forget()

                # Output Box
                self.writeToOutbox("Closed Quests menu")

        elif "inventory" in Gui.argument or "i" in Gui.argument and len(Gui.argument) == 1:
            Gui.itimes += 1
            if Gui.itimes is 1:
                self.inventory.config(relief="sunken", bg="white", fg="black")
                self.inventorybox.config(state="normal")
                self.inventorybox.delete("1.0", END)
                self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
                self.inventorybox.place(x=240, y=210, height=100, width=240)
                self.inventorybox.config(state="disabled")

                self.writeToOutbox("Opened Inventory menu")
            else:
                Gui.itimes = 0
                self.inventory.config(relief="groove", bg="black", fg="white")
                self.inventorybox.place_forget()

                self.writeToOutbox("Closed Inventory menu")

        elif "crafting" == Gui.argument or "c" in Gui.argument and len(Gui.argument) == 1:
            Gui.ctimes += 1
            if Gui.ctimes is 1:
                self.crafting.config(relief="sunken", bg="white", fg="black")
                self.craftbox.config(state="normal")
                self.craftbox.delete("1.0", END)
                self.craftbox.insert(INSERT, geteverything(Gui.game.craft))
                self.craftbox.place(x=480, y=210, height=100, width=240)
                self.craftbox.config(state="disabled")

                self.writeToOutbox("Opened Crafting menu")
            else:
                Gui.ctimes = 0
                self.crafting.config(relief="groove", bg="black", fg="white")
                self.craftbox.place_forget()

                self.writeToOutbox("Closed Crafting menu")

        elif "help" in Gui.argument or "h" in Gui.argument and len(Gui.argument) == 1:
            Gui.htimes += 1
            if Gui.htimes is 1:
                self.help.config(relief="sunken", bg="white", fg="black")
                self.helpbox.config(state="normal")
                self.helpbox.delete("1.0", END)
                self.helpbox.insert(INSERT, geteverything(Gui.game.commands))
                self.helpbox.place(x=720, y=210, height=100, width=240)
                self.helpbox.config(state="disabled")

                self.writeToOutbox("Opened Help menu")
            else:
                Gui.htimes = 0
                self.help.config(relief="groove", bg="black", fg="white")
                self.helpbox.place_forget()

                self.writeToOutbox("Closed Help menu")

        else:
            self.writeToOutbox(Gui.argument + " is not a valid argument")

        # if the command is not blank
        if Gui.argument is not "" and Gui.argument is not " ":
            # Hunger and Health
            # If hunger is greather than 70% of max
            if Gui.game.hero["hunger"] >= int(Gui.g.hero["hunger"] * 0.7):
                # If health is lower than maximum
                if Gui.game.hero["health"] < Gui.g.hero["health"]:
                    # Regeneration of health
                    Gui.game.hero["health"] += Gui.game.hero["healthDecay"]
                    # If health is greater than maximum
                    if Gui.game.hero["health"] > Gui.g.hero["health"]:
                        # Set health to maximum
                        Gui.game.hero["health"] = Gui.g.hero["health"]
            if Gui.game.hero["hunger"] > 0 and "eat" not in Gui.argument.lower():
                Gui.game.hero["hunger"] -= Gui.game.hero["hungerDecay"]
                if Gui.game.hero["hunger"] < 0:
                    Gui.game.hero["hunger"] = 0
            if Gui.game.hero["hunger"] == 0 and "eat" not in Gui.argument.lower():
                if Gui.game.hero["health"] != 0:
                    Gui.game.hero["health"] -= Gui.game.hero["healthDecay"]
                    if Gui.game.hero["health"] < 0:
                        Gui.game.hero["health"] = 0
                    if Gui.game.hero["health"] == 0:
                        self.endgame("lose")
            self.hbar["value"] = Gui.game.hero["health"]
            self.hungerbar["value"] = Gui.game.hero["hunger"]
            self.hunger.config(text="Hunger: " + str(Gui.game.hero["hunger"]))
            self.health.config(text="Health: " + str(Gui.game.hero["health"]))
            if Gui.game.hero["health"] > int(Gui.g.hero["health"] * 0.5):
                self.hbar.configure(style="green.Horizontal.TProgressbar")
            elif Gui.game.hero["health"] > int(Gui.g.hero["health"] * 0.25):
                self.hbar.configure(style="yellow.Horizontal.TProgressbar")
            else:
                self.hbar.configure(style="red.Horizontal.TProgressbar")

    # Function that "returns" previous commands
    def gethistoryup(self, event):
        keypress = event
        amt = len(Gui.history)
        if amt > 0:
            Gui.index += 1
            if Gui.index < amt:
                self.userCommand.delete(0, 'end')
                self.userCommand.insert(0, Gui.history[Gui.index])
            else:
                Gui.index = amt-1
                self.userCommand.delete(0, 'end')
                self.userCommand.insert(0, Gui.history[Gui.index])

    # Function that "returns" previous commands (backwards)
    def gethistorydown(self, event):
        keypress = event
        if len(Gui.history) > 0:
            Gui.index -= 1
            if Gui.index >= 0:
                self.userCommand.delete(0, 'end')
                self.userCommand.insert(0, Gui.history[Gui.index])
            if Gui.index <= -1:
                Gui.index = -1
                self.userCommand.delete(0, 'end')

    def writeToOutbox(self, text):
        text = text + "\n"
        self.outbox.config(state="normal")
        self.outbox.insert(END, text)
        self.outbox.config(state="disabled")
        self.outbox.see(tkinter.END)

    def eat(self, item):
        if item in Gui.game.foods.keys() and Gui.game.foods[item]["amount"] > 0:
            self.writeToOutbox("Restored " + str(Gui.game.foods[item]["restores"]) + " hunger")
            if Gui.game.hero["hunger"] != 100:
                Gui.game.hero["hunger"] += Gui.game.foods[item]["restores"]
                if Gui.game.hero["hunger"] > 100:
                    Gui.game.hero["hunger"] = 100
            self.hunger.config(text="Hunger: " + str(Gui.game.hero["hunger"]))
            Gui.game.foods[item]["amount"] -= 1
            self.inventorybox.config(state="normal")
            self.inventorybox.delete("1.0", END)
            self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
            self.inventorybox.config(state="disabled")
        else:
            self.writeToOutbox(item + " is not an edible item")
            if Gui.game.hero["hunger"] > 0:
                Gui.game.hero["hunger"] -= Gui.game.hero["hungerDecay"]
                if Gui.game.hero["hunger"] < 0:
                    Gui.game.hero["hunger"] = 0
            self.hunger.config(text="Hunger: " + str(Gui.game.hero["hunger"]))
            if Gui.game.hero["hunger"] == 0:
                if Gui.game.hero["health"] != 0:
                    Gui.game.hero["health"] -= Gui.game.hero["healthDecay"]
                    if Gui.game.hero["health"] <= 0:
                        self.endgame("lose")
                else:
                    self.endgame("lose")
        self.hungerbar["value"] = Gui.game.hero["hunger"]

    def gather(self, item):
        if item in Gui.game.gatherable:
            self.writeToOutbox("Gathered " + str(Gui.game.hero["gatherRate"]) + " " + item)
            Gui.game.items[item] += Gui.game.hero["gatherRate"]
            self.inventorybox.config(state="normal")
            self.inventorybox.delete("1.0", END)
            self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
            self.inventorybox.config(state="disabled")
        elif item in Gui.game.foods:
            self.writeToOutbox("Gathered " + item)
            Gui.game.foods[item]["amount"] += Gui.game.hero["gatherRate"]
            self.inventorybox.config(state="normal")
            self.inventorybox.delete("1.0", END)
            self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
            self.inventorybox.config(state="disabled")
        else:
            self.writeToOutbox(item + " is not gatherable")

    # Method for Crafting items
    def play(self, arg):

        command = arg.split()

        if len(command) > 0:
            verb = command[0].lower()
        else:
            verb = None
        if len(command) > 1:
            item = command[1].lower()
        else:
            item = None
        if len(command) > 2:
            try:
                quantity = int(command[2].lower())
            except ValueError:
                Gui.writeToOutbox(self, "Error: Please switch position of item and quantity")
                quantity = None
        else:
            quantity = 1

        if verb == "craft":

            Gui.writeToOutbox(self, "making " + item + ":")
            if item in Gui.game.craft:

                for i in Gui.game.craft[item]:
                    Gui.writeToOutbox(self, "  you need : " + str(Gui.game.craft[item][i] * quantity) + " " + i +
                                      " and you have " + str(Gui.game.items[i]))

                canBeMade = True

                for i in Gui.game.craft[item]:
                    if (Gui.game.craft[item][i] * quantity) > Gui.game.items[i]:
                        Gui.writeToOutbox(self, "item cannot be crafted\n")
                        canBeMade = False
                        break

                if canBeMade is True:
                    for i in Gui.game.craft[item]:
                        Gui.game.items[i] -= Gui.game.craft[item][i] * quantity

                    Gui.game.items[item] += 1 * quantity

                    if quantity > 1:
                        Gui.removeQuest(self, item)
                        Gui.writeToOutbox(self, "items crafted\n")
                        self.inventorybox.config(state="normal")
                        self.inventorybox.delete("1.0", END)
                        self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
                        self.inventorybox.config(state="disabled")

                    else:
                        Gui.removeQuest(self, item)
                        Gui.writeToOutbox(self, "item crafted\n")
                        self.inventorybox.config(state="normal")
                        self.inventorybox.delete("1.0", END)
                        self.inventorybox.insert(INSERT, geteverything(Gui.game.items))
                        self.inventorybox.config(state="disabled")

                if len(Gui.game.quests) == 0:
                    Gui.writeToOutbox(self, "\n**YOU HAVE MANAGED TO SURVIVE!\nWELL DONE!")
                    self.endgame("win")

            else:
                Gui.writeToOutbox(self, "you can't")

        else:
            Gui.writeToOutbox(self, "you can't")

    def popup(self, text):
        pass

    def removeQuest(self, arg):
        arg = arg.capitalize()
        # for i in range(len(Gui.game.quests)):
        for item in Gui.game.quests[:]:
            if arg in item:
                try:
                    Gui.game.quests.remove(item)
                except ValueError:
                    pass
        self.questbox.config(state="normal")
        self.questbox.delete("1.0", END)
        a = geteverything(Gui.game.quests)  # Different way to do it
        self.questbox.insert(INSERT, a)
        self.questbox.config(state="disabled")


def geteverything(mlist):
    if mlist is Gui.game.quests:
        l = ""
        for i in range(len(mlist)):
            l += mlist[i] + "\n"
        return l
    elif mlist is Gui.game.craft:
        l = ""
        for key in mlist:
            l += key + " can be made with:\n"
            for i in Gui.game.craft[key]:
                l += str(Gui.game.craft[key][i]) + " " + i + "\n"
            l += "\n"
        return l
    elif mlist is Gui.game.items:
        l = ""
        for key in mlist:
            l += key + "\t:  " + str(mlist[key]) + "\n"
        for key in Gui.game.foods:
            l += key + "\t:  " + str(Gui.game.foods[key]["amount"]) + "\n"
        return l
    else:
        l = ""
        for key in mlist:
            l += key + " : " + str(mlist[key]) + "\n"
        return l


########################################################################################################################
# END LAB 2 ############################################################################################################
########################################################################################################################

########################################################################################################################
# START LAB 3 ##########################################################################################################
########################################################################################################################
"""
Warning: Do not alter anything below until instructed to do so.

Instructions: Attempt to bypass or disable the login box
Remember: Undo [CTRL]+[Z] is your friend
"""


def combine(a, b, c):
    return a + b + c


# This part just obfuscates built-in functions
main = combine('_', '_', 'm') + "ai" + combine('n', '_', "_")  # __main__
string = combine('<', 's', 't') + combine('r' + "i", 'n', 'g' + ">")  # <string>
ev = combine('e', "", 'v')  # ev
al = combine("", 'a', 'l')  # al
evals = combine(ev, "", al)  # eval
compiles = eval(compile(combine("c", 'o' + "m", 'p' + "i") + combine('l', 'e', ""), string, evals))  # compile
evaluate = eval(compile(evals, string, evals))  # eval
byte = combine('b' + "y", "t", 'e' + 's' + ".")  # bytes.
bytesfromhex = evaluate(compiles(byte + combine('f' + "ro", "m", 'h' + 'e') + 'x', string, evals))  # bytes.fromhex
utf8 = 'u' + 't' + combine('f', '-', '8')  # utf-8
strtype = evaluate(compiles(combine('s', 't', 'r'), string, evals))  # str
execute = combine('e', 'x', 'e') + 'c'  # exec
name = evaluate(compiles('_' + combine("_" + 'n' + 'a', 'm' + 'e', '_' + '_'), string, evals))  # __name__


"""
So you want to know what goes on below?
The first step is to decode the message in tow.

There are many unnecessary marks under the score
But only one aligns different than the rest. 
Once you find the correct mark, 
Move not more than two forward and not more than three backward, 
For these nefarious characters 
Are plotting against you. 

Fuse all the pieces together
And you will find a secret message, 
Cast in base64
A firey tool will help
Lead the way


# Base64 Decoded
Hidden operations be awaiting below:
One that appears like this does
(But a fair warning to you,
Decoding does not like that
In which quotes thee),

And one who's complexity
Is not what it seems.
He who wants to break the code
Uses the 16th base

Clues be hidden invariably in this program,
Above all that is running
To help decode
This Cyrillic mess

Tread carefully though,
A watchful warden awaits
Any trespassers who dare
To discover the secrets below.


"""
if __name__ == '__main__':
    # Additional import statements
    import hashlib
    import os.path

    # Starting point for anti-tampering
    identifier = 'if __na'

    # Open this file and read the lines
    infile = open("survival.py").readlines()
    # Variable to store the lines of the file
    wc = ""
    # Counter variable
    c = 0
    # For each line in this file
    for line in infile:
        # If the identifier is found in the line
        if identifier in line:
            # Add 1 to the counter variable
            c += 1
        # If the counter is greater than 1
        if c > 0:
            # Start appending the lines of this file to the variable
            # We do this so that the game code can be edited but the anti-tampering and login functions cannot be
            wc = wc + line.strip()
    # If the counter variable remains 0 (meaning the string 'if __na' is not found in the file
    if c < 1:
        # Print the exit message
        print('The Warden detected an intruder! Passage has been blocked. Exiting...')
        # Quit the program
        sys.exit(0)
    # Get the current SHA1 hash of the wc variable
    current_hash = hashlib.sha1(wc.encode()).hexdigest()
    # If the file exists
    if os.path.isfile(os.path.expanduser('~/AppData/Local/Temp/pqsddsfr.tmp')):
        # Get the hash from the file
        stored_hash = open(os.path.expanduser('~/AppData/Local/Temp/pqsddsfr.tmp')).read().strip()
        # If the two hashes do not match
        if stored_hash != current_hash:
            # Print the exit message
            print('The Warden detected an intruder! Passage has been blocked. Exiting...')
            # Quit the program
            sys.exit(0)
    # Else, the file does not exist and needs to be created
    else:
        # Open the file in write mode
        hash_file = open('~/AppData/Local/Temp/pqsddsfr.tmp', "w")
        # Write the hash to the file
        hash_file.write(current_hash)
        # Close the file
        hash_file.close()
        # This hash will be used in subsequent runs of the program

    # Function to validate the given password
    def validate():
        # Get the password entered by the user
        password = passwordEntry.get()
        # If the password matches
        if password == 'magenta319clouds':
            # Quit and destroy the login window
            loginWindow.quit()
            loginWindow.destroy()
            # Start the game
            game = Tk()
            gui = Gui(game)
            game.mainloop()

    # Create the login window
    loginWindow = Tk()
    # Disable resizing of the window
    loginWindow.resizable(False, False)
    # Give the window a title 'login'
    loginWindow.title("Login")
    # Configure the background white
    loginWindow.configure(background='white')
    # Create the Username text
    usernameLabel = Label(loginWindow, text='Username:', background='white')
    # Create the Password text
    passwordLabel = Label(loginWindow, text='Password:', background='white')
    # Create the username entry space
    usernameEntry = Entry(loginWindow)
    # Create the password entry space
    passwordEntry = Entry(loginWindow)
    # Create the login button
    loginButton = Button(loginWindow, text='Login', command=validate, background='white')
    # Create the exit button
    exitButton = Button(loginWindow, text='Exit', command=quit, background='white')
    # Place all the elements in the window
    usernameLabel.grid(row=0, column=0)
    usernameEntry.grid(row=0, column=1, columnspan=3)
    passwordLabel.grid(row=1, column=0)
    passwordEntry.grid(row=1, column=1, columnspan=3)
    loginButton.grid(row=2, column=0, columnspan=2, sticky=W + E)
    exitButton.grid(row=2, column=2, columnspan=2, sticky=W + E)
    # Run the window
    loginWindow.mainloop()
