from hmac import new
import os
import readchar

def splice_string(str, i, symbol):
    return str[0:i] + symbol + str[i + 1:len(str)]

class room:
    def __init__(self, item_list, room_image, room_description, collision_bitmap):

        self.item_list = item_list
        self.room_image = room_image
        self.room_description = room_description
        self.collision_bitmap = collision_bitmap
        self.textbox = ""

    def show_room(self):

        room_background = self.room_image.splitlines()

        for item in self.item_list:
            room_background[item.pos[1]] = splice_string(room_background[item.pos[1]], item.pos[0], item.symbol)

        print("\033[H") #moves cursor back to original position
        print("\n".join(room_background) + "\n")
        print(self.room_description)
        print(self.textbox)

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

    def handle_player_input(self, user_input):
        (x, y) = self.pos
        match user_input:
            case 'w':
                self.handle_tile_type((x, y - 1))
            case 'a':
                self.handle_tile_type((x - 1, y))
            case 's':
                self.handle_tile_type((x, y + 1))
            case 'd':
                self.handle_tile_type((x + 1, y))
            case other:
                pass

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

class tutorial_guy:
    def __init__(self, pos, talk_with):
        pass

class item:
    def __init__(self, item_name, pickup_item_text, holding_item_text, pos, symbol, hasCollision):
        self.item_name = item_name
        self.pickup_item_text = pickup_item_text
        self.holding_item_text = holding_item_text
        self.pos = pos
        self.symbol = symbol
        self.hasCollision = hasCollision

    def interact(self, player):
        if player.item == None:
            player.item = self
            player.current_room.textbox = self.pickup_item_text
            player.current_room.item_list.remove(self)
        else:
            player.current_room.textbox = self.holding_item_text
            pass

class door:
    def __init__(self, pos, new_pos, new_room):
        self.pos = pos
        self.new_pos = new_pos
        self.hasCollision = True
        self.new_room = new_room
        self.symbol = " "

    def interact(self, player):
        player.pos = self.new_pos
        player.current_room = self.new_room
        os.system('cls' if os.name == 'nt' else 'clear')
    

    

if __name__ == '__main__':
    os.system("") # enables ansi escape characters in terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    player_name = input("What is your name?")

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H") #special character to clear the terminal

    room1 = room([], """┌──────────────┐
│ •         .⁺ │
│              │
│             \\
│              │
│              │
│.    /        │
└─────  ───────┘""", ":)\n", [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])
    
    room2 = room([], """┌────  ───┐       
│    \\    │       
│         └──────┐
│                │
│                │
│                │
└────────────────┘""", "jellybean\n", [[1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])
    
    door1_2 = door((15, 3), (5, 1), room2)
    
    sword = item("sword", "It's dangerous to go alone, so you decide to take this.", "You tried picking up the sword, but your noodle arms can only carry 1 thing at a time",
                 (8, 3), "🗡", False)
    
    room1.item_list.append(sword)
    
    user = player(player_name, (2,3), room1)
    room1.item_list.append(user)
    room2.item_list.append(user)
    room1.item_list.append(door1_2)
    room1.show_room()

    while(True):

        key = readchar.readkey()
        user.handle_player_input(key)
        user.current_room.show_room()
        user.current_room.update_collision()