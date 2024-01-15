from hmac import new
import os
import readchar
from gamedata import *

#You need to write a function that replaces a character at a particular position ("i") in a string with "symbol".
#You are given the string you need to alter ("str"), the position ("i"), and the "symbol".
#You must return the altered string.
#Hint: a string is just a list of characters, remember lists in computer language always with 0.
def splice_string(str, i, symbol):

    #write your code here!
    pass #delete "pass" once you have written code

class room:
    def __init__(self, item_list, room_image, room_description, collision_bitmap):

        self.item_list = item_list
        self.room_image = room_image
        self.room_description = room_description
        self.collision_bitmap = collision_bitmap
        self.textbox = ""

    def show_room(self):
        room_background = self.room_image.splitlines()

        #item generation on the room background image, splice string is used to generate items
        for item in self.item_list:
            room_background[item.pos[1]] = splice_string(room_background[item.pos[1]], item.pos[0], item.symbol)

        print("\033[H") #moves cursor back to original position

        #since we split apart our room background image, we have to join it together again
        print("\n".join(room_background) + "\n")
        print(self.room_description)
        print(self.textbox)

    #a function that updates the room bitmap to indicate what tile is which type.
    #type 1 is a wall, 2 is a walkable item (player can walk through it), 3 is a collidable item. 0 is an empty, regular tile.
    #called every time a room is shown.
    def update_collision(self):
        for item in self.item_list:
            if not isinstance(item, player):
                self.collision_bitmap[item.pos[1]][item.pos[0]] = 3 if item.hasCollision else 2



class player:
    def __init__(self, name, pos, current_room):
        self.name = name
        self.item = None
        self.pos = pos
        self.current_room = current_room
        self.symbol = name[0]

    #You will need to write the conditional logic that processes character movement.
    #'w' and 'q' is already done as an example. There is nothing to return.
    def handle_player_input(self, user_input):
        (x, y) = self.pos

        if user_input == 'w':
            self.handle_tile_type((x, y - 1))

        #write your code here!
            
        
        elif 'q':
            exit()
        else:
            pass

    #checks the properties of the tile the player will move into. Based on tile type defined in the bitmap, there may be item interactions.
    def handle_tile_type(self, new_pos):
        (new_x, new_y) = new_pos

        tile = self.current_room.collision_bitmap[new_y][new_x]

        if tile & 1 == 0:
            self.pos = new_pos
        if tile & 2 == 2:
            for item in self.current_room.item_list:
                if item.pos == new_pos and item is not self:
                    item.interact(self)
                    break
        else:
            pass

#Here is the start of all item/npc classes, each follows a similar format, with a constructor and an interact function.
#The interact function sets the text the terminal will display when the player walks into it. 
class item:
    def __init__(self, item_name, pickup_item_text, holding_item_text, pos, symbol, hasCollision, canPickUp):
        self.item_name = item_name
        self.pickup_item_text = pickup_item_text
        self.holding_item_text = holding_item_text
        self.pos = pos
        self.symbol = symbol
        self.hasCollision = hasCollision
        self.canPickUp = canPickUp

    def interact(self, player):
        if player.item == None:
            player.current_room.textbox = self.pickup_item_text
            if self.canPickUp:
                player.item = self
                player.current_room.item_list.remove(self)
        else:
            player.current_room.textbox = self.holding_item_text
            pass

class boss:
    def __init__(self, pos, symbol, weapon_room, next_weapon):
        self.pos = pos
        self.hasCollision = True
        self.symbol = symbol
        self.weapon_room = weapon_room
        self.next_weapon = next_weapon

    def interact(self, player):
        if player.item is None:
            player.current_room.textbox = "You wave to the slime. It is quite intimidating, so maybe you won't do that again."
        elif player.item is not chocolate:
            player.current_room.textbox = boss_text[player.item.item_name]
            if self.next_weapon[player.item.item_name] != None:
                self.weapon_room.item_list.append(self.next_weapon[player.item.item_name])
            player.item = None
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(win_screen)
            exit()

class tutorial_guy:
    def __init__(self, pos, symbol):
        self.pos = pos
        self.symbol = symbol
        self.hasCollision = True

    def interact(self, player):
        if player.item == None:
            player.current_room.textbox = "There's a big ol' slime causing a ruckus!\n It's been making a huge mess around here."
        else:
            player.current_room.textbox = tutorial_guy_text[player.item.item_name]

class door:
    def __init__(self, pos, new_pos, new_room):
        self.pos = pos
        self.new_pos = new_pos
        self.hasCollision = True
        self.new_room = new_room
        self.symbol = " "

    def interact(self, player):
        player.pos = self.new_pos
        player.current_room.textbox = ""
        player.current_room = self.new_room
        os.system('cls' if os.name == 'nt' else 'clear')
    

def instantiate_game(name):
    global room1, room2, room3, room4, room5
    global door1_2_0, door1_2_1, door1_2_2, door3_2, door4_2_0, door4_2_1, door4_2_2, door5_2, door2_1_0, door2_1_1, door2_1_2, door2_3, door2_4_0, door2_4_1, door2_4_2, door2_5
    global stick, sword, chainsaxe, rubberducky, chocolate, user

    rubberducky = item("duck", item_pickup["duck"], item_fail_pickup["duck"], (17, 4), "🦆", False, True)
    stick = item("stick", item_pickup["stick"], item_fail_pickup["stick"], (17, 4), "ᚬ", False, True)
    sword = item("sword", item_pickup["sword"], item_fail_pickup["sword"], (17, 4), "🗡", False, True)
    chainsaxe = item("greg's chainsaw axe", item_pickup["chainsaxe"], item_fail_pickup["chainsaxe"], (17, 4), "🪓", False, True)
    #Initialize your strongest weapon here! Remember to add your weapon to the "slime_next_weapon" dictionary down below and add text to the gamedata.py file.

    chocolate = item("hershey's", item_pickup["chocolate"], item_fail_pickup["chocolate"], (1,5), "⌧", False, True)
    old_man = tutorial_guy((8, 4), "🯆")

    #Add your weapon here!
    slime_next_weapon={
        "duck": None,
        "stick": sword,
        "sword": chainsaxe,
        "greg's chainsaw axe": None,
        "hershey's": None
    }

    room1 = room([chocolate], room_bgs[0], room_descriptions[0], room_bitmaps[0])
    room2 = room([old_man], room_bgs[1], room_descriptions[1], room_bitmaps[1])
    room3 = room([], room_bgs[2], room_descriptions[2], room_bitmaps[2])
    room4 = room([stick], room_bgs[3], room_descriptions[3], room_bitmaps[3])

    slime0 = boss((35, 3),"╭", room4, slime_next_weapon)
    slime1 = boss((35, 4),"🤇", room4, slime_next_weapon)
    slime2 = boss((35, 5),"╰", room4, slime_next_weapon)

    room5 = room([slime0, slime1, slime2], room_bgs[4], room_descriptions[4], room_bitmaps[4])

    door1_2_0 = door((5,8),(7,1), room2)
    door1_2_1 = door((6,8),(8,1), room2)
    door1_2_2 = door((7,8),(9,1), room2)
    door3_2 = door((19,6),(1,4), room2)
    door4_2_0 = door((8,1),(7,7), room2)
    door4_2_1 = door((9,1),(8,7), room2)
    door4_2_2 = door((10,1),(9,7), room2)
    door5_2 = door((0,4),(15,4), room2)
    door2_1_0 = door((7,0),(5,7), room1)
    door2_1_1 = door((8,0),(6,7), room1)
    door2_1_2 = door((9,0),(7,7), room1)
    door2_3 = door((0,4),(18,6),room3)
    door2_4_0 = door((7,8),(8,2), room4)
    door2_4_1 = door((8,8),(9,2), room4)
    door2_4_2 = door((9,8),(10,2), room4)
    door2_5 = door((16,4),(1,4),room5)

    room1.item_list.append(door1_2_0)
    room1.item_list.append(door1_2_1)
    room1.item_list.append(door1_2_2)
    room3.item_list.append(door3_2)
    room4.item_list.append(door4_2_0)
    room4.item_list.append(door4_2_1)
    room4.item_list.append(door4_2_2)
    room5.item_list.append(door5_2)
    room2.item_list.append(door2_1_0)
    room2.item_list.append(door2_1_1)
    room2.item_list.append(door2_1_2)
    room2.item_list.append(door2_3)
    room2.item_list.append(door2_4_0)
    room2.item_list.append(door2_4_1)
    room2.item_list.append(door2_4_2)
    room2.item_list.append(door2_5)

    user = player(name, (2,3), room3)
    user.item = rubberducky
    room1.item_list.append(user)
    room2.item_list.append(user)
    room3.item_list.append(user)
    room4.item_list.append(user)
    room5.item_list.append(user)

if __name__ == '__main__':
    os.system("") # enables ansi escape characters in terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    player_name = input("What is your name?\n\t")

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H")

    instantiate_game(player_name)
    
    room3.show_room()

    while(True):

        key = readchar.readkey()
        user.handle_player_input(key)
        user.current_room.show_room()
        user.current_room.update_collision()