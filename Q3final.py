import sys
import random
import time

#Player Stats
love = 1
exp = 0
max_exp = 20
hp = 20
max_hp = 40
karma = 0
name = "ryu"
#We use a temporary list to make sure names don't break the box
#Player Inventory
inv = []
           
#Food Inventory
foodinv = []

#Monster Art Credits https://gemini.google.com/share/732ef73a467c
kitty_monster = r'''
                     /\_/\
                    ( o.o )
                     > ^ <
                    /     \
                   (| . . |)
                    \_____/'''

mole_monster = r'''
                / \  // 
               |\_/_/ /
               /  `  /_
              |  o  o  |  ___
              |   ||   | / _ \
              \   --   /| | | |
               `------` |_| |_|
               /      \  /  /
              /|      |\|  /
               \______/ `"`
                ||  ||
                ^`  ^`
'''
clover_monster = r''''''

obscurus_monster = r''''''

rău_monster = r''''''

garamond_monster = r''''''

def level_up():
    global love, exp, max_exp, hp, max_hp 

    while exp >= max_exp:
        love += 1
        exp -= max_exp  #Subtract the requirement to keep the 'leftover' EXP so it goes into the next levels
        
        #Increase the requirements for the NEXT level
        max_exp = int(max_exp * 1.5) 
        
        #Increase max hp by 10
        max_hp += 10
        hp = max_hp  #Fully heals player everytime they level up
        
        print(f"\n[!] LOVE INCREASED! You are now LOVE {love}!")
        print(f"[!] Max HP is now {max_hp}!")
        time.sleep(1)


#Monster Class
class Monster:
    def __init__(self, name, art, hp, maxhp, exp_drop, monster_dmg, mercy_chance, monster_karma):
        self.name = name
        self.art = art
        self.hp = hp
        self.maxhp = maxhp
        self.exp_drop = exp_drop
        self.monster_dmg = monster_dmg
        self._mercy_chance = mercy_chance
        self.monster_karma = monster_karma

#Creating the monsters
kitty = Monster("Kitty", kitty_monster, 20, 20, 3, 4, 90, 1)
mole = Monster("Mole", mole_monster, 30, 30, 5, 6, 85, 3)
obscurus = Monster("Obscurus", obscurus_monster, 100, 100, 20, 15, 10, 5)
rau = Monster("Rău", rău_monster, 200, 200, 50, 20, 5, 10)
garamond = Monster("Garamond", garamond_monster, 350, 350, 75, 40, 3, 15)
clover = Monster("Clover", clover_monster, 150, 150, 100, 20, 1, 50)


#Fight battle ASCII credits to https://gemini.google.com/share/62ff69091c7b
def fight_scene(enemy):


    sys.stdout.write("\033[H")#Jump to top-left
    sys.stdout.write("\033[J") #Clear the line

    monster_stats = f"{enemy.name}: {enemy.hp}/{enemy.maxhp}".ljust(20) #ljust is to make the spaces after the name constant. credits to https://gemini.google.com/share/3b1a682d0ddc
    player_stats = f"HP: {hp}/{max_hp}".ljust(14) #So that the stats box will stay intact regardless of the length of the name.

    print(f'''    
          
{enemy.art}
╔════════════════════════════════════════════════╗
║ {monster_stats}                                ║ 
║ {player_stats}                                 ║ 
╠════════════════════════════════════════════════╣
║ [A] ATTACK        [H] HEAL          [P] SPARE  ║
╚════════════════════════════════════════════════╝
          ''')


line = "\033[K"




#Attack function
#Credits to https://gemini.google.com/share/930902e408bf for attributes inside def bracket
def attack(enemy, amount):
    enemy.hp -= amount
    if enemy.hp < 0:
        enemy.hp = 0

    dmg_text = f"HIT! -{amount}" #Red and bold text credits to https://gemini.google.com/share/0ae44afd001c

    sys.stdout.write("\033[17A")#Jump up so the damage text will be above the stats box
    sys.stdout.write(dmg_text)
    sys.stdout.flush()

    #Credits to https://gemini.google.com/share/4ee0b6718017 for making the enemy shake after damaged
    #Shake right
    sys.stdout.write("\033[H") # Jump to top-left
    # We add 3 spaces to every line of the art to push it right
    #replace("\n", "\n   ") adds spaces after every 'Enter' key in the art
    print("\n   " + enemy.art.replace("\n", "\n   ")) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake left
    sys.stdout.write("\033[H") # Jump to top-left
    print("\n" + enemy.art) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake right 
    sys.stdout.write("\033[H")
    print("\n   " + enemy.art.replace("\n", "\n   ")) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake left
    sys.stdout.write("\033[H") # Jump to top-left
    print("\n" + enemy.art) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake right 
    sys.stdout.write("\033[H")
    print("\n   " + enemy.art.replace("\n", "\n   ")) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake left
    sys.stdout.write("\033[H") # Jump to top-left
    print("\n" + enemy.art) 
    sys.stdout.flush()
    time.sleep(0.07)

    #Shake right 
    sys.stdout.write("\033[H")
    print("\n   " + enemy.art.replace("\n", "\n   ")) 
    sys.stdout.flush()
    time.sleep(0.07)

    fight_scene(enemy) #Redraws the fight scene with the new stats after the attack



#This handles everything about the fight, it has damage def inside and fight scene def inside, so that when you call fight_function(), it will run the whole fight sequence. 
def fight_function(enemy):
    fight_scene(enemy)
    
    global hp, karma, exp 

    while enemy.hp > 0:
        action = input("Choose your action: ").upper()

        if action == "A":
            #Clears the fight scene to show weapon inventory
            sys.stdout.write("\033[H\033[J")
            placeholder_inv = ["Empty", "Empty", "Empty"]
            #to put the correct weapons in each placeholder slot
            for i in range(len(inv)):
                placeholder_inv[i] = inv[i]
            print(f"""
            ╔══════════════════════════ WEAPONS ═══════════════════════════╗
            ║                                                              ║
            ║    1.   * {placeholder_inv[0]:<15}                                    ║
            ║                                                              ║
            ║    2.   * {placeholder_inv[1]:<15}                                    ║
            ║                                                              ║
            ║    3.   * {placeholder_inv[2]:<15}                                    ║                                                 
            ║                                                              ║ 
            ╚══════════════════════════════════════════════════════════════╝
            """)
            #i is the counter, item is the string in the list
            for i, item in enumerate(inv):
                    print(f"[{i+1}] {item}")

            weapon_choice = input("What weapon would you like to use to attack? (Pick 1, 2 or 3): ")
            #To make sure theres only the amount of weapons in the list. (in this case 3)
            if weapon_choice.isdigit() and 0 < int(weapon_choice) <= len(inv):
                #To make 1 into 0, 2 into 1, etc. To match the index values
                index = int(weapon_choice) - 1
                selected_weapon = inv[index]

                #To take only the damage part of the weapon, excluding the name. https://gemini.google.com/share/28b3a70a0eca
                dmg = int(selected_weapon.split("(")[1].split(" ")[0])

                print(f"You used the {selected_weapon}!")
                attack(enemy, dmg)

                #Monster's turn to attack
                if enemy.hp > 0:
                    print(f"{enemy.name} is attacking!!")
                    time.sleep(1)

                    print(f"You got hit for {enemy.monster_dmg} HP!")

                    hp -= enemy.monster_dmg

                    #Death function
                    if hp <= 0:
                        print("You died...restart?")
                        exit()

                    time.sleep(1)
                    fight_scene(enemy)

            else:
                print("Invalid choice, pick a valid slot!") 
                time.sleep(1)

            fight_scene(enemy)   

        elif action == "H":
            #Clears the fight scene to show food inventory
            sys.stdout.write("\033[H\033[J")
            placeholder_foodinv = ["Empty", "Empty", "Empty"]
            #to place each food in the correct placeholder spot
            for i in range(len(foodinv)):
                placeholder_foodinv[i] = foodinv[i]
            print(f"""
            ╔══════════════════════════ FOOD ══════════════════════════════╗
            ║                                                              ║
            ║    1.   * {placeholder_foodinv[0]:<15}                       ║
            ║                                                              ║
            ║    2.   * {placeholder_foodinv[1]:<15}                       ║
            ║                                                              ║
            ║    3.   * {placeholder_foodinv[2]:<15}                       ║                                                 
            ║                                                              ║ 
            ╚══════════════════════════════════════════════════════════════╝
            """)
            #i is the counter, item is the string in the list
            for i, item in enumerate(foodinv):
                    print(f"[{i+1}] {item}")

            food_choice = input("What food would you like to eat? (Pick 1, 2 or 3): ")
            #To make sure theres only the amount of weapons in the list. (in this case 3)
            if food_choice.isdigit() and 0 < int(food_choice) <= len(foodinv):
                #To make 1 into 0, 2 into 1, etc. To match the index values
                index = int(food_choice) - 1
                selected_food = foodinv.pop(index)

                #To take only the damage part of the weapon, excluding the name. https://gemini.google.com/share/28b3a70a0eca
                heal_amount = int(selected_food.split("+(")[1].split(" ")[0])

                hp += heal_amount
                if hp > max_hp:
                    hp = max_hp

                print(f"You ate the {selected_food}!")
                time.sleep(1)

                #Monster's turn to attack
                if enemy.hp > 0:
                    print(f"{enemy.name} is attacking!!")
                    time.sleep(1)

                    print(f"You got hit for {enemy.monster_dmg} HP!")

                    hp -= enemy.monster_dmg

                    #Death function
                    if hp < 0:
                        print("You died...restart?")
                        exit()

                    time.sleep(1)
                    fight_scene(enemy)
                
            else:
                print("Invalid choice!")
                time.sleep(1)

            fight_scene(enemy)

        elif action == "P":
            print(f"\n* You reach out to {enemy.name}...")
            time.sleep(1)
            
            roll = random.randint(1, 100)
            
            #Check if roll hits 
            if roll <= enemy._mercy_chance:
                print(f"* {enemy.name} accepts your mercy. The air grows calm.")
                karma += enemy.monster_karma
                time.sleep(1)
                break
            else:
                #Roll fails, battle keeps going
                print(f"* {enemy.name} ignores your mercy!")
                time.sleep(1)
                                
                #Death function
                if hp <= 0:
                    print("\n[!] Your soul shattered... Game Over. Try again?")
                    exit()
                
                time.sleep(1)
                fight_scene(enemy) # Redraw the box so you see your lower HP

        else:
            print("Invalid action, try again.")
            time.sleep(1)
            fight_scene(enemy)

        if enemy.hp == 0:
            print(f"You defeated {enemy.name}!")
            print(f"You gained {enemy.exp_drop} EXP!")
            exp += enemy.exp_drop
            karma -= enemy.monster_karma
            level_up()
            break



#Weapons
class Weapon:
    def __init__(self, name, dmg):
        self.name = name
        self.dmg = dmg
        
stick = Weapon("Stick", 5) 
dagger = Weapon("Dagger", 7)
rapier = Weapon("Rapier", 10)
greataxe = Weapon("Rusty Greataxe", 25)
legendary_sword = Weapon("Legendary Sword", 35)
corrupted_saber = Weapon("Corrupted Saber", 50)
void_stitcher = Weapon("Void Stitcher", 70)
whisper = Weapon("Whisper of the Abyss", 100)



#Food
class Food:
    def __init__(self, name, heal):
        self.name = name
        self.heal = heal

donut = Food("Donut", 10)
pie = Food("Pie", 15)
soul_burger = Food("Soul Burger", 20)
soda = Food("Soda", 30)
golden_apple = Food("Golden Apple", 50)

#Function for picking up weapons
def add_weapon(weapons):
    
    wpn = f"{weapons.name} ({weapons.dmg} dmg)"

    if len(inv) < 3:
        inv.append(wpn)
    else:
        print("\nInventory full! Delete something first.")
        show_stats() #Shows the stats box so the player can choose what to delete to make space for the new weapon

#Function for picking up food
def add_food(foods):

    consumables = f"{foods.name} +({foods.heal} HP)"

    if len(foodinv) < 3:
        foodinv.append(consumables)
        print(f"You picked up a {foods.name}!")
    else:
        print("Inventory full! Delete something first.")
        show_stats() #Shows the stats box so the player can choose what to delete to make space for the new food


#Chests Class
class Chest:
    def __init__(self, name, content1, content2, content3, content4, content5, content1chance, content2chance, content3chance, content4chance, content5chance):
        self.name = name
        self.content1 = content1
        self.content2 = content2
        self.content3 = content3
        self.content4 = content4
        self.content5 = content5
        self.content1chance = content1chance
        self.content2chance = content2chance
        self.content3chance = content3chance
        self.content4chance = content4chance
        self.content5chance = content5chance


Common_chest = Chest(
    "Common Chest", 
    dagger, rapier, greataxe, legendary_sword, None,  # Items
    0.6, 0.20, 0.09, 0.02, 0.0              # Chances 
)

Rare_chest = Chest(
    "Rare Chest", 
    dagger, rapier, greataxe, legendary_sword, corrupted_saber, 
    0.5, 0.3, 0.1, 0.05, 0.01
)

Epic_chest = Chest(
    "Epic Chest",
    rapier, greataxe, legendary_sword, corrupted_saber, void_stitcher, 
    0.35, 0.4, 0.1, 0.05, 0.01
)

Legendary_chest = Chest(
    "Legendary Chest", 
    legendary_sword, corrupted_saber, void_stitcher, whisper, None,
    0.5, 0.2, 0.1, 0.005, 0.0
)

mystery_chest = Chest(
    "??? Chest",
    corrupted_saber, void_stitcher, whisper, None, None, 
    0.5, 0.35, 0.15, 0.0, 0.0 
)

def chest_open(chest_to_open):
    print(f"\n* You found a {chest_to_open.name}!")
    input("  [ Press Enter to open ]")

    items = [chest_to_open.content1, chest_to_open.content2, chest_to_open.content3, chest_to_open.content4, chest_to_open.content5]
    chances = [chest_to_open.content1chance, chest_to_open.content2chance, chest_to_open.content3chance, chest_to_open.content4chance, chest_to_open.content5chance]
    #credits to https://gemini.google.com/share/cbf8a9bed0b3 for function of random.weight (taking variables from lists,etc.)
    obtained_item = random.choices(items, weights=chances, k=1)[0]

    chest_art = r'''
          _________________________
         /                        /|
        /________________________/ |
       |________________________|  |
       |                        |  | 
       |      [Opening...]      | /
       |________________________|/
'''
    print(chest_art)
    time.sleep(1)

    sys.stdout.write("\033[H\033[J") # Clear screen
    chest_art_result = f'''
          _________________________
         /                        /|
        /________________________/ |
       |________________________|  |
       |                        |  | 
       |  {obtained_item.name:^22}| /
       |________________________|/
'''
    print(chest_art_result)
    chest_obtain = (f"\n* You obtained {obtained_item.name}!")
    for character in chest_obtain:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(0.06)

    add_weapon(obtained_item) 






#:< function is to make the spaces after the name constant, so that the stats box will stay intact regardless of the length of the name.
#(E.G. if the name is "Ryu", there will be 10 spaces after it, but if the name is "Ryu Honda", there will still be 10 spaces after it, so the stats box will stay the same.)
# credits to https://gemini.google.com/share/8b064a893bfe
def show_stats():

    #Placeholder inventory to avoid errors (E.g, if inv is full then cannot pickup, but if inv empty then index error)
    #credits to https://gemini.google.com/share/1989dceedc51

    placeholder_inv = ["Empty", "Empty", "Empty"]

    if len(inv) > 0: placeholder_inv[0] = inv[0] #ONLY if the weapons exist in original inv list, then placeholder_inv will update
    if len(inv) > 1: placeholder_inv[1] = inv[1]
    if len(inv) > 2: placeholder_inv[2] = inv[2] 

    placeholder_foodinv = ["Empty", "Empty", "Empty"]

    if len(foodinv) > 0: placeholder_foodinv[0] = foodinv[0] #ONLY if the foods exist in original foodinv list, then placeholder_foodinv will update
    if len(foodinv) > 1: placeholder_foodinv[1] = foodinv[1]
    if len(foodinv) > 2: placeholder_foodinv[2] = foodinv[2]


    final_exp = (f"{exp}/{max_exp}")
    final_hp = (f"{hp}/{max_hp}")

    print(f"""
  ╔══════════════════════════════════ STATS ══════════════════════════════════╗
  ║                                                                           ║
  ║  NAME: {name:<20}                LOVE: {love:<20}     ║
  ║  HP:   {final_hp:<20}                EXP:  {final_exp:<20}     ║
  ║                                                                           ║
  ╠════════════════════════════════ INVENTORY ════════════════════════════════╣
  ║                                                                           ║
  ║      WEAPONS                                  FOOD                        ║
  ║                                                                           ║
  ║  * {placeholder_inv[0]:<35}  * {placeholder_foodinv[0]:<20}            ║
  ║  * {placeholder_inv[1]:<35}  * {placeholder_foodinv[1]:<20}            ║
  ║  * {placeholder_inv[2]:<35}  * {placeholder_foodinv[2]:<20}            ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
""")
    
    #Function to delete items from inventory if the player wants to, to make space for new items.
    while True:
            delete_choice = input("Would you like to delete any items? (Y/N): ").upper()

            if delete_choice == "Y":
                item_type = input("Delete from (W)eapons or (F)ood? ").upper()
                
                if item_type == "W":
                    delete_weapon = input("Which weapon slot? (1, 2 or 3): ")
                    if delete_weapon.isdigit() and 0 < int(delete_weapon) <= len(inv):
                        index = int(delete_weapon) - 1
                        removed_item = inv.pop(index)
                        print(f"You discarded the {removed_item}.")
                        break
                    else:
                        print("Invalid slot or slot is already empty!")

                elif item_type == "F":
                    delete_food = input("Which food slot? (1, 2 or 3): ")
                    if delete_food.isdigit() and 0 < int(delete_food) <= len(foodinv):
                        index = int(delete_food) - 1
                        removed_item = foodinv.pop(index)
                        print(f"You discarded the {removed_item}.")
                        break
                    else:
                        print("Invalid slot or slot is already empty!")

            elif delete_choice == "N":
                break
            else:
                print("Invalid choice! Please type Y or N.")

#Function for random chests
def find_random_chest():
    # List of possible chests
    all_chests = [Common_chest, Rare_chest, Epic_chest, Legendary_chest, mystery_chest]
    
    # 70% Common, 20% Rare, 8% Epic, 2% Legendary
    rarity_weights = [0.65, 0.20, 0.1, 0.04, 0.01] 
    
    found_chest = random.choices(all_chests, weights=rarity_weights, k=1)[0]
    chest_open(found_chest)


def intro():
#Box credits to https://www.asciiart.eu/ascii-borders/maker "Strong Corners"
    box = ("""
╔═════════════════════════════════════════════════════════╗
║                                                         ║
║                                                         ║
║                                                         ║
║                                                         ║
║                                                         ║
╚═════════════════════════════════════════════════════════╝""")

#Credits to https://gemini.google.com/share/eddd0b0d35ab for the function to put a print statement in "box" and using sys
    print(box)


#STORY BASED ON PLOT OF THE GAME "Undertale" by Toby Fox

#List #1
    intro_texts = [
        ["* Long ago, two sides lived in harmony.", " HUMANS and MONSTERS...", 3.0],
        ["* The world was peaceful,", "but fear began to grow in the humans hearts.", 2.5],
        ["* They feared the monsters would attack them,", "and rumors began to spread.", 2.0],
        ["* Whispers turned into words,", "and words turned into shouts.", 2.5],
        ["* Hatred began to spread amongst everyone,", "wrath consuming the world...", 2.0],
        ["* War broke out between the two sides.", "Humans triumphed, sealing the monsters underground.", 3.5],
        ["* Deep in the Whispering Woods,", "lies a Great Hollow..", 2.0],
        ["* A place where the monsters were sealed away.", "Many have tried to enter, but none have returned.", 3.0],
        ["* You are a child who fell into the Great Hollow.", "Your adventure begins here...", 3.0]
    ]

    sys.stdout.write("\033[5A") #Moves the text 4 spaces up so it is inside the box

    #To seperate every sentence in the list.
    for sentences in intro_texts:

        current_sentence = sentences[0]
        current_sentence1 = sentences[1] 
        time_to_wait = sentences[2] 


        #Function for text printing one letter at a time 

        #First line
        sys.stdout.write("\r\033[5C") #Moves the text 5 spaces to the right so it is inside the box
        for character in current_sentence:
            sys.stdout.write(character)#Character = One letter
            sys.stdout.flush() #To display text
            time.sleep(0.09) #Time it takes for one letter to load

        #Second line
        sys.stdout.write("\n\033[5C") #Moves the text 5 spaces to the right, uses \n to move it down, credits https://gemini.google.com/share/4f31f4d93f09
        for character in current_sentence1:
            sys.stdout.write(character) #Character = One letter
            sys.stdout.flush() #To display text
            time.sleep(0.09) #Time it takes for one letter to load


        time.sleep(time_to_wait) #Time it takes for the text to load after the prevous one

    #Eraser: Replaces the line with spaces (makes it seem like the text gets deleted then next line comes)
        sys.stdout.write("\r\033[5C" + " " * 50)
        sys.stdout.write("\033[1A") 
        sys.stdout.write("\r\033[5C" + " " * 50) #Moves the output up so that the next line will be printed on the upper sentence


    sys.stdout.write("\033[5B\r")


#Flag 1
menu_choice = True


#Credits to https://gemini.google.com/share/6c1434ffeb76
game_menu = ("""
+--------------------------------------------------------------------+
|                                                                    |
|        ██╗  ██╗ ██████╗ ██╗     ██╗      ██████╗ ██╗    ██╗        |
|        ██║  ██║██╔═══██╗██║     ██║     ██╔═══██╗██║    ██║        |
|        ███████║██║   ██║██║     ██║     ██║   ██║██║ █╗ ██║        |
|        ██╔══██║██║   ██║██║     ██║     ██║   ██║██║███╗██║        |
|        ██║  ██║╚██████╔╝███████╗███████╗╚██████╔╝╚███╔███╔╝        |
|        ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝         |
|                                                                    |
|               ███╗   ███╗██╗   ██╗████████╗██╗  ██╗                |
|               ████╗ ████║╚██╗ ██╔╝╚══██╔══╝██║  ██║                |
|               ██╔████╔██║ ╚████╔╝    ██║   ███████║                |
|               ██║╚██╔╝██║  ╚██╔╝     ██║   ██╔══██║                |
|               ██║ ╚═╝ ██║   ██║      ██║   ██║  ██║                |
|               ╚═╝     ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝                |
|                                                                    |
+--------------------------------------------------------------------+
|                                                                    |
|                        [ 1 ]  PLAY GAME                            |
|                                                                    |
|                        [ 2 ]  CREDITS                              |
|                                                                    |
|                        [ 3 ]  REPLAY INTRO                         |
|                                                                    |
|                        [ 4 ]  CONTROLS                             |
|                                                                    |
+--------------------------------------------------------------------+
|                   USE NUMBERS TO SELECT AN OPTION                  |
+--------------------------------------------------------------------+
""")                                              


add_weapon(stick) #Player starts with a stick weapon in inventory

print(game_menu)
while menu_choice:
    choice = input("Please select an option by entering a number: ")

    if choice == "1":
        print("Hello, user.")
        menu_choice = False
    elif choice == "2":
        print("This game was made by Ryu Matthew Honda.")

    elif choice == "3":
        intro()

    elif choice == "4":
        print("Enter 'S' to open inventory and check stats.\n")

    else:
        print("Invalid choice, please pick again.")



input("Press Enter to continue...")


#Introductory Paragraph
print("\nIn this game, you will be playing as a child who fell into the Great Hollow...")
print("Your overall goal is to escape back to the surface, but beware of the monsters..")
print("Your decisions will impact the path you will take, think carefully.")
print("\n")

input()

#Flag 2
intro_choice = True

while intro_choice:
    name = input("What is your name? ")

#Name Address 1
    print("\n")
    name_choice = input(f"Are you sure you want to be called {name}? This will be permanent. (yes/no): ").lower()

    if name_choice == "yes":
        print(f"Welcome to Hollowmyth, {name}.")
        intro_choice = False

    elif name_choice == "no":
        print("Pick again.")
    
    else:
        print("Invalid answer, try again.")

            
input("Press Enter to continue..")
print("???: Hey there! You okay?\n")
input()
print("???: Sounds good! Now let me tell you how it works here underground.")
input()



print("???: You have an attribute called LOVE, think of it as your LEVEL. You can gain more LOVE by gaining EXP.\n")
input()
print("???: To gain EXP, you can do tasks that monsters give you. Don't worry, they're friendly!\n")
input()
print("???: However, there is a way to gain EXP way faster...")
input()
gain_exp_sentence = ("by KILLING monsters..\n")
                    
for character in gain_exp_sentence:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.15)

input()
print("???: Underground, monsters can also fuse with humans soul temporarily! It allows the monster to guide and help you throughout your journey.")
input()
print("???: Oh yeah! Don't forget you can check stats and inventory by entering 'S', you can also delete items to free up space!\n")
input()


#Flag 3
first_choice = True

while first_choice:

    choice1 = input('''Type in a letter to pick your choice.
    A. Who are you...?
    B. [SPARE]
    C. Where should I go next?
    S. Check stats 'S'
    Answer: ''').upper()


    if choice1 == "A":
        print(f"[CLOVER]: I forgot to introduce myself! Hello {name}! My name is Clover, I am one of the monsters underground.")
        input()

        while True:
            clover_choice = input("[CLOVER]: Let me fuse with your soul so I can guide you!(yes/no): ").lower()

            if clover_choice == "yes":
                soul_fuse = ("Clover turns into essence and goes in your chest...You feel a slight hint of power and can hear Clover now.\n")               
                for character in soul_fuse:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(0.08)
                    
                break
            
            elif clover_choice == 'no':
                print("....\n")
                input()
                print("[CLOVER]: Don't deny me...")
                input()
                soul_fuse1 = ("Clover jumps out and attacks you, leaving you stunned. He fuses into your soul. (-5 HP)\n")

                for character in soul_fuse1:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(0.08)
                    
                hp -= 5
                show_stats()
    
                break
            
            else:
                print("[CLOVER]: I need an answer. Yes or No?")

        break

    elif choice1 == "B":
        print("*You run away...leaving Clover stunned.")
        input()
        print("[CLOVER]: H-hey! Wait up! Don't leave me here alone!")
        input()
        print("*Clover runs after you and fuses into your soul, he seems happy but also a bit hurt that you tried to leave him.\n")
        karma += 3
        break
        
    elif choice1 == "C":
        print("[CLOVER]: You should head into the forbidden castle...let me fuse into you so I can guide you.")
        break

    elif choice1 == "S":
        show_stats()
        
    else:
        print("Invalid choice, try again.")

input("Press Enter to continue...")
print("You start walking towards the darkness with Clover's voice in your head, guiding you through the path ahead...\n")        
input()
print("As you walk through the path, you see a sign that says 'Forbidden Castle'..")
input()
print("You walk in the castle, it's dark and eerie, you can hear faint sounds of meows and moles digging..")
input()

while True:
    choice2 = input("You notice a dark corner in the castle, you can hear a faint sound of meows. Do you want to check it out?(yes/no): ").lower()

    if choice2 == "yes":
        print("You walk towards the corner and find a small kitty monster, it looks friendly.")
        input() 
        print("It suddenly launches itself at you!")
        input()
        fight_function(kitty)
        break
    elif choice2 == "no":
        print("You ignore the corner and keep walking, but you can't help but feel like you're missing out on something...")
        input()
        break
    else:
        print("Invalid choice, try again.")

print("After walking for a while, you finally see a huge purple gate in the distance..")
input()
print("[CLOVER]: That's the gate to the next area, but it's locked. I think there's a key somewhere in this castle that can open it.")
input()
print("You start searching the castle for the key, but you can't find it anywhere...")
input()
print("You decide to check the basement, you go down the stairs and find a chest in the corner!")
input()
while True:
    chest_choice = input("Do you want to open the chest? (yes/no): ").lower()

    if chest_choice == "yes":
        find_random_chest()
        break
    elif chest_choice == "no":
        print("You ignore the chest and keep searching, but you can't help but feel like you're missing out on something...")
        input()
        break
    else:
        print("Invalid choice, try again.")

print("After searching for a while, you finally find the key hidden in a drawer in the basement.")
input()
print("You use the key to open the gate, but as you open it, a mole monster jumps out!")
input()

while True:
    mole_choice = input("He offers you a donut if you can defeat him in a fight, do you accept?: ").lower()
    if mole_choice == "yes":
        fight_function(mole)
        add_food(donut)
        break
    elif mole_choice == "no":
        print("You decline the offer and try to run away, but the mole monster blocks your path.")
        input()
        print("He attacks you with his claws!")
        input()
        while True:            
            run_choice = input("Do you want to fight back or keep trying to run? (fight/run): ").lower()
            if run_choice == "fight":
                fight_function(mole)
                break
            elif run_choice == "run":
                print("You got away but with a few scratches... (-5 HP)")
                input()
                hp -= 5
                break
            else:
                print("Invalid choice, try again.")
        break
    else:
        print("Invalid choice, try again.")

print(f"[CLOVER]: Phew, that was close! Im glad you're safe, {name}.")
input()
print("[CLOVER]: From the mole monster, you got a donut that can heal you! Don't forget to eat it when you're low on HP!")
input()
print("You continue walking through the gate, with Clover guiding you through the next area...")
input()

print(f"[CLOVER]: Look! There's a table behind the gate, lets check it out!")
input()
print("You walk towards the table, spotting a pie and a chest..")
input()
while True:
    table_choice = input("Do you want to take the items? (yes/no): ").lower()

    if table_choice == "yes":
        find_random_chest()
        add_food(pie)
        break
    elif table_choice == "no":
        print("You ignore it and decide to keep walking.")
        input()
        break
    else:
        print("Invalid choice, try again.")

obscurus_dialogue = "???: ..."
for character in obscurus_dialogue:
    sys.stdout.write(character) 
    sys.stdout.flush() 
    time.sleep(0.2)


#BOSS ENCOUNTER 1
#Flag 4
obscurus_scene = True

while obscurus_scene:
    obscurus_choice = input('''Type in a letter to pick your choice.
    A. Who are you?
    B. [FIGHT]
    C. [SPARE]
    D. Ignore and keep walking
    S. Check stats 'S'
    Answer: ''').upper()

    if obscurus_choice == "A":
        print("Obscurus: I am the guardian of this place. I watch over the creatures and protect the balance.")
        input()
        print("Obscurus: You have entered my domain, but I sense something different about you. You have a strong evil presence in you...")
        input()
        while True:
            obscurus_choice2 = input('''Type in a letter to pick your choice.
                    A. What's your name?
                    B. Why are monsters underground?
                    Answer: ''').upper()
            if obscurus_choice2 == "A":
                print("Obscurus: I am Obscurus, the guardian of the Abandoned Castle.")
                input()
                print("Obscurus: I have been here for centuries, watching over the monsters and the balance of this place.")
                input()
                print("Obscurus: I also have the ability to sense the souls and know their past, including their names.")
                input()
                print(f"Obscurus: I know your name is {name}, and I can see the darkness in your soul. You have a long journey ahead of you.")
                input()
                print("Obscurus: Take good care of your soul kid...corruption can take over anytime.")
                while True:
                    corruption_choice = input('''Type in a letter to pick your choice.
                        A. What do you mean by corruption?
                        B. I'll be careful, thank you for the advice.
                        Answer: ''').upper()
                    if corruption_choice == "A":
                        print("Obscurus: Heh. Don't worry about it too much right now, you'll understand as you go along.")
                        karma += 5
                        input()
                        obscurus_scene = False # End the whole scene
                        break
                    elif corruption_choice == "B":
                        print("Obscurus: Good, I'm glad you understand. Take care of your soul, and it will take care of you.")
                        karma += 5
                        input()
                        obscurus_scene = False # End the whole scene
                        break
                break # Break out of choice2

            elif obscurus_choice2 == "B":
                print("Obscurus: Long ago, there was a war between humans and monsters. The humans won and sealed the monsters underground to protect themselves.")
                input()
                print("Obscurus: Many think it is the monsters fault for the war, but in reality, it was the humans who started it by invading the monster's home and taking their resources.")
                input()
                print("Obscurus: The real truth needs to be revealed, but sadly we all are stuck here.")
                obscurus_choice3 = input('''Type in a letter to pick your choice.
                    A. Don't worry! I will spread the news when I get back to the surface!
                    B. Heh, I don't care about the truth, I just want to get out of here.
                    Answer: ''').upper()
                if obscurus_choice3 == "A":
                    print("Obscurus: Thank you for your kindness, kid. I hope you can make a difference.")
                    input()
                    print("Obscurus: I will be watching you, and I hope you can find a way to free us all from this place. Goodbye.")
                    input()
                    karma += 5
                    obscurus_scene = False
                    break
                elif obscurus_choice3 == "B":
                    print("Obscurus: I see... You are not interested in helping others.")
                    input()
                    print("Obscurus: I hope you can find some compassion in your heart as you continue your journey. Goodbye.")
                    input()
                    obscurus_scene = False
                    break
                else:
                    print("Obscurus: Don't give me that nonsense...")
                    input()
                    print("Obscurus walks away, leaving you stunned...maybe next time follow instructions?")
                    input()
                    obscurus_scene = False
                    break
            else:
                print("Invalid choice, try again.")

    elif obscurus_choice == "B":
        print("Obscurus: You are not ready for this fight.")
        input()
        print(f"[CLOVER]: Hey {name}! I really suggest you to not fight him, unless you have a strong weapon.")
        input()
        while True:
            clover_stats_choice = input("Do you want to check your stats? (yes/no): ").lower()
            if clover_stats_choice == "yes":
                show_stats()
            elif clover_stats_choice == "no":
                break
            else:
                print("Invalid choice, try again.")
        print("Obscurus: I'll give you one last chance to leave, but if you choose to fight me, I won't hold back.")
        input()
        while True:
            fight_obscurus_choice = input("Do you want to leave or fight? (leave/fight): ").lower()
            if fight_obscurus_choice == "leave":
                print("Obscurus: Wise choice, now scram.")
                input()
                print("You walk away, Obscurus lets you go this time.")
                input()
                print(f"[CLOVER]: That guy really was scary! I'm glad you're safe, {name}.")
                obscurus_scene = False # End the whole scene
                break
            elif fight_obscurus_choice == "fight":
                fight_function(obscurus)            
                print("Obscurus: Others stronger than me will come, so be prepared for the challenges ahead.")
                input("Press Enter to continue...")
                obscurus_scene = False # End the whole scene
                break
            else:
                print("Invalid choice, try again.")

    elif obscurus_choice == "C":
        print("You decide to spare Obscurus, showing him mercy. He seems to not be fazed by your actions...")
        input()
        print("You decide to walk past him, sensing the feeling of being watched as you do so...")
        input()
        print(f"[CLOVER]: Good choice!")
        karma += 2
        obscurus_scene = False 
    elif obscurus_choice == "D":
        print("You ignore Obscurus and continue walking, but you feel a strange presence watching you.")
        karma += 1
        input()
        obscurus_scene = False 
    elif obscurus_choice == "S":
        show_stats()
        
    else:
        print("Invalid choice, try again.")

print("You continue walking through the castle, with Clover guiding you through the next area...")
input()

print(f"[CLOVER]: {name}, look over there! A monster cafeteria. It looks like they left in a hurry.")
input()

kitchen_choice = input("Do you want to scavenge the kitchen? (yes/no): ").lower()
if kitchen_choice == "yes":
    print("You find a sizzling grill and a cold fridge!")
    add_food(soul_burger)
    add_food(soda)
    print("[CLOVER]: Whoa, a Soul Burger? That's high-quality stuff. Save that for a big fight.")
    # No further endings. All branches handled above.
    print("You decide to keep moving. Your stomach growls.")

input("\n* You walk further into the heart of the castle. The walls turn from stone to iron. *")

print(f"[CLOVER]: Wait, {name}... check that golden pedestal. It's glowing.")
pedestal_choice = input("Investigate the pedestal? (yes/no): ").lower()
if pedestal_choice == "yes":
    print("It's a Golden Apple! It radiates pure healing energy.")
    add_food(golden_apple)
    print("\n* You also see two chests tucked behind the pedestal! *")
    find_random_chest()
    find_random_chest()
else:
    print("You ignore the glow. The shadows seem to get darker.")

input("\n* The air grows heavy. A massive obsidian door stands before you. *")


print(f"[CLOVER]: {name}... stop. Right there.")
time.sleep(1)
print("[CLOVER]: Behind this door is Rău. He isn't like the others.")
print("[CLOVER]: He won't care about your 'kindness.' He won't care about your 'mercy.'")
input()
print("[CLOVER]: If we don't strike first, he'll crush us. I can feel his power... it's intoxicating.")
print(f"[CLOVER]: Promise me, {name}... when the time comes, you'll do what's necessary. KILL him.")
input()

print("* You push open the heavy iron doors. The room is a massive arena filled with blue fire. *")
time.sleep(1)
 


#BOSS ENCOUNTER 2 
print("Rău: So... the 'Chosen One' finally arrives, guided by a parasite.")
input()
print(f"Rău: Do you even know who is inside your head, {name}?")
input()
print("Rău: Clover was never a 'guide.' He was a mistake. A soul that refused to fade.")
input()
print("Rău: And now he uses your skin to walk the earth again. How pathetic.")
input()

print("Rău: Look at you. Dragging around a bag of toys and snacks like a child on a field trip.")
print(f"Rău: Do you really think a {inv[0] if inv else 'stick'} and some crumbs can stop a Guardian?")
input()

print(f"[CLOVER]: SHUT UP! Don't listen to him, {name}! He's trying to get inside your head!")
print("[CLOVER]: Rip those red eyes out of his skull!")
input()

print(f"Rău: You have a choice, {name}.")
input()
print("Rău: You can cast out the voice in your head and face me with honor...")
input()
print("Rău: Or you can let the corruption take you, and become just another monster in the dark.")
input()
print("Rău: But know this... if you choose to fight for Clover, you are fighting for a lie.")
input()

print(f"[CLOVER]: He's lying! He wants us weak! {name}, look at his armor...")
print("[CLOVER]: It's made of the souls of children like you! Don't let him talk! ATTACK!")
input()


while True:
    rau_final_choice = input(f'''How will you respond to Rău?
    A. [FIGHT] "Clover is right, you're in our way."
    B. [SPARE] "I don't want to fight you, Rău."
    C. [TALK] "What do you mean by 'a lie'?"
    Answer: ''').upper()

    if rau_final_choice == "A":
        print("Rău: Then you are already lost. So be it!")
        karma -= 5
        fight_function(rau)
        break
    elif rau_final_choice == "B":
        print("Rău: Mercy? In a place like this? You are either very brave... or very foolish.")
        print("[CLOVER]: NO! What are you doing?! KILL HIM!")
        fight_function(rau)
        break
    elif rau_final_choice == "C":
        print("Rău: Clover was a human once, just like you. But his greed for LOVE turned him into... that.")
        print("[CLOVER]: LIES! LIES! LIES!")
        time.sleep(1)
        print("* Clover pulses with a dark energy, forcing your hand toward your weapon! *")
        input()
        fight_function(rau)
        break
    else:
        print("Invalid choice.")


if rau.hp <= 0:
    print("\n* Rău falls to one knee, his obsidian armor shattering. *")
    print("Rău: ...Heh. The cycle... continues...")
    input()
    print(f"[CLOVER]: YES! DID YOU SEE THAT EXP?! We're legendary, {name}!")
    print("[CLOVER]: I can feel my power returning. We're almost ready for the King.")
else:
    # This triggers if the player successfully spared Rău (using the mercy chance)
    print("\n* Rău lowers his blade, looking at you with pity. *")
    print("Rău: You have a strong will, kid. Keep it. You'll need it when Clover finally shows his true face.")
    print("[CLOVER]: ...Whatever. He's gone. Let's just go.")
    karma += 10

input("\n* You walk past the smoldering arena and head toward the Throne Room... *")


print("\nThe purple gates of the castle groan as they close behind you. You are now in the Long Hall.")
print("Golden sunlight filters through stained glass, but it feels cold.")
input()

print(f"[CLOVER]: This is it, {name}. The King is just at the end of this hall.")
print("[CLOVER]: But look... the guards left their posts. They left everything behind.")
input()


print(f"To your left, a heavy iron door is slightly ajar. It's the Royal Armory.")
armory_choice = input("Do you want to search the armory for supplies? (yes/no): ").lower()

if armory_choice == "yes":
    print("You find a massive crate labeled 'EMERGENCY RATIONS'.")
    add_food(soul_burger)
    add_food(soda)
    print("You also see a weapon rack that looks promising.")
    find_random_chest()
    input()
    print("[CLOVER]: Nice. That Soul Burger looks like it could heal a giant.")
else:
    print("You ignore the armory. You feel like you have enough... for now.")

input()


print("You continue walking. You pass a beautiful indoor garden filled with glowing flowers.")
print("In the center of the garden, a golden tree stands tall. Only one fruit remains.")
garden_choice = input("Do you want to pick the Golden Apple? (yes/no): ").lower()

if garden_choice == "yes":
    print(f"You carefully pick the Golden Apple. It feels warm in your hand.")
    add_food(golden_apple)
    print(f"As you pull the apple, the ground shifts, revealing a hidden chest!")
    find_random_chest()
    input()
    print(f"[CLOVER]: A Golden Apple! {name}, that's literally the best healing item in the world.")
else:
    print(f"You leave the garden untouched. The flowers seem to wilt as you walk away.")

input()


print(f"Before the final doors, you see a small library. A chest sits on the main desk.")
library_choice = input("Do you want to check the library for one last treasure? (yes/no): ").lower()

if library_choice == "yes":
    print(f"You open the chest on the desk. It's filled with snacks and gear!")
    add_food(pie)
    add_food(donut)
    find_random_chest()
    input()
    print(f"[CLOVER]: Look at us. We're practically an army by ourselves now.")
else:
    print(f"You stay focused on the golden doors ahead.")

input()

print("* Your inventory is full. Your stats are high. The golden doors are right in front of you. *")
print(f"[CLOVER]: This is it, {name}. Don't let him talk his way out of this.")
input("Press Enter to enter the Throne Room...")


print(f"The golden doors swing open with a heavy thud. The room is vast and filled with light.")
print(f"King Garamond stands at the far end, looking out a massive window at the barrier.")
input()

print(f"Garamond: It is a strange thing, isn't it? To spend your whole life looking at a wall.")
print(f"Garamond: You start to memorize every crack. Every shadow. You start to think the wall is the world.")
input()

print(f"Garamond: But then... a child falls. A new soul arrives. And the wall doesn't seem so permanent anymore.")
print(f"Garamond: Turn around, {name}. Let me look at the one who has caused so much noise in my halls.")
input()

print(f"* King Garamond turns. He is massive, wearing heavy golden armor and a tattered purple cape. *")
print(f"Garamond: And I see you have brought Clover with you. Or rather... Clover has brought you.")
input()



garamond_choice = input(f"How do you want to respond to the King, {name}?
                        A. 'I just want to go home. Why must it be like this?'
                        B. [FIGHT] 'Enough talking. Let's finish this.''
                        C. 'What do you mean by Clover bringing me?'
                        Answer: ").upper()

if garamond_choice == "A":
    print("Garamond: Home. A simple wish. One that every monster in this hollow shares with you.")
    print("Garamond: But for you to go home, we must stay here forever. And for us to leave, you must stay.")
    input()
    print("Garamond: Do you believe one life is worth more than an entire kingdom's freedom?")
    

    sub_choice_a = input("Do you think your life is more important? (yes/no): ").lower()
    if sub_choice_a == "yes":
        print("Garamond: Honesty. A rare trait in these woods. But a selfish one.")
        print(f"Garamond: You have the spark of a conqueror, {name}. Just like the humans who put us here.")
        karma -= 5
    else:
        print("Garamond: Then you understand my pain. I do not want to take your soul, child.")
        print("Garamond: But I am a King first, and a person second. I must do what is best for my people.")
        karma += 5

elif garamond_choice == "B":
    print("Garamond: So much fire in such a small frame. Clover has trained you well, it seems.")
    print("Garamond: You remind me of another human who fell long ago. They didn't want to talk either.")
    input()
    print(f"Garamond: They only wanted to see the world burn. Is that your goal too, {name}?")
    

    sub_choice_b = input("Are you here to destroy the monsters? (yes/no): ").lower()
    if sub_choice_b == "yes":
        print("Garamond: Then I shall be the shield that stops you. I will not let my people suffer again!")
        karma -= 10
    else:
        print("Garamond: Then why hold your weapon so tightly? Your actions and your words are at war.")
        karma -= 2

elif choice_1 == "C":
    print("Garamond: Ah, so the 'guide' hasn't been entirely truthful with you. I am not surprised.")
    print("Garamond: Clover wasn't born a monster. He was a human who fell, just like you.")
    input()
    print("Garamond: But he didn't want to escape. He wanted power. He stayed to harvest the souls of the weak.")
    print("Garamond: Clover: [HE'S LYING! HE'S TRYING TO TURN YOU AGAINST ME!]")
    input()
    

    sub_choice_c = input("Who do you trust more right now? (clover/king): ").lower()
    if sub_choice_c == "clover":
        print("Garamond: Blind trust is the quickest way to a shallow grave. But I admire your loyalty.")
        karma -= 3
    else:
        print("Clover: [How could you?! After I guided you?! After I SAVED you?!]")
        print("* You feel a burning sensation in your chest. Clover is furious. *")
        hp -= 5
        karma += 7

else:
    print("Garamond: Your silence speaks volumes. But silence will not save you now.")


print(f"\nGaramond: Whether you believe me or not, {name}, the result remains the same.")
print(f"Garamond: I have a duty to my people. I have a duty to the monsters who have lived in fear for so long.")
input()

print(f"Garamond: Look at the barrier behind me. It requires one more human soul to shatter.")
print(f"Garamond: If I take yours, we all go free. If you take mine... you go free, but we remain in the dark.")
input()

print(f"[CLOVER]: He's making it sound like he's a martyr! He's a murderer, {name}!")
print(f"[CLOVER]: Don't let him guilt-trip you! One strike is all it takes. Think of the LOVE we'll gain!")
input()

print(f"Garamond: Clover... you were always so hungry for 'LOVE'. You never understood that real power comes from sacrifice.")
print(f"Garamond: {name}, prepare yourself. I will not hold back. For my kingdom!")
input()

# Final Choice before the fight
while True:
    final_stance = input(f'''The room glows with a blinding light. What is your final stance?
    A. [FIGHT] "I'm sorry, but I have to get home."
    B. [SPARE] "There has to be another way!"
    C. [THREATEN] "I'll kill you and everyone else in this castle!"
    Answer: ''').upper()

    if final_stance == "A":
        print(f"Garamond: Then let us see if your resolve is stronger than my crown!")
        karma -= 2
        break
    elif final_stance == "B":
        print(f"Garamond: Your mercy is a heavy burden to carry, child. But I cannot accept it!")
        karma += 10
        break
    elif final_stance == "C":
        print(f"Garamond: ...Then you truly are the monster here. I will stop you or die trying!")
        karma -= 20
        break
    else:
        print("Garamond: The time for indecision is over!")

#FINAL BOSS ENCOUNTER
print("\n* KING GARAMOND CHALLENGES YOU TO A FINAL BATTLE! *")
fight_function(garamond)


if garamond.hp <= 0:
    print("\n* King Garamond falls to the floor, his trident clattering beside him. *")
    print("Garamond: ...So... the sun... will finally shine... on a new world...")
    input()
    print(f"Garamond: Use my soul... break the seal... leave this place, {name}...")
    input()
    print("* King Garamond fades away into dust. *")
    print("[CLOVER]: WE DID IT! WE ACTUALLY DID IT!")
    print("[CLOVER]: Look at that LOVE! We're the strongest things in this world now!")
    input()
else:
    #HAPPENS at a very slight chance, only if the spare option works during fight
    print("\n* King Garamond lowers his trident, exhausted and weeping. *")
    print("Garamond: You... you would truly stay here? You would give up your freedom for us?")
    input()
    print("Garamond: I cannot take your soul. Not after seeing such kindness.")
    print(f"Garamond: Go, {name}. Take the secret path behind the throne. Escape before the guards arrive.")
    input()
    print("[CLOVER]: Are you serious?! We're just... leaving?!")
    print("[CLOVER]: Ugh... fine. But don't expect me to be happy about this.")
    karma += 15

print("\nYou walk toward the barrier. The light is blinding. Your journey has reached its end.")
input("Press Enter to see your destiny...")


#Final Ending Branches
print("You take a step toward the barrier, but suddenly, your heart stops.")
input()
print("A cold, paralyzing pain shoots through your chest. You fall to your knees.")
input()

print(f"[CLOVER]: ...Going somewhere, {name}?")
input()

print("A dark, oily mist begins to pour out of your mouth and eyes.")
print("The mist hardens and forms a shape in front of you. It looks like a shadow of yourself.")
input()

print("Clover: Ah... it feels good to have my own legs again.")
print(f"Clover: You were a decent vessel, I'll give you that. You gathered all those items... all that EXP, {name}.")
input()

if karma <= -30:
    print("Clover: Look at us. The King is dead. The monsters are cowering.")
    print("Clover: We have reached the peak of LOVE. I can feel our souls humming in perfect sync.")
    input()
    print("Clover: You didn't hesitate. You didn't flinch. You are exactly what I needed.")
    print("Clover: There's no need for us to fight. The barrier is weak, and we are strong.")
    input()
    print(f"Clover: Let's go to the surface, {name}. Together, we'll show the humans what real monsters look like.")
    print("Clover: Are you ready to finish what we started?")
    input()
    print("The two of you walk through the barrier together. The world outside will never be the same.")
    input("Press enter to reveal your ending...")
    print("ENDING: GENOCIDE - THE DREAD PARTNERS")

elif karma > -30 and karma < 30:
    print(f"Clover: We've come a long way, {name}. But you've been... inconsistent.")
    print("Clover: Sometimes you're a killer, sometimes you're a mistake. It's confusing.")
    input()
    print("Clover: I'm going to give you one chance to decide who you really are.")
    print("Clover: Join me. We'll take this power, hit the surface, and take whatever we want.")
    print("Clover: Or... stay in my way, and I'll erase you right here.")
    input()

    while True:
        neutral_final = input("What is your choice? (join/refuse): ").lower()
        if neutral_final == "join":
            print("Clover: Heh. I knew you had it in you. Let's go, partner.")
            print("The two of you step into the light together.")
            input("Press enter to reveal your ending...")
            print("ENDING: NEUTRAL - THE CORRUPTED")
            break
        elif neutral_final == "refuse":
            print("Clover: ...I figured you'd say that. You always were a disappointment.")
            print("Clover: DIE!")
            input()
            fight_function(clover)
            print("Clover dissipates into dark smoke. You stand alone before the barrier, collapsing to your knees.")
            input("Press enter to reveal your ending...")
            print("ENDING: NEUTRAL - THE LONELY ESCAPE")
            break
        else:
            print("Clover: Choose! My patience is wearing thin!")

elif karma >= 30:
    print(f"Clover: Why...? Why do you keep looking at me like that, {name}?")
    print("Clover: I tried to kill the King! I tried to take your soul! I'm a parasite!")
    input()
    print("Clover: Stop being so... NICE! It burns! It hurts more than any weapon!")
    print("Clover: I don't deserve your mercy. I've done terrible things. I've lived for hatred!")
    input()

    while True:
        pacifist_choice = input("Do you spare Clover and offer him forgiveness? (spare/fight): ").lower()
        if pacifist_choice == "spare":
            print("You reach out and hug the dark mist that is Clover.")
            print("Clover: ...What are you doing? Let go... stop it...")
            input()
            print("Clover: ...I'm sorry. I forgot what it was like to be human.")
            print("Clover: I forgot that I didn't have to be a monster just because I was hurt.")
            input()
            print(f"Clover: Go, {name}. Use the power of your soul to free everyone.")
            print("Clover: I will stay here and try to fix what I broke. Thank you for not giving up on me.")
            input()
            print("You shatter the barrier with the power of kindness. All monsters return to the surface.")
            input("Press enter to reveal your ending...")
            print("ENDING: TRUE PACIFIST - THE REDEEMED SOUL")
            break
        elif pacifist_choice == "fight":
            print("Clover: That's better. Let's finish this the way it was meant to end!")
            fight_function(clover)
            print("ENDING: PACIFIST - THE TRAGIC HERO")
            break
        else:
            print("Clover looks confused. Choose to spare or fight.")

print(f"\nTHANK YOU FOR PLAYING HOLLOWMYTH, {name.upper()}!")
input()
print("Play again to see different endings and discover all the secrets hidden in the castle...")

