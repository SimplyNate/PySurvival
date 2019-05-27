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


def qeydfsfgdstreygfd(hytedy, ghytjh, fewqe):
    return hytedy + ghytjh + fewqe


from base64 import b64decode as безопасность
pdftagrthrsae = "ianm_girstn<8ab6>_u-ecxmeaoplvfybh."
лояльность = qeydfsfgdstreygfd(pdftagrthrsae[4],pdftagrthrsae[17],pdftagrthrsae[3])+"ai"+qeydfsfgdstreygfd(pdftagrthrsae[2],pdftagrthrsae[17],"_")
Кремль = qeydfsfgdstreygfd(pdftagrthrsae[11],pdftagrthrsae[8],pdftagrthrsae[9])+qeydfsfgdstreygfd(pdftagrthrsae[7]+"i",pdftagrthrsae[10],pdftagrthrsae[5]+">")
технологии = qeydfsfgdstreygfd(pdftagrthrsae[20],"",pdftagrthrsae[29])
компьютер = qeydfsfgdstreygfd("",pdftagrthrsae[1],pdftagrthrsae[28])
кодирование = qeydfsfgdstreygfd(технологии,"",компьютер)
нарушения = eval(compile(qeydfsfgdstreygfd("c",pdftagrthrsae[26]+"m",pdftagrthrsae[27]+"i")+qeydfsfgdstreygfd(pdftagrthrsae[28],pdftagrthrsae[20],""), Кремль, кодирование))
оценивать = eval(compile(кодирование, Кремль, кодирование))
сила = qeydfsfgdstreygfd(pdftagrthrsae[32]+"y","t",pdftagrthrsae[20]+pdftagrthrsae[8]+".")
информационная = оценивать(нарушения(сила+qeydfsfgdstreygfd(pdftagrthrsae[-5]+"ro","m",pdftagrthrsae[-2]+pdftagrthrsae[20])+pdftagrthrsae[22], Кремль, кодирование))
большевик = pdftagrthrsae[18]+pdftagrthrsae[9]+qeydfsfgdstreygfd(pdftagrthrsae[30],pdftagrthrsae[19],pdftagrthrsae[12])
взлом = оценивать(нарушения(qeydfsfgdstreygfd(pdftagrthrsae[(9-1)],pdftagrthrsae[(27-9*(2-(-2)))*-1],pdftagrthrsae[int((2/(1/4))-1)]), Кремль, кодирование))
советский = qeydfsfgdstreygfd(pdftagrthrsae[20],pdftagrthrsae[22],pdftagrthrsae[(17+3)])+pdftagrthrsae[(7*3)]
выигрыш = оценивать(нарушения(pdftagrthrsae[4]+qeydfsfgdstreygfd("_"+pdftagrthrsae[2]+pdftagrthrsae[1],pdftagrthrsae[3]+pdftagrthrsae[20],pdftagrthrsae[17]+pdftagrthrsae[4]), Кремль, кодирование))


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

SGlkZGVuIG9wZ__ XJhdGlvbnMgYmUgYXdhaXRpbmcgYmVsb3c6DQpPbmUgdGhh__ dCBhcHBlYXJzIGxpa2UgdGhpcyBkb2VzDQooQnV0IGEgZmFpciB3YX
JuaW5nIHRvIHlvdSwNCkRlY29kaW__ 5nIGRvZXMgbm90IGxpa2UgdGhhdA0KSW4gd2hpY2ggcXVvdGVzIHRoZ__ WUpLA0KDQpBbmQgb25lIHdobydzIGNv
bXBsZXhpdHkNCklzIG5vdCB3aGF0IGl0IHNlZW1zLg0KSGUgd2hvIHd__ hbnRzIHRvIGJyZ__ WFrIHRoZSBjb2RlDQpVc2VzIHRoZSAxNnRoIGJhc2UNCg
0K__ Q2x1ZXMgYmUgaGlkZGVuIGludmFyaWFibHkgaW4gdGhpcyBwcm9ncmFtLA0KQWJvdmUgYWxsIif __naHRoYXQgaXMgcnVubmluZw0KVG8gaGVscCBk
ZWNvZGUNClRoaXMgQ3l__ yaWxsaWMgbWVzcw0KDQpUcmVhZCBjYXJlZnVsbHkgdGhvdWdoLA0KQSB3YXRjaGZ1bCB3YXJkZW4gYXdhaXRzDQpBbnkgd__ H
Jlc3Bhc3NlcnMgd2hvIGRhcmUNClRvIGRpc2NvdmVyIHR__ oZSBzZWNyZXRzIGJlbG93Lg==


"""
if выигрыш == лояльность:

    оценивать(нарушения(взлом(безопасность(
        'ZnJvbSB0a2ludGVyIGltcG9ydCBUayBhcyBhc2Y2NWVzZGhpODcNCmZyb20gYmFzZTY0IGltcG9ydCBiNjRkZWNvZGUgYXMgbWxzdzR0ajc2M3'
        'cwOWhncw0KaW1wb3J0IGhhc2hsaWIgYXMgaHl0ZWRzZGdqaGdydGRzDQppbXBvcnQgb3MucGF0aCBhcyB5dXlnZmZzZA0KDQpsMWxsMTFsMSA9'
        'IG9wZW4NCmxsMWwxMWwxID0gY29tcGlsZQ0KbDFsMWxsMWwgPSB5dXlnZmZzZC5leHBhbmR1c2VyDQpsMTFsbDFsMSA9IHN0cg0KbGwxMWwxbG'
        'wgPSB5dXlnZmZzZC5pc2ZpbGUNCmwxMTFsbDFsID0gcHJpbnQNCmwxbDFsMWwxID0gZXZhbA0KbDExbGxsbGwgPSBieXRlcy5mcm9taGV4DQpk'
        'WFJtTFRnID0gJ3V0Zi04Jw0KUEhOMGNtbHVaejQgPSAnPHN0cmluZz4nDQpaWGhsWXcgPSAnZXhlYycNCmFXWWdYMTl1WVEgPSAnaWYgX19uYS'
        'c='),
        большевик),
        Кремль,
        советский)
    )

    оценивать(
        информационная(
            '6C316C316C316C31280D0A096C6C316C31316C31280D0A09096C31316C6C316C31280D0A0909096D6C737734746A37363377303968'
            '6773280D0A0909090927624446734D5777786244456F62444578624778736247776F44516F4A4A7A5A444D7A4532517A4D784E6B4D'
            '7A4D545A444D7A45794F445A444E6B4D7A4D545A444D7A457A4D545A444D7A45794F445A444D7A457A4D545A444E6B4D7A4D545A44'
            '4D7A270D0A090909092745794F445A454E6B4D334D7A63334D7A51334E445A424D7A637A4E6A4D7A4E7A637A4D444D354E6A67324E'
            '7A637A4D6A6777524442424D446B794E7A56424D7A497A4F545A454E6A49304F4452464A77304B43536332516A59794E6B51324F44'
            '6378270D0A09090909274E446B304E444D774E6A63324D6A51304E4459334D7A59794E4451304E5463344E6A49304E4451314E6B59'
            '324D6A55334E7A6733515459304E3045314D6A4D774E6A45325154597A4D7A493052444D7A4E6A4D334E7A52474E5463324F445A46'
            '4E6A270D0A09090909274D334F5459334E6A6B314F5464424E4555314E7A59314E5463314D6A63304E6A49304E43634E43676B6E4E'
            '454531515455324D7A4D324E444D784E546B7A4D4459344E7A49314D44557A4E446B334D4452444E444D304D6A5A444E6A49325244'
            '5246270D0A09090909274E7A5931515451334E6B4D334E5456424E30457A4D545A434E5463304E6A52424E7A51314E4451324E5449'
            '32525452434E544D7A4E5463354E5545314E7A51324E6B49324D6A51334D6A6377524442424D446B794E7A5A444E7A556E44516F4A'
            '4A7A270D0A090909092756424E54673052445A474E4549314D544D774E4549324E444D794E4551324E7A55774E544D304D5459354E'
            '446B324E7A4D774E4549314F5463354E44457A4F5451354E4451304D5452464E444D32524456424E7A59324D7A59354E4449334E7A'
            '597A270D0A09090909274E4467304E6A4D7A4E5545314F4452424E7A41304F5451334E6B4D334E5451354E4463324E4463324E5545'
            '32524463344A77304B43536333515456424E44637A4E545A474E6A453251545A474E4555304D7A59334E6B4D334D4456424E6A6B30'
            '4D6A270D0A090909092759344E54597A4D545A444E6B55314E7A51304E44557A4E5459304E545932517A55794E446B304E7A5A444E'
            '7A55304F5451344E4449334E7A597A4E5467324E445A444E6A4D3252445A434D7A59304E4455784E6B59305154517A4E5463305244'
            '5933270D0A09090909274D6A63775243634E43676B6E4D4545774F5449334E45493351544D774E6A6330524455784D7A4130516A51'
            '7A4E546332517A5A454E446B304E7A52454E6A63314D4459354E4445334E7A52474E6A637A4D4452434E444D314D545A444D7A4D31'
            '4F54270D0A090909092763354E44457A4F5451354E4467324E445A424E446B304D7A637A4E6A63324D7A51344E4449334F4459304D'
            '7A49314E6A63354E6A45314D7A4D314E30456E44516F4A4A7A59304E446730515463774E6A4D304D7A59334E7A41304E4455784E7A'
            '4133270D0A09090909274D4456424E6A6B304D6A5A424E446B304E4463334E6A6330524455304E6B59305254517A4E6A6332516A52'
            '424E6A49304E4451314E7A6730524455334E7A67334D7A52454E5463334E7A5A474E6A49304E4451314E7A67324D6A51334E7A6333'
            '4F44270D0A090909092759794E4451304E545A474E6A49314E7A63344A77304B43536333515459304E3045794E7A42454D4545774F'
            '5449334E54497A4D4459784E6B45324D7A4D794E45517A4D7A597A4E7A6330526A55334E6A67325254597A4E7A6B324E7A5A464E54'
            '5932270D0A0909090927516A59304E6B59324D6A51314E6B4D304E7A56424E4463324F445A424E6A49314E6A52424E7A4D314F545A'
            '454E6B4D304D7A59784D7A45334D4455354E545532524463344E5545305243634E43676B6E4D7A45305154637A4E546332516A5246'
            '4E44270D0A09090909274D324D5451334E4545334D4455784E6B55304D6A59354E6A4932517A52424D7A5531515451324E6A51314D'
            '7A59794E446330525463774E5449314E7A59304E5459314D6A4D774E55457A4E6A55354E304530515451334E6A4932517A63774E54'
            '5131270D0A09090909274D545A454D7A6B31515455334E44557A4D545A464E5463314E7A4D784E54636E44516F4A4A7A59794E4463'
            '30515463774E54453252445A444E6A6B794E7A42454D4545774F5449334E54493351545A444E7A45314F5455304E4545314E7A5978'
            '4D7A270D0A090909092741334F4463774E5445314E544D314E445131515464424E444930517A55314E6B4D324F445A474E6A4D304E'
            '7A55794E4467324D6A51344E5459324D5459314E5451314D6A4D784E5451304E7A597A4E7A63314D7A63354A77304B435363324D7A'
            '6377270D0A09090909274E454D304D7A51794E6B49314E7A51324E4545334E4455304E4459314D6A5A464E4549314D7A5A434E4555'
            '304D7A59334E6B4930515459794E4451304E6A637A4E4551314E7A63334E7A67324D6A51304E445532526A59794E4463334E7A6334'
            '4E6A270D0A090909092749304E4451314E7A67324D6A51304E445532526A59794E4451304E5463344E6A49304E7A63334E7A67324D'
            '69634E43676B6E4E4451304E545A474E6A49314E7A63344E3045324E4464424E54497A4D4459784E6B45794E7A42454D4545774F54'
            '4933270D0A09090909274E6A4D7A4D6A52454D7A4D324D7A63334E4559314E7A59344E6B55324D7A63354E6A6332525455354E3045'
            '305254637A4E6A5532516A63344E7A51314E6A5A424E5449324F4455334E4459304E6A63324E5451314E5452464E7A49314D44557A'
            '4E6A270D0A09090909274D6E44516F4A4A7A63774E454D304D7A51794E6B49314E7A51324E4545334E4455304E4459314D6A5A464E'
            '4549314D7A63334E6A63314E5451314E6A6730526A52454E446330525463304E6A49304F4455324E6A45324E545A424E5445334D7A'
            '5135270D0A09090909274E4459334D4455354E6A45304E7A63344E5545324E4463354E6B49334D4451304E5445334D445A424E6A45'
            '304D7A51784D7A6B304F5451334A77304B435363334E7A63344E6A49304E4451324E7A4D30524455334E7A63334F4452434E446333'
            '4E7A270D0A090909092763344E4551314E7A63344E7A4D794E7A42454D4545774F5449334E4551314E7A63334E7A6730516A51334D'
            '7A45334D7A597A4D7A4D324D7A4D774E6A51304E7A5A474D7A4D3052545A424E45557A4D7A52454E445132517A5A474E55457A4D7A'
            '5245270D0A09090909274E6B593051544D794E4459304F53634E43676B6E4E6A49304E4451794E6A45314E6A4D784E45457A4E6A55'
            '334E6B49324E445A434E6A4D314E7A51324E446731515451344E6B4D32516A55794D7A453051544D324E5451304E7A4D314E455932'
            '4D6A270D0A09090909274D784E6B4D314E5455794E54637A4F545A434E455132516A4D784D7A45314E7A5A444E6A4D7A4D5459784E'
            '6B51304F5463354E545532524463344E454D314D544D794E7A516E44516F4A4A7A63334E5451304E7A4D784E6B59324D6A51334E54'
            '5930270D0A09090909274F4455314E6B55304D6A59784E455132517A56424D7A5931515451314E4555325254597A4E444D794E7A42'
            '454D4545774F5449334E6A4D334D4452444E444D304D6A5A434E5463304E6A52424E7A51314E4451324E544932525452434E544D32'
            '516A270D0A090909092752464E444D3252445A444E6B51304F5451334E7A67334D7A52454A77304B435363314E4451324E7A4D3052'
            '4455334E7A67334D7A52434E4463334E7A63344E6A49304E4451324E7A4D324D6A51304E4459334D7A52434E44637A4D54637A4E6A'
            '4D7A270D0A09090909274D7A597A4D7A41324E4451334E6B597A4D7A52464E6B453052544D7A4E4551304E445A444E6B593151544D'
            '7A4E455132526A52424D7A4931515463774E4559314E5452424E6B45314D7A51314E4545304E69634E43676B6E4E5463314E6A5934'
            '4E54270D0A09090909274D324D5451314E7A63334E7A59314E446731515456424E455132516A56424E3045314E4451304E4459314D'
            '7A59794E446330515455354E5445314F4456424E6B45794E7A42454D4545774F5449334E544D304E5456424D7A59314E7A5A434E6A'
            '5131270D0A09090909274D7A59314E6B4D334D4463314E544D314F4455324E6B49314D6A64424E44597A4D7A52424E7A6B6E44516F'
            '4A4A7A5A434E7A4130516A55304E6B59305254517A4E6A6332517A63334E6A497A4D6A55794D7A45324E4451344E45453252445135'
            '4E44270D0A0909090927517A4D4459334E6A49304E4451324E7A4D324D6A51304E4455334F4459794E4451304E545A474E6A49304E'
            '4451324E7A4D30524455334E7A67334D7A52454E5463334E7A5A474E6A49314E7A63344E3045324E4464424E54497A4D4459784A77'
            '304B270D0A0909090927435363325154597A4D7A493052444D7A4E6A4D334E7A52474E5463324F445A464E6A4D334F5459334E6B55'
            '3151545A454E6B497A4E5455784E6B5130525451354E544532516A55324E5545314E7A51324E454532526A55304E4451794E7A4245'
            '4D45270D0A090909092745774F5449334E44497A4E4459304E6B4D32516A63354E544932525452464E455130524455324E4545334D'
            '7A55354E6B4D324F43634E43676B6E4E4449324E445A454E4555304F5455794E6B55334D4459784E54497A4D5452424D7A59314E7A'
            '5A45270D0A09090909274D7A5530515459304E5463314D6A51344E4551314F44597A4E6B5530516A557A4E6B49334D4452444E6B55'
            '3051545A444E546B314E7A55784E6B5930516A557A4D7A5533515459304E446730515463774E6A4D304D7A59334E7A41304E445578'
            '4E6B270D0A09090909275930515459784E54636E44516F4A4A7A55354E6A63324D7A51334D7A6B32516A59304E5467314D6A63354E'
            '5545324F5451784E6A67314D44557A4E444932515459784E445132526A52464E444D324E7A5A434E4545324D6A51304E4455334F44'
            '5245270D0A09090909274E5463334F44637A4E4551314E7A63334E6B59794E7A42454D4545774F5449334E6A49304E4451314E7A67'
            '324D6A51334E7A63334F4459794E4451304E545A474A77304B435363324D6A55334E7A6733515459304E3045314D6A4D774E6A4532'
            '5154270D0A0909090927597A4D7A493052444D7A4E6A4D334E7A52474E5463324F445A464E6A4D334F5459334E6B55314E6A5A434E'
            '6A5132526A59794E445532517A51334E5545304E7A59344E6B45324D6A55324E4545334D7A55354E6B5132517A517A4E6A457A4D54'
            '6377270D0A09090909274E546B314E545A454E7A6731515452454D7A45305153634E43676B6E4E7A4D314E7A5A434E4555304D7A59'
            '784E446330515463774E544532525451794E6A6B324D6A5A444E45457A4E5456424E4459324E44557A4E6A49304E7A52464E7A4131'
            '4D6A270D0A090909092755334E6A51314E6A55794D7A413151544D324E546B33515452424E4463324D6A5A444E7A41314E4455784E'
            '6B51794E7A42454D4545774F5449334D7A6B31515455334E44557A4D545A464E54636E44516F4A4A7A55334D7A45314E7A59794E44'
            '6330270D0A0909090927515463774E54453252445A444E6A6B314D6A64424E6B4D334D5455354E545130515455334E6A457A4D4463'
            '344E7A41314D5455314D7A55304E4456424E3045304D6A52444E545532517A59344E6B59324D7A51334E5449304F4459794E446731'
            '4E6A270D0A090909092759784E6A55314E4455794D7A45314E4451334E6A4D334E7A557A4E7A6B324D7A63774A77304B4353633051'
            '7A517A4E444932516A55334E445930515463304E5451304E6A55794E6B5530516A557A4E6B49305254517A4E6A6332516A52424E6A'
            '4930270D0A09090909274E4451324E7A4D30524455334E7A63334F4459794E4451304E545A474E6A49304E7A63334E7A67324D6A51'
            '304E4455334F4459794E4451304E545A474E6A49304E4451314E7A67794E7A42454D4545774F5449334E6A49304E79634E43676B6E'
            '4E7A270D0A090909092763334F4459794E4451304E545A474E6A49314E7A63344E3045324E4464424E54497A4D4459784E6B45324D'
            '7A4D794E45517A4D7A597A4E7A6330526A55334E6A67325254597A4E7A6B324E7A5A464E546B33515452464E7A4D324E545A434E7A'
            '6733270D0A09090909274E4455324E6B45314D6A59344E5463304E6A51324E7A59314E4455314E4555334D6A55774E544D324D7A63'
            '774E454D6E44516F4A4A7A517A4E444932516A55334E445930515463304E5451304E6A55794E6B5530516A557A4E7A63324E7A5531'
            '4E44270D0A090909092755324F4452474E4551304E7A52464E7A51324D6A51344E5459324D5459314E6B45314D54637A4E446B304E'
            '6A63774E546B324D5451334E7A6731515459304E7A6B32516A63774E4451314D5463774E6B4D324D6A51344E455532517A52474E6A'
            '6379270D0A09090909274E7A42454A77304B43536377515441354D6A637A4D4452434E444D314E7A63334E7A67324D6A51304E4459'
            '334D7A52454E5463334E7A63344E4549304E7A63344E7A4D30524455334E7A63334F4452454E5463334E7A63344E4549304E7A6333'
            '4E7A270D0A09090909276730524455334E7A67334D7A52454E5463334E7A63344E4549304E7A4D784E7A4D324D7A4D7A4E6A4D7A4D'
            '4459304E446332526A4D7A4E4555325153634E43676B6E4E45557A4D7A52454E445132517A5A474E55457A4D7A52454E6B59305154'
            '4D79270D0A09090909274E4555304F4459314E446730515459344E54593351545A444E7A6731515451324E4555304D6A52474E5455'
            '32517A51344E6A517A4D7A59344E6A6B314D6A4D7A4E6A517A4E4455304E5459324E444D7A4E6A55304E5463304E4467324E444D7A'
            '4E6A270D0A090909092767324F5455794E445531515464424E546B6E44516F4A4A7A5A434E5449304E7A49334D455177515441354D'
            '6A63324D7A4D774E7A51304F4452454E54673052545A424E45517A4D6A52454E7A6331515451314E6A51334E6A52454D7A417A4E54'
            '6378270D0A09090909274E545132515452464E4555314D6A51334E7A67334E6A55334E6B4530525452464E6A497A4D445A474E7A6B'
            '314E7A5A464E4449314D4455324E5455334D4463784E54557A4D4455324A77304B43536330516A55794E6B4D324E4455334E6A4530'
            '4E6A270D0A090909092752464E6A67314D6A55344E6A517A4D7A56424E5455324F4459784E546332516A4D784E7A49314E7A5A464E'
            '7A41314E5455794E445531515455304E546B32516A59304E4549314E7A55324E4459314F5455334E6B51334D4455304E5449314E6A'
            '5A47270D0A09090909274D7A49314E6A4D794E7A5132516A55314D7A49314E6A637A4E6A4D304F43634E43676B6E4E5459314E4455'
            '334E445931515463794E545532525449334D455177515441354D6A63334D4451334E45517A4D4463774D7A55324D544D7A4E444930'
            '5244270D0A090909092755784D7A41304E6A63774E5545304F445A444E4545324D7A51314E5449314D6A597A4E4467324E4459354E'
            '54497A4D7A55794E7A63314F545A424E4545334E7A52454E5455334F4463314E5545304F445A444E6A676E44516F4A4A7A55334E44'
            '5930270D0A09090909275154637A4E544D7A4D4459304E4559324D6A4D774E7A51314D6A52454E4455334E445A424E54497A4D7A59'
            '344E7A6B314F5455324E6A4D7A4E54597A4E5463314D6A55304E4555314E7A63774E6A6B314D6A64424E6B4D7A4E6A55334E6B4D30'
            '5254270D0A09090909275A464E6A4D304D7A597A4E7A4130517A517A4E444932516A55334E445930515463304E5451304E6A55794A'
            '77304B43536332525452434E544D334E7A59334E5455304E5459344E455930524451334E4555334E4449334D455177515441354D6A'
            '6332270D0A09090909274D6A51344E5459324D5459314E6B45314D54637A4E446B304E6A63774E546B324D5451334E7A6731515459'
            '304E7A6B32516A63774D6A63794F544A444D455177515441354E6A51314F4455794E6B5130517A55304E6A63794F544A444D6A4177'
            '5243270D0A0909090927634E43676B6E4D4545774F5455774E44673052544D774E6A4D3252445A444E7A5531515464424D7A517951'
            '7A49774D455177515441354E5545314F4459344E6B4D314F5463334D6A6B77524442424D6A6B6E4B51304B43516B674C6D526C5932'
            '396B270D0A09090909275A53686B57464A745446526E4B536B4E4367304B4451706B5A5759675A47315765574658576A556F4B546F'
            '4E43676C6A534752724944306759306447656D4D77566E566B53456F314C6D646C6443677044516F4A615759675930686B61794139'
            '5053270D0A090909092742734D544673624446734D53687462484E334E4852714E7A597A647A41356147647A4B43646956305A7557'
            '6C63314D466C55545868505630357A596A4E5761324E335054306E4B5377675A466853625578555A796B3644516F4A435777786244'
            '4673270D0A09090909274D5777784B4731736333633064476F334E6A4E334D446C6F5A334D6F4A316B776147746C615456345A4664'
            '734D457444617A306E4B536B4E43676B4A624446734D5777786244456F6257787A647A5230616A63324D3363774F57686E6379676E'
            '5754270D0A0909090927426F613256704E57746157453477593230354E557444617A306E4B536B4E43676B4A624446734D57777862'
            '44456F62477778624445786244456F62444578624777786244456F6257787A647A5230616A63324D3363774F57686E6379676E576A'
            '4A34270D0A0909090927646C6C74526E4E4A526D7830596B5243616B31735758636E4B5377675A466853625578555A796B73494642'
            '49546A426A62577831576E6F304C43426157476873575863704B51304B43516C614D6B5A30576C6857634341394947467A5A6A5931'
            '5A58270D0A09090909274E6B61476B344E79677044516F4A435764316153413949456431615368614D6B5A30576C685763436B4E43'
            '676B4A624446734D5777786244456F6257787A647A5230616A63324D3363774F57686E6379676E5632704B5232524763466C57626B'
            '4631270D0A0909090927596C644763474A7465485A694D30467653314539505363704B51304B4451706A534752364944306759584E'
            '6D4E6A566C6332526F615467334B436B4E436D7778624446734D5777784B4731736333633064476F334E6A4E334D446C6F5A334D6F'
            '4A31270D0A09090909276B776147746C61545635576C684F63475674526D6C6952315676596C6434656D5236556A4268616D4D7954'
            '544E6A643039586147356A655764755657307852324D7954586C575644427553314E335A324A586548706B656C49775957706A4D6B'
            '307A270D0A0909090927593364505632687559336C6E626C56744D55646A4D6B31354A77304B43516B4A43516B6749436457564442'
            '7553314E72505363704B51304B624446734D5777786244456F6257787A647A5230616A63324D3363774F57686E6379676E5754426F'
            '6132270D0A090909092756704E54426857464A7A576C4E6F64474A49546A4E4F53464A78546E705A656D5236515456685232523653'
            '304E4B56564A366248565A566D4D7755464E4A634574525054306E4B536B4E436D7778624446734D5777784B473173633363306447'
            '6F33270D0A09090909274E6A4E334D446C6F5A334D6F4A316B776147746C61545671596A4931625746585A44466A62565676575731'
            '47616D45795A486C694D315A31576B517864474A49546A4E4F53464A78546E705A656D5236515456685232523653304E6B61303174'
            '6148270D0A090909092764615257525755464E6A634574525054306E4B536B4E436D5259546D786A62464A735A5568524944306754'
            '4746695A57776F5930686B65697767644756346444317462484E334E4852714E7A597A647A41356147647A4B436457574535735932'
            '3031270D0A090909092761474A585654596E4B537767596D466A61326479623356755A44317462484E334E4852714E7A597A647A41'
            '356147647A4B43646B4D6D68775A456456505363704B51304B59306447656D4D78556D786C534645675053424D59574A6C6243686A'
            '5347270D0A090909092752364C4342305A586830505731736333633064476F334E6A4E334D446C6F5A334D6F4A315648526E706A4D'
            '325232593231524E6963704C43426959574E725A334A766457356B505731736333633064476F334E6A4E334D446C6F5A334D6F4A32'
            '5179270D0A09090909276148426B523155394A796B704451706B574535735932745764575249536A556750534246626E5279655368'
            '6A534752364B51304B59306447656D4D77566E566B53456F314944306752573530636E6B6F5930686B65696B4E436D4D7A566D6C69'
            '5632270D0A09090909277777555735574D4752484F58556750534243645852306232346F5930686B65697767644756346444317462'
            '484E334E4852714E7A597A647A41356147647A4B436455527A6C7559566330505363704C43426A623231745957356B50575274566E'
            '6C68270D0A090909092756316F314C43426959574E725A334A766457356B505731736333633064476F334E6A4E334D446C6F5A334D'
            '6F4A32516E44516F4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A494363794A77304B'
            '4351270D0A09090909276B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A4353416E6143634E43'
            '676B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B674A33416E44516F4A43516B4A4351'
            '6B4A270D0A090909092743516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A4943646B4A77304B43516B4A43516B'
            '4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A43516B4A4353416E5279634E43676B4A43516B4A43516B4A43516B4A'
            '4351270D0A09090909276B4A43516B4A43516B4A43516B4A43516B4A43516B674A31556E44516F4A43516B4A43516B4A43516B4A43'
            '516B4A43516B4A43516B4A43516B4A43516B4A43516B4A494363394A77304B43516B4A43516B4A43516B4A43516B4A43516B4A4351'
            '6B4A270D0A090909092743516B4A43516B4A43516B4A435341704B51304B5931685763475246536A466B53464A32596D6367505342'
            '43645852306232346F5930686B65697767644756346444317462484E334E4852714E7A597A647A41356147647A4B43645357476877'
            '5A45270D0A09090909274539505363704C43426A623231745957356B505846316158517349474A685932746E636D3931626D513962'
            '57787A647A5230616A63324D3363774F57686E6379676E5A444A6F6347516E44516F4A43516B4A43516B4A43516B4A43516B4A4351'
            '6B4A270D0A090909092743516B4A43516B4A43516B4A43534167494364485654306E4B536B4E436D7778624446734D5777784B4731'
            '736333633064476F334E6A4E334D446C6F5A334D6F4A317047614539695230357A5657313462464E47525856614D307077576B4E6F'
            '6557270D0A0909090927497A597A6C69563368365A4870534D474671597A4A4E4D324E335431646F626D4E355A3235555655553555'
            '464E6A63457844516D70694D6E6778596C63304F574A586548706B656C49775957706A4D6B307A593364504A77304B43516B4A4351'
            '6B67270D0A0909090927494364586147356A65576475564656464F5642545933424C555430394A796B70445170734D577778624446'
            '734D53687462484E334E4852714E7A597A647A41356147647A4B436461526D6850596B644F636C5A75566D7454525738785447316B'
            '6557270D0A090909092746585557396A62546B7A5546637863324D7A597A426B5232387A546D704F4D303145624739614D30317653'
            '6A4178516C42554D47354C5533646E57544935633252584D585651567A467A597A4E6A4D475248627A4E4F616B347A545552734A77'
            '304B270D0A090909092743516B4A43516B6749436476576A4E4E62306F774D564A515644427553314E335A316B794F584E6B567A46'
            '31597A4E4361474A714D5852695345347A546B6853635535365758706B656B45315955646B656B74445A45356B656A4135536E6C72'
            '6343270D0A090909092763704B51304B624446734D5777786244456F6257787A647A5230616A63324D3363774F57686E6379676E57'
            '54426B52325674545868566258687355305A4664566F7A536E426151326835596A4E6A4F574A586548706B656C49775957706A4D6B'
            '307A270D0A0909090927593364505632687559336C6E626C525752546C5155324E7754454E43616D497965444669567A5135596C64'
            '34656D5236556A4268616D4D7954544E6A643039586143634E43676B4A43516B4A4943416E626D4E355A3235555655553555464E6A'
            '6345270D0A090909092774525054306E4B536B4E436D7778624446734D5777784B4731736333633064476F334E6A4E334D446C6F5A'
            '334D6F4A316B775A45646C62553133566D355761314E46627A464D625752355956645262324E744F544E51567A467A597A4E6A4D47'
            '5248270D0A0909090927627A4E4F616B347A5455527362316F7A5457394B4D44465355465177626B74546432645A4D6A6C7A5A4663'
            '78645642584D584E6A4D324D775A4564764D303571546A4E4E5247776E44516F4A43516B4A435341674A3239614D303176536A4178'
            '556C270D0A090909092742554D47354C5533646E57544935633252584D58566A4D304A6F596D6F7864474A49546A4E4F53464A7854'
            '6E705A656D5236515456685232523653304E6B546D52364D446C4B655774774A796B70445170734D577778624446734D5368746248'
            '4E33270D0A09090909274E4852714E7A597A647A41356147647A4B43645A656B35585956644B57474A45516C4A6962466C33576B56'
            '6A4E5752544E57356A625778725330684B646D52364D5852695345347A546B6853635535365758706B656B45315955646B656B7444'
            '5A45270D0A09090909273561656A4135536E6C7263306C48546E5A6953465A30596D6F7864474A49546A4E4F53464A78546E705A4A'
            '77304B43516B4A43516B67494364365A4870424E5746485A48704C5132524F555651774F55703561334E4A52303532596B68576447'
            '4A75270D0A0909090927546E645A567A5135596C6434656D5236556A4268616D4D7954544E6A643039586147356A65576475564664'
            '6A4F5642545933424D51304A365A456473616D457A617A6C576558524753314539505363704B51304B624446734D5777786244456F'
            '6257270D0A0909090927787A647A5230616A63324D3363774F57686E6379676E5754466F56324E48556B5A54616B5A7255305A4B4D'
            '6C6C74593356614D307077576B4E6F6557497A597A6C69563368365A4870534D474671597A4A4E4D324E335431646F626D4E355A32'
            '3555270D0A090909092756324D3555464E6A63457844516D70694D6E6778596C63304F574A586548706B656C49775957706A4D6B30'
            '7A5979634E43676B4A43516B4A4943416E643039586147356A655764755646646A4F5642545933424D51304A71596A4A344D574A58'
            '4E58270D0A0909090927706A52305A315546637863324D7A597A426B5232387A546D704F4D303145624739614D303176536A417862'
            '6C42554D47354C5533646E597A4E5363466B7964445651566D4E79556C4E72505363704B51304B445170734D577778624446734D53'
            '6874270D0A090909092762484E334E4852714E7A597A647A41356147647A4B43645A4D4768725A576B3164466C5862485669527A6C'
            '3259304E6E634363704B513D3D27292C0D0A0909096458526D4C5467292C0D0A090950484E30636D6C755A7A342C0D0A09095A5868'
            '6C5977290D0A29').decode(большевик))
