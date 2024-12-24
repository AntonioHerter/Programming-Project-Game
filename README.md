- Overview
Welcome to the Jumpy Goat game! This is a simple 2D platformer built using Python and the Pygame library. In this game, you control a goat that can jump, collect keys, and avoid obstacles like spikes. The goal is to collect all the keys to win the game.

- Getting Started
Prerequisites
To run this game, you need to have Python and Pygame installed on your computer. You can download Python from python.org and install Pygame using pip install pygame

- Running the Game
Clone or download the repository containing the game code.
Navigate to the directory where the code is located.
Run the game using the following command: main.py

- Game Controls
Left Arrow Key: Move the goat to the left.
Right Arrow Key: Move the goat to the right.
Space Bar: Make the goat jump.

- Code Structure
--Main Components
Player Class: Controls the player's actions, including movement, jumping, and collision detection.
Object Classes: Represents various objects in the game, such as blocks, spikes, and collectibles (keys, cups, etc.).
Game Functions: Includes functions for drawing the game elements, handling collisions, and managing the game loop.
  -Key Functions
main(window): The main function that initializes the game and runs the game loop.
draw(window, background, bg_image, player, objects, scroll_offset): Draws all game elements on the screen.
handle_move(player, objects): Handles player movement and interactions with objects.
Sprite Loading
The game uses sprite sheets for character animations and object graphics. The load_sprite_sheets function loads these sprites from the specified directories.

- References
Pygame Documentation (https://www.pygame.org/docs/)
Python Documentation (https://docs.python.org/3/)
Sprite Animation in Pygame (https://realpython.com/pygame-a-primer/) 

- Tag designer creator(s):
--Character:
The palette used is The Perfect Palette 2.0 Palette
Using Dino Characters by @ScissorMarks as a template
Author	ChaosWitchNikol
Tags	16-bit, Animals, Animation, Characters, Colorful, Pixel Art, Retro, spri
Asset license	Creative Commons Attribution v4.0 International

--Tile set:
Jesse M / Twitter - @Jsf23Art

--Objects:
Copyright/Attribution Notice: 
Recycle items art by Clint Bellanger

--Keys:
Author: 
BizmasterStudios
Thursday, August 31, 2017 - 23:23

--Song: "Mario Type beat" by RCCrawlersfourlife

Feel free to add any additional references or resources. 

-Instructions for Resolving Path Issues
If you encounter issues related to file paths during the download process, there is an alternative solution to ensure everything works smoothly.
Create a New Folder: Start by creating a new folder with your desired name. This will serve as the main directory for your project.
Transfer Files: Move all the downloaded files into this newly created folder.
Update the Code: At the end of this document, you will find a code snippet. Copy and paste this code into your main Python file.
Modify the Folder Name: In the main Python file, locate the placeholder "GAME PROJECT" and replace it with the name of your newly created folder.
By following these steps, you will correctly adjust the file paths, allowing the project to run without any issues.

Conclusion
Thank you for checking out the Jumpy Goat game! I hope you enjoy playing it as much as I enjoyed creating it. If you have any questions or suggestions, feel free to reach out!






Solving problem code:
# Import necessary libraries -  Remember to check if any of then were forgotten
import pygame # Main game library for creating the game
import os # For file path operations
from os import listdir # To list all files in a directory
from os.path import isfile, join # To work with file paths and check file

# Start Pygame
pygame.init()
pygame.font.init()

# Set up the game window
pygame.display.set_caption("Jumpy goat")
WIDTH, HEIGHT = 1000, 800 
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Game constants for smooth gameplay
FPS = 60  # Frames per second, controls the speed of the game loop
player_vel = 7  # Speed of the player’s movement

#   Function to flip sprites horizontally 
def flip(sprites):
    """
    Flips a list of sprites horizontally for left movement.
    Args:
        sprites (list): List of Pygame surface objects (frames).
    Returns:
        list: Flipped sprites.
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # Flips each frame horizontally

#                   Function to load sprite sheets
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Loads sprites from sprite sheets, organizes them by action and direction.
    Args:
        dir1 (str): Main folder name.
        dir2 (str): Subfolder name.
        width (int): Width of each sprite frame.
        height (int): Height of each sprite frame.
        direction (bool): Whether to load directional sprites.
    Returns:
        dict: Dictionary of sprite animations.
    """
    path = join("GAME PROJECT","assets", dir1, dir2) # Builds the path to the folder containing the sprite sheets
    images = [f for f in listdir(path) if isfile(join(path, f))] # Lists all files in the folder

    all_sprites = {} # Dictionary to hold all loaded sprites

    for image in images:  # Loops through each sprite sheet
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() # Loads the sprite sheet with transparency

        sprites = [] # List to store individual frames
        for i in range(sprite_sheet.get_width() // width): # Loops through each frame in the sprite sheet
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32) # Creates a blank surface for a frame
            rect = pygame.Rect(i * width, 0, width, height) # Defines the area of the current frame
            surface.blit(sprite_sheet, (0, 0), rect) # Copies the frame from the sprite sheet to the surface
            sprites.append(pygame.transform.scale2x(surface)) # Doubles the size of the frame and adds to the list

        if direction: # If the sprites have directional movement
            all_sprites[image.replace(".png", "") + "_right"] = sprites  # Store right-facing sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites) # Store flipped (left-facing) sprites
        else:
            all_sprites[image.replace(".png", "")] = sprites # Store non-directional sprites

    return all_sprites  # Return all loaded sprites as a dictionary

#         Function to get block images 
def get_block(size):
    """
    Loads a block image from the terrain sprite sheet.
    Args:
        size (int): Size of the block.
    Returns:
        pygame.Surface: Scaled block surface.
    """
    path = join("GAME PROJECT", "assets", "Terrain", "jungle tileset.png") # Path to the terrain image
    image = pygame.image.load(path).convert_alpha() # Loads the terrain sprite sheet with transparency
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32) # Creates a blank surface for the block
    rect = pygame.Rect(76, 33, size, size) # Defines the rectangle of the block to extract
    surface.blit(image, (0, 0), rect) # Copies the block from the sprite sheet to the surface
    return pygame.transform.scale2x(surface)  # Doubles the block's size and returns it

# Class to control the Player
class Player(pygame.sprite.Sprite):
    player_color = (255, 0, 0)
    GRAVITY = 1.8 # Gravity constant to pull the player down
    SPRITES = load_sprite_sheets("MainCharac", "WhiteG", 72, 72, True) # Load player sprites
    animation_frame_delay = 2 # How quickly the animations change frames

    def __init__(self, x, y, width, height):
        """
        Initializes the player.
        Args:
            x (int): Initial x-position.
            y (int): Initial y-position.
            width (int): Width of the player.
            height (int): Height of the player.
        """
        super().__init__() # Call the parent class initializer
        self.rect = pygame.Rect(x, y, width, height) # Create a rectangle for the player
        self.x_vel = 0 # Initial horizontal velocity
        self.y_vel = 0 # Initial vertical velocity
        self.mask = None 
        self.direction = "left" # Default direction
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.last_hit_time = 0  # Track the last hit time
        self.initial_position = (x, y)  # Store the initial position
        self.hit_animation_duration = 30  # Duration of hit animation frames
        self.hit_animation_count = 0  # Counter for hit animation frames
        self.points = 0  # Initialize points to 0
        self.collected_key_set = set()  # Set to track collected keys

    def jump(self): #Makes the player jump
        self.y_vel = -self.GRAVITY * 7
        self.animation_count = 0 # Reset animation count for jump
        self.jump_count += 1
        if self.jump_count == 1: # Reset animation count for jump
            self.fall_count = 0

    def move(self, dx, dy):
        """
        Moves the player by a given amount.
        Args:
            dx (int): Change in x-position.
            dy (int): Change in y-position.
        """
        self.rect.x += dx # Update x-position
        self.rect.y += dy # Update y-position

    def points_count(self, key_name):
        if key_name not in self.collected_key_set:  # Check if the key has not been collected
            self.collected_key_set.add(key_name)  # Add the key to the collected set
            self.points += 1  # Increment points
            print(f"Keys collected: {self.points}")  # Print the current points (for debugging)

    def make_hit(self, current_time):
        if current_time - self.last_hit_time >= 500:  # 0.5 seconds interval
            self.hit = True
            self.hit_count += 1
            self.last_hit_time = current_time  # Update last hit time 

    def reset_position(self):
        self.rect.topleft = self.initial_position  # Reset to initial position
        self.y_vel = 0  # Reset vertical velocity
        self.hit_count = 0  # Reset hit count
        self.hit = False  # Reset hit state
        self.points = 0  # Reset points
        self.collected_key_set = set()  # Reset collected keys
        return self.initial_position[0]  # Return the x position for resetting the view

    def move_left(self, vel): # Moves the player left. Args: vel (int): Speed of movement.
        self.x_vel = -vel # Set negative velocity for left movement
        if self.direction != "left": # Update direction
            self.direction = "left"
            self.animation_count = 0 
    def move_right(self, vel): #Moves the player right. Args: vel (int): Speed of movement.
        self.x_vel = vel # Set positive velocity for right movement
        if self.direction != "right": # Update direction
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps): # Update the vertical velocity (y_vel) based on gravity and fall count.
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) # The fall speed increases gradually, capped at a maximum of 1.
        self.move(self.x_vel, self.y_vel) # Move the player by the current horizontal (x_vel) and vertical (y_vel) velocities.

        if self.hit: # Check if the player is currently in a hit state (e.g., has been damaged).
            self.hit_animation_count += 1 # Increment the hit animation counter to track how long the player has been hit.
            if self.hit_animation_count >= self.hit_animation_duration: # Check if the hit animation has reached its duration limit.
                self.hit = False  # Reset the hit state to false, indicating the player is no longer hit.
                self.hit_animation_count = 0  # Reset animation counter
        self.fall_count += 1 # Increment the fall count to track how long the player has been falling.
        self.update_sprite() # Update the player's sprite based on the current state (e.g., running, jumping, falling).

    def landed(self): # Resets jump and fall counters when the player lands.
        self.fall_count = 0 # Reset the fall count to 0, indicating that the player is no longer falling.
        self.y_vel = 0 # Set the vertical velocity (y_vel) to 0, stopping any downward movement.
        self.jump_count = 0 # Reset the jump count to 0, indicating that the player is no longer in a jump state.

    def hit_head(self):
        self.count = 0 # Reset the count variable to 0. This could be used for tracking purposes, such as how many times the player has hit their head or for other game logic.
        self.y_vel *= -1 #Invert the vertical velocity (y_vel) to make the player bounce upwards. This simulates the effect of hitting a ceiling, causing the player to move in the opposite direction (upward).

    def update_sprite(self): #Updates the player's sprite based on the current direction and animation state.
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction # Construct the full sprite sheet name based on the current sprite sheet and direction.
        sprites = self.SPRITES[sprite_sheet_name] # Retrieve the list of sprites from the SPRITES dictionary using the constructed name.
        sprite_index = (self.animation_count // self.animation_frame_delay) % len(sprites) # Calculate the current sprite index based on the animation count and frame delay.
        self.sprite = sprites[sprite_index] # Update the current sprite to the one at the calculated index.
        self.animation_count += 1 # Increment the animation count to progress the animation.
        self.update() # Call the update method to refresh the player's rectangle and mask.

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Update the player's rectangle to match the current sprite's position.
        self.mask = pygame.mask.from_surface(self.sprite) # Create a mask from the current sprite for collision detection.

    def draw(self, win, scroll_offset): #Draws the player on the screen. Args: win (pygame.Surface): The game window.
        win.blit(self.sprite, (self.rect.x - scroll_offset, self.rect.y)) # Draw the player sprite


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None): # Initialize the object with its position, dimensions, and optional name.
        super().__init__() # Call the parent class (Sprite) constructor to initialize the sprite. 
        self.rect = pygame.Rect(x, y, width, height) # Create a rectangle (rect) to represent the object's position and size.
        self.image = pygame.Surface((width, height), pygame.SRCALPHA) # Create a surface (image) for the object with the specified width and height. The surface is created with an alpha channel (transparency) enabled.
        self.width = width # Store the width of the object for future reference.
        self.height = height  #Store the height of the object for future reference.
        self.name = name # Store the optional name of the object, which can be used for identification.

    def draw(self, win, scroll_offset):
        win.blit(self.image, (self.rect.x - scroll_offset, self.rect.y))
        # Draw the object on the given window (win) at its current position,
        # adjusting for any scrolling offset.
        
        # Blit (draw) the object's image onto the window at the position of the rectangle,
        # subtracting the scroll offset to account for camera movement.


class Block(Object):
    def __init__(self, x, y, block_size):
        super().__init__(x, y, block_size, block_size)
        block = get_block(block_size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Spike(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike")
        self.spike = load_sprite_sheets("Objects", "Spikes", width, height)
        self.image = self.spike["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Cup(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "cup")
        self.cup = load_sprite_sheets("Objects", "Cup", width, height)
        self.image = self.cup["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Mug(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "mug")
        self.mug = load_sprite_sheets("Objects", "Mug", width, height)
        self.image = self.mug["idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Metalcan(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "metalcan")
        self.metalcan = load_sprite_sheets("Objects", "Metalcan", width, height)
        self.image = self.metalcan["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
    
class Big_Plastic(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "bigplastic")
        self.bigplastic = load_sprite_sheets("Objects", "Big Plastic", width, height)
        self.image = self.bigplastic["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Pizza(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "pizza")
        self.pizza = load_sprite_sheets("Objects", "Pizza", width, height)
        self.image = self.pizza["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Key1(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "key1")
        self.key1 = load_sprite_sheets("Objects", "Keys", width, height)
        self.image = self.key1["Key1"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Key2(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "key2")
        self.key2 = load_sprite_sheets("Objects", "Keys", width, height)
        self.image = self.key2["Key2"][0]
        self.mask = pygame.mask.from_surface(self.image)

class Key3(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "key3")
        self.key3 = load_sprite_sheets("Objects", "Keys", width, height)
        self.image = self.key3["Key3"][0]
        self.mask = pygame.mask.from_surface(self.image)


# Function to draw the win screen
def draw_win_screen(window):
    font = pygame.font.Font(None, 74)  # Create a font object
    victory_message = font.render("YOU WON!", True, (10, 112, 21))  # Render the win text
    victory_text_rect = victory_message.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    window.blit(victory_message, victory_text_rect)  # Draw the text on the window
    pygame.display.update()  # Update the display
    pygame.time.delay(20000)  # Wait for 20 seconds

def get_background(name):
    """
    Loads and tiles the background image.
    Args:
        name (str): Background image file name.
    Returns:
        list: Positions of tiled background.
        pygame.Surface: Background image.
    """
    image = pygame.image.load(join("GAME PROJECT", "assets", "Background", name)) # Load background image
    _, _, width, height = image.get_rect() # Get dimensions of the image
    tiles = [] # List to store tile positions

    for i in range(WIDTH // width + 1): # Loop for horizontal tiling
        for j in range(HEIGHT // height + 1): # Loop for vertical tiling
            pos = (i * width, j * height) # Calculate position for each tile
            tiles.append(pos)  # Add position to the list

    return tiles, image  # Return positions and image

#Main drawing function 
def draw(window, background, bg_image, player, objects, scroll_offset):
    """
    Draws all game elements on the screen.
    Args:
        window (pygame.Surface): The game window.
        background (list): Tiled background positions.
        bg_image (pygame.Surface): Background image.
        player (Player): Player object.
        scroll_offset(int): Scrolling offset.
    """
    for tile in background: # Loop through all background tiles
        window.blit(bg_image, tile) # Draw each tile at its position

    for obj in objects:
        obj.draw(window, scroll_offset)

    player.draw(window, scroll_offset)  # Draw the player

    pygame.display.update()# Update the display


def handle_vertical_collision(player, objects, dy):
    collided_objects = [] # List to keep track of objects the player collides with. 
    for obj in objects: # Check if the player collides with the object using a pixel-perfect mask collision.
        if pygame.sprite.collide_mask(player, obj): 
            if dy > 0: # If the player is moving downwards. Position the player's bottom at the top of the object (land on it).
                player.rect.bottom = obj.rect.top
                player.landed() # Call the landed method to reset jump and fall states.
            elif dy < 0: # If the player is moving upwards. Position the player's top at the bottom of the object (hit their head).
                player.rect.top = obj.rect.bottom
                player.hit_head()  # Call the hit_head method to handle head collision. 

            collided_objects.append(obj) # Add the collided object to the list.

    return collided_objects # Return the list of collided objects.


def collide(player, objects, dx): # Handles horizontal collisions between the player and a list of objects. 
    player.move(dx, 0) # Move the player horizontally by dx.
    player.update() 
    collided_object = None # Initialize a variable to store the first collided object.
    object_index = None 
    for obj in range(len(objects)): # Iterate through each object in the list. Check if the player collides with the object using a pixel-perfect mask collision.
        if pygame.sprite.collide_mask(player, objects[obj]): 
            collided_object = objects[obj]  # Store the collided object.
            object_index = obj
            break # Exit the loop after the first collision is found.

    player.move(-dx, 0) # Move the player back to the original position.
    player.update() # Update the player's state after moving back.
    return [collided_object, object_index] # Return the first collided object, if any.


def handle_move(player, objects):
    keys = pygame.key.get_pressed() # Get the current state of all keyboard keys.
    new_objects_list = objects
    player.x_vel = 0 # Reset the player's horizontal velocity.
    # Check for collisions when moving left and right.
    collide_left, object_left_index = collide(player, objects, -player_vel * 6) # Check for left collisions.
    collide_right, object_right_index = collide(player, objects, player_vel * 6) # Check for right collisions.

    # Move the player left if the left key is pressed and there is no left collision.
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(player_vel)
    # Move the player right if the right key is pressed and there is no right collision.
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(player_vel)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel) # Handle vertical collisions based on the player's vertical velocity.
    to_check = [collide_left, collide_right, *vertical_collide] # Create a list of objects to check for interactions (collisions).

    # Check for interactions with specific objects (e.g., spikes, keys).
    for obj in to_check:
        if obj and obj.name == "spike":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "bigplastic":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "cup":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "metalcan":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "mug":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "pizza":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
            
    # Check for key collection and remove keys from the game.
    for obj in to_check:
        if obj and obj.name == "key1":
            if (object_right_index != None):
                new_objects_list.pop(object_right_index)
            if (object_left_index != None):
                new_objects_list.pop(object_left_index)
            player.points_count("key1")  # Pass the key name
            obj.kill()  # Remove the key from the game
        if obj and obj.name == "key2":
            if (object_right_index != None):
                new_objects_list.pop(object_right_index)
            if (object_left_index != None):
                new_objects_list.pop(object_left_index)
            player.points_count("key2")  # Pass the key name
            obj.kill()  # Remove the key from the game
        if obj and obj.name == "key3":
            if (object_right_index != None):
                new_objects_list.pop(object_right_index)
            if (object_left_index != None):
                new_objects_list.pop(object_left_index)
            player.points_count("key3")  # Pass the key name
            obj.kill()  # Remove the key from the game
    return new_objects_list


def main(window):
    game_clock= pygame.time.Clock()
    background_tiles, bg_image = get_background("green.png")

    pygame.mixer.music.load("GAME PROJECT/Sounds/Background.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1,0.0)


    block_size = 100

    player = Player(100, 100, 50, 50)
    spike = Spike(100, HEIGHT - block_size - 32, 16, 32) #Reference for inputing in the map
    bigplastic = Big_Plastic(100, HEIGHT - block_size - 115, 41, 59) #Reference for inputing in the map
    mug = Mug(100, HEIGHT - block_size - 55, 31, 31)  #Reference for inputing in the map
    cup = Cup(100, HEIGHT - block_size - 90, 30, 48) #Reference for inputing in the map
    metalcan= Metalcan(100, HEIGHT - block_size - 88, 22, 44) #Reference for inputing in the map
    pizza= Pizza(100, HEIGHT - block_size - 68.5,62,38) #Reference for inputing in the map
    key1= Key1(50, HEIGHT - block_size - 32, 32, 32)
    key2= Key2(100, HEIGHT - block_size - 32, 32, 32)
    key3= Key3(150, HEIGHT - block_size - 32, 32, 32)

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 29) // block_size)]
    objects = [*floor, Block(-800, HEIGHT - block_size * 2, block_size), Block(-800, HEIGHT - block_size * 3, block_size),
               Block(-800, HEIGHT - block_size * 4, block_size), Block(-800, HEIGHT - block_size * 5, block_size),
               Block(-800, HEIGHT - block_size * 6, block_size), Block(-800, HEIGHT - block_size * 7, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size),Block(block_size * 6, HEIGHT - block_size * 6, block_size),
               Block(block_size * 10, HEIGHT - block_size * 6, block_size),Block(block_size * 14, HEIGHT - block_size * 6, block_size),
               Block(block_size * 18, HEIGHT - block_size * 4, block_size), Block(block_size * 21, HEIGHT - block_size * 4, block_size),
               Block(block_size * 24, HEIGHT - block_size * 4, block_size),Block(block_size * 27, HEIGHT - block_size * 4, block_size),
               Big_Plastic(block_size * 19.5, HEIGHT - block_size - 115, 41, 59),Big_Plastic(block_size * 22.5, HEIGHT - block_size - 115, 41, 59), 
               Big_Plastic(block_size * 25.5, HEIGHT - block_size - 115, 41, 59), Mug(block_size * 24, HEIGHT - block_size*4 - 55, 31, 31),
               Block(block_size * 30, HEIGHT - block_size * 6, block_size), Block(block_size * 31, HEIGHT - block_size * 6, block_size),
               Block(block_size * 32, HEIGHT - block_size * 6, block_size), Spike(block_size*33, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*33.5, HEIGHT - block_size - 32, 16, 32),Spike(block_size*34, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*34.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size*35, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*35.5, HEIGHT - block_size - 32, 16, 32),Spike(block_size*36, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*36.5, HEIGHT - block_size - 32, 16, 32),Spike(block_size*37, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*37.5, HEIGHT - block_size - 32, 16, 32),Spike(block_size*38, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size*38.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size*39, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 44, HEIGHT - block_size * 4, block_size),Block(block_size * 45, HEIGHT - block_size * 5, block_size), 
               Block(block_size * 46, HEIGHT - block_size * 4, block_size),Spike(block_size * 46, HEIGHT - block_size * 4 -32, 16, 32),
               Spike(block_size * 46.5, HEIGHT - block_size * 4 -32, 16, 32), Big_Plastic(block_size * 45, HEIGHT - block_size - 115, 41, 59),
               Block(block_size * 48, HEIGHT - block_size * 6, block_size), Cup(block_size * 50, HEIGHT - block_size - 90, 30, 48),
               Spike(block_size * 51, HEIGHT - block_size - 32, 16, 32),Spike(block_size * 53, HEIGHT - block_size - 32, 16, 32),
               Cup(block_size * 54, HEIGHT - block_size - 90, 30, 48),Block(block_size * 57, HEIGHT - block_size * 4, block_size),
               Block(block_size * 58, HEIGHT - block_size * 4, block_size),Block(block_size * 59, HEIGHT - block_size * 4, block_size),
               Block(block_size * 60, HEIGHT - block_size * 4, block_size),Block(block_size * 61, HEIGHT - block_size * 4, block_size),
               Block(block_size * 62, HEIGHT - block_size * 4, block_size), Block(block_size * 63, HEIGHT - block_size * 4, block_size),
               Block(block_size * 64, HEIGHT - block_size * 4, block_size), Block(block_size * 65, HEIGHT - block_size * 4, block_size),
               Block(block_size * 66, HEIGHT - block_size * 4, block_size), Block(block_size * 67, HEIGHT - block_size * 4, block_size),
               Pizza(block_size * 66, HEIGHT - block_size * 4 - 68.5,62,38), Block(block_size * 68, HEIGHT - block_size * 4, block_size),
               Block(block_size * 68, HEIGHT - block_size * 5, block_size), Block(block_size * 68, HEIGHT - block_size * 6, block_size),
               Block(block_size * 68, HEIGHT - block_size * 7, block_size), Block(block_size * 68, HEIGHT - block_size * 8, block_size),
               Spike(block_size * 70, HEIGHT - block_size - 32, 16, 32),Spike(block_size * 70.5, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 72, HEIGHT - block_size * 2, block_size), Block(block_size * 73, HEIGHT - block_size * 3, block_size),
               Block(block_size * 74, HEIGHT - block_size * 4, block_size), Block(block_size * 75, HEIGHT - block_size * 5, block_size),
               Block(block_size * 76, HEIGHT - block_size * 6, block_size), Block(block_size * 77, HEIGHT - block_size * 5, block_size), Key1(block_size * 76, HEIGHT - block_size -64, 32, 32),
               Block(block_size * 78, HEIGHT - block_size * 4, block_size), Metalcan(block_size * 75.5, HEIGHT - block_size*5 - 88, 22, 44),
               Spike(block_size * 78, HEIGHT - block_size*4 -32 , 16, 32), Spike(block_size * 78.5, HEIGHT - block_size*4 - 32, 16, 32),
               Spike(block_size * 80.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 81, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 83, HEIGHT - block_size - 32, 16, 32),Spike(block_size * 83.5, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 85.5, HEIGHT - block_size * 4, block_size), 
               Big_Plastic(block_size * 85.5, HEIGHT - block_size - 115, 41, 59), Metalcan(block_size * 88.5, HEIGHT - block_size - 88, 22, 44),
               Block(block_size * 90, HEIGHT - block_size * 5, block_size), Block(block_size * 92, HEIGHT - block_size * 6, block_size),
               Block(block_size * 98, HEIGHT - block_size * 5, block_size), Block(block_size * 99, HEIGHT - block_size * 5, block_size),
               Block(block_size * 100, HEIGHT - block_size * 5, block_size), Block(block_size * 101, HEIGHT - block_size * 5, block_size),
               Block(block_size * 102, HEIGHT - block_size * 5, block_size), Block(block_size * 103, HEIGHT - block_size * 4, block_size),
               Spike(block_size * 103, HEIGHT - block_size*4 - 32, 16, 32), Spike(block_size * 103.5, HEIGHT - block_size*4 - 32, 16, 32),
               Block(block_size * 105, HEIGHT - block_size * 7, block_size), Block(block_size * 106, HEIGHT - block_size * 6, block_size),
               Block(block_size * 107, HEIGHT - block_size * 6, block_size), Block(block_size * 108, HEIGHT - block_size * 6, block_size),
               Block(block_size * 109, HEIGHT - block_size * 6, block_size), Block(block_size * 110, HEIGHT - block_size * 6, block_size),
               Block(block_size * 111, HEIGHT - block_size * 6, block_size), Block(block_size * 112, HEIGHT - block_size * 6, block_size),
               Block(block_size * 113, HEIGHT - block_size * 6, block_size),Block(block_size * 113, HEIGHT - block_size * 7, block_size),
               Block(block_size * 113, HEIGHT - block_size * 8, block_size),Block(block_size * 113, HEIGHT - block_size * 9, block_size),
               Block(block_size * 113, HEIGHT - block_size * 10, block_size), Key2(block_size * 112, HEIGHT - block_size*6 - 64, 32, 32),
               Block(block_size * 96, HEIGHT - block_size * 4, block_size), Block(block_size * 122, HEIGHT - block_size * 4, block_size),
               Block(block_size * 123, HEIGHT - block_size * 4, block_size), Block(block_size * 124, HEIGHT - block_size * 4, block_size),
               Block(block_size * 125, HEIGHT - block_size * 4, block_size), Block(block_size * 126, HEIGHT - block_size * 4, block_size),
               Block(block_size * 127, HEIGHT - block_size * 4, block_size), Block(block_size * 128, HEIGHT - block_size * 4, block_size),
               Block(block_size * 129, HEIGHT - block_size * 4, block_size), Block(block_size * 129, HEIGHT - block_size * 3, block_size),
               Block(block_size * 129, HEIGHT - block_size * 2, block_size), Block(block_size * 133, HEIGHT - block_size * 5, block_size),
               Cup(block_size * 136, HEIGHT - block_size - 90, 30, 48), Block(block_size * 136, HEIGHT - block_size * 6, block_size),
               Block(block_size * 139, HEIGHT - block_size * 5, block_size), Block(block_size * 142, HEIGHT - block_size * 6, block_size),
               Cup(block_size * 142, HEIGHT - block_size - 90, 30, 48),Block(block_size * 145, HEIGHT - block_size * 5, block_size),
               Pizza(block_size * 150, HEIGHT - block_size - 68.5,62,38), Pizza(block_size * 154, HEIGHT - block_size - 68.5,62,38),
               Pizza(block_size * 158, HEIGHT - block_size - 68.5,62,38), Pizza(block_size * 162, HEIGHT - block_size - 68.5,62,38),
               Pizza(block_size * 166, HEIGHT - block_size - 68.5,62,38), Pizza(block_size * 170, HEIGHT - block_size - 68.5,62,38),
               Block(block_size * 175, HEIGHT - block_size * 4, block_size), Block(block_size * 176, HEIGHT - block_size * 4, block_size),
               Block(block_size * 177, HEIGHT - block_size * 4, block_size), Mug(block_size * 177, HEIGHT - block_size - 55, 31, 31),
               Block(block_size * 178, HEIGHT - block_size * 4, block_size),  Block(block_size * 179, HEIGHT - block_size * 4, block_size), 
               Block(block_size * 180, HEIGHT - block_size * 4, block_size),  Block(block_size * 181, HEIGHT - block_size * 4, block_size), 
               Mug(block_size * 180, HEIGHT - block_size - 55, 31, 31), Block(block_size * 182, HEIGHT - block_size * 4, block_size),
               Block(block_size * 183, HEIGHT - block_size * 4, block_size), Block(block_size * 184, HEIGHT - block_size * 5, block_size),
               Block(block_size * 185, HEIGHT - block_size * 5, block_size), Spike(block_size * 185, HEIGHT - block_size*5 - 32, 16, 32), Spike(block_size * 185.5, HEIGHT - block_size*5 - 32, 16, 32),
               Block(block_size * 186, HEIGHT - block_size * 6, block_size), Block(block_size * 187, HEIGHT - block_size * 7, block_size),
               Block(block_size * 188, HEIGHT - block_size * 7, block_size), Spike(block_size * 187.5, HEIGHT - block_size*7 - 32, 16, 32),Spike(block_size * 188, HEIGHT - block_size*7 - 32, 16, 32),
               Block(block_size * 189, HEIGHT - block_size * 4, block_size), Block(block_size * 191, HEIGHT - block_size * 5, block_size),
               Big_Plastic(block_size * 193, HEIGHT - block_size - 115, 41, 59),
               Block(block_size * 196, HEIGHT - block_size * 4, block_size), Block(block_size * 198, HEIGHT - block_size * 5, block_size), 
               Big_Plastic(block_size * 200, HEIGHT - block_size - 115, 41, 59),
               Block(block_size * 204, HEIGHT - block_size * 4, block_size), Block(block_size * 207, HEIGHT - block_size * 4, block_size),
               Block(block_size * 210, HEIGHT - block_size * 5, block_size), Block(block_size * 213, HEIGHT - block_size * 6, block_size),
               Spike(block_size * 215, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 215.5, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 216, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 216.5, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 217, HEIGHT - block_size - 32, 16, 32),Spike(block_size * 217.5, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 218, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 218.5, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 220, HEIGHT - block_size * 4, block_size),Block(block_size * 221, HEIGHT - block_size * 4, block_size),
               Metalcan(block_size * 222.5, HEIGHT - block_size*4 - 88, 22, 44), Block(block_size * 222, HEIGHT - block_size * 4, block_size),
               Block(block_size * 223, HEIGHT - block_size * 4, block_size), Block(block_size * 224, HEIGHT - block_size * 4, block_size),
               Cup(block_size * 226, HEIGHT - block_size - 90, 30, 48),Block(block_size * 230, HEIGHT - block_size * 4, block_size),
               Block(block_size * 230, HEIGHT - block_size * 7, block_size), Big_Plastic(block_size * 232, HEIGHT - block_size - 115, 41, 59),
               Block(block_size * 233, HEIGHT - block_size * 4, block_size), Block(block_size * 233, HEIGHT - block_size * 7, block_size), 
               Big_Plastic(block_size * 235, HEIGHT - block_size - 115, 41, 59), Big_Plastic(block_size * 238, HEIGHT - block_size - 115, 41, 59),
               Block(block_size * 236, HEIGHT - block_size * 4, block_size), Block(block_size * 236, HEIGHT - block_size * 7, block_size),
               Block(block_size * 240, HEIGHT - block_size * 2, block_size), Block(block_size * 241, HEIGHT - block_size * 3, block_size),
               Block(block_size * 242, HEIGHT - block_size * 3, block_size), Block(block_size * 243, HEIGHT - block_size * 3, block_size),
               Block(block_size * 246, HEIGHT - block_size * 5, block_size), Block(block_size * 244, HEIGHT - block_size * 7, block_size),
               Block(block_size * 243, HEIGHT - block_size * 7, block_size), Metalcan(block_size * 243, HEIGHT - block_size*7 - 88, 22, 44),
               Block(block_size * 246.5, HEIGHT - block_size * 8, block_size), Block(block_size * 247.5, HEIGHT - block_size * 8, block_size),
                Block(block_size * 248.5, HEIGHT - block_size * 6, block_size), Spike(block_size * 247, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 247.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 248, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 248.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 249, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 249.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 250, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 250.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 251, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 251.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 252, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 258, HEIGHT - block_size * 4, block_size), Cup(block_size * 258, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 259, HEIGHT - block_size - 90, 30, 48),Cup(block_size * 260, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 261, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 262, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 263, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 264, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 265, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 266, HEIGHT - block_size - 90, 30, 48),
               Block(block_size * 264.5, HEIGHT - block_size * 5.5, block_size), Block(block_size * 271, HEIGHT - block_size * 5.5, block_size),
               Block(block_size * 277.5, HEIGHT - block_size * 5.5, block_size), Block(block_size * 279, HEIGHT - block_size * 7.5, block_size),
               Cup(block_size * 267, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 268, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 269, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 270, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 271, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 272, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 273, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 274, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 275, HEIGHT - block_size - 90, 30, 48), Cup(block_size * 276, HEIGHT - block_size - 90, 30, 48),
               Cup(block_size * 277, HEIGHT - block_size - 90, 30, 48),Cup(block_size * 278, HEIGHT - block_size - 90, 30, 48),
               Block(block_size * 282, HEIGHT - block_size * 2, block_size), Block(block_size * 283, HEIGHT - block_size * 2, block_size),
               Block(block_size * 284, HEIGHT - block_size * 2, block_size),Block(block_size * 285, HEIGHT - block_size * 2, block_size),
               Block(block_size * 286, HEIGHT - block_size * 2, block_size),Spike(block_size * 282, HEIGHT - block_size*2 - 32, 16, 32), Spike(block_size * 282.5, HEIGHT - block_size*2 - 32, 16, 32),
               Spike(block_size * 283, HEIGHT - block_size*2 - 32, 16, 32), Spike(block_size * 283.5, HEIGHT - block_size*2 - 32, 16, 32),
               Spike(block_size * 284, HEIGHT - block_size*2 - 32, 16, 32), Spike(block_size * 284.5, HEIGHT - block_size*2 - 32, 16, 32),
               Spike(block_size * 285, HEIGHT - block_size*2 - 32, 16, 32), Spike(block_size * 285.5, HEIGHT - block_size*2 - 32, 16, 32),
               Spike(block_size * 286, HEIGHT - block_size*2 - 32, 16, 32), Spike(block_size * 286.5, HEIGHT - block_size*2 - 32, 16, 32),
               Key3(block_size * 287, HEIGHT - block_size*4.5 - 64, 32, 32),
               Spike(350, HEIGHT - block_size - 32, 16, 32),Spike(1560, HEIGHT - block_size - 32, 16, 32),Metalcan(block_size * 6.5, HEIGHT - block_size - 88, 22, 44)]


    scroll_offset = 0
    scroll_area_width = 300
    floor_level = HEIGHT  # Define the floor level

    run = True
    while run:
        game_clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        objects = handle_move(player, objects)
        draw(window, background_tiles, bg_image, player, objects, scroll_offset)

        if player.points >= 3:  # Assuming there are 3 keys
            draw_win_screen(window)  # Call the win screen function
            run = False  # End the game loop

        # Check if the player has fallen below the floor
        if player.rect.y > floor_level:
            scroll_offset = player.reset_position()  # Reset player position and update scroll_offset
             # Recreate keys when the player resets
            key1 =Key1(block_size * 76, HEIGHT - block_size -64, 32, 32)
            key2 = Key2(block_size * 112, HEIGHT - block_size*6 - 64, 32, 32)
            key3 = Key3(block_size * 287, HEIGHT - block_size*4.5 - 64, 32, 32)
            objects = [obj for obj in objects if obj.name not in ["key1", "key2", "key3"]]  # Remove old keys
            objects.extend([key1, key2, key3])  # Add keys back to the objects list

        # Check if the player has been hit 3 times
        if player.hit_count >= 3:
            scroll_offset = player.reset_position()  # Reset player position and update scroll_offset
             # Recreate keys when the player resets
            key1 =Key1(block_size * 76, HEIGHT - block_size -64, 32, 32)
            key2 = Key2(block_size * 112, HEIGHT - block_size*6 - 64, 32, 32)
            key3 = Key3(block_size * 287, HEIGHT - block_size*4.5 - 64, 32, 32),
            objects = [obj for obj in objects if obj.name not in ["key1", "key2", "key3"]]  # Remove old keys
            objects.extend([key1, key2, key3])  # Add keys back to the objects list

        if ((player.rect.right - scroll_offset >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - scroll_offset <= scroll_area_width) and player.x_vel < 0):
            scroll_offset += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
