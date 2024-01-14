import os
import readchar

def splice_string(str, i, symbol):
    return str[0:i] + symbol + str[i + 1:len(str)]

class room:
    def __init__(self, north, east, south, west, item_list, room_image, room_description, collision_bitmap):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.item_list = item_list
        self.room_image = room_image
        self.room_description = room_description
        self.collision_bitmap = collision_bitmap

    def show_room(self):

        room_background = self.room_image.splitlines()

        for item in self.item_list:
            room_background[item.pos[1]] = splice_string(room_background[item.pos[1]], item.pos[0], item.symbol)

        print("\033[H") #special character to clear the terminal
        print("\n".join(room_background) + "\n")
        print(self.room_description)



class player:
    def __init__(self, name, pos, current_room):
        self.name = name
        self.item = "rubber ducky"
        self.pos = pos
        self.current_room = current_room
        self.symbol = name[0]

    def handle_player_input(self, user_input):
        (x, y) = self.pos
        match user_input:
            case 'w':
                if self.current_room.collision_bitmap[y - 1][x] == 0:
                    y -= 1
            case 'a':
                if self.current_room.collision_bitmap[y][x - 1] == 0:
                    x -= 1
            case 's':
                if self.current_room.collision_bitmap[y + 1][x] == 0:
                    y += 1
            case 'd':
                if self.current_room.collision_bitmap[y][x + 1] == 0:
                    x += 1
            case other:
                pass
        
        self.pos = (x,y)



if __name__ == '__main__':
    os.system("") # enables ansi escape characters in terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    room1 = room(0, 0, 0, 0, [], """┌──────────────┐
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
    
    kevin = player("Kevin", (2,3), room1)
    room1.item_list.append(kevin)
    room1.show_room()

    while(True):

        key = readchar.readkey()
        kevin.handle_player_input(key)
        room1.show_room()