'''Due to problems while coding I am recreating the main menu which was before and adding comments new things to implement

Tag designer creator:
'''

'''
Next TO-DOs:
- map 
- keys (separate in 3 diffferent keys)
- sound effects 

'''

# Import necessary libraries -  Remember to check if any of then were forgotten
import pygame # Main game library for creating the game
import random # For random number generation
import math # For mathematical operations
import os # For file path operations
from os import listdir # To list all files in a directory
from os.path import isfile, join # To work with file paths and check file

# Start Pygame
pygame.init()
pygame.font.init()

# Set up the game window
pygame.display.set_caption("Forest and Hooves")
WIDTH, HEIGHT = 1000, 800 
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Game constants for smooth gameplay
FPS = 60  # Frames per second, controls the speed of the game loop
PLAYER_VEL = 7  # Speed of the player’s movement

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
    path = join("GAME PROJECT", "assets", dir1, dir2) # Builds the path to the folder containing the sprite sheets
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
    COLOR = (255, 0, 0)
    GRAVITY = 1.8 # Gravity constant to pull the player down
    SPRITES = load_sprite_sheets("MainCharac", "WhiteG", 72, 72, True) # Load player sprites
    ANIMATION_DELAY = 2 # How quickly the animations change frames

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

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_animation_count += 1
            if self.hit_animation_count >= self.hit_animation_duration:
                self.hit = False  # Reset hit state after animation
                self.hit_animation_count = 0  # Reset animation counter
        self.fall_count += 1
        self.update_sprite()

    def landed(self): # Resets jump and fall counters when the player lands.
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

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

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x): #Draws the player on the screen. Args: win (pygame.Surface): The game window.
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y)) # Draw the player sprite


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
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


# Key class for collectible keys
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Initialize the parent class
        self.image = pygame.image.load(join("assets", "KeyIcons.png")).convert_alpha()  # Load the key image
        self.image = pygame.transform.scale(self.image, (32, 32))  # Scale the key image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the position of the key

# Function to draw the win screen
def draw_win_screen(window):
    font = pygame.font.Font(None, 74)  # Create a font object
    text = font.render("YOU WON", True, (255, 255, 255))  # Render the win text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    window.blit(text, text_rect)  # Draw the text on the window
    pygame.display.update()  # Update the display
    pygame.time.delay(2000)  # Wait for 2 seconds

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
def draw(window, background, bg_image, player, objects, offset_x):
    """
    Draws all game elements on the screen.
    Args:
        window (pygame.Surface): The game window.
        background (list): Tiled background positions.
        bg_image (pygame.Surface): Background image.
        player (Player): Player object.
        offset_x (int): Scrolling offset.
    """
    for tile in background: # Loop through all background tiles
        window.blit(bg_image, tile) # Draw each tile at its position

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)  # Draw the player

    pygame.display.update()# Update the display


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 6)
    collide_right = collide(player, objects, PLAYER_VEL * 6)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "spike":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "bigplastic":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current 
        if obj and obj.name == "cup":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "metalcan":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "mug":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time
        if obj and obj.name == "pizza":
            player.make_hit(pygame.time.get_ticks())  # Call make_hit with current time



def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("green.png")

    block_size = 100

    player = Player(100, 100, 50, 50)
    spike = Spike(100, HEIGHT - block_size - 32, 16, 32)
    bigplastic = Big_Plastic(100, HEIGHT - block_size - 115, 41, 59)
    mug = Mug(100, HEIGHT - block_size - 55, 31, 31)
    cup = Cup(100, HEIGHT - block_size - 90, 30, 48)
    metalcan= Metalcan(100, HEIGHT - block_size - 88, 22, 44)
    pizza= Pizza(100, HEIGHT - block_size - 68.5,62,38)

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 20) // block_size)]
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
               Block(block_size * 76, HEIGHT - block_size * 6, block_size), Block(block_size * 77, HEIGHT - block_size * 5, block_size),
               Block(block_size * 78, HEIGHT - block_size * 4, block_size), Metalcan(block_size * 75.5, HEIGHT - block_size*5 - 88, 22, 44),
               Spike(block_size * 78, HEIGHT - block_size*4 -32 , 16, 32), Spike(block_size * 78.5, HEIGHT - block_size*4 - 32, 16, 32),
               Spike(block_size * 80.5, HEIGHT - block_size - 32, 16, 32), Spike(block_size * 81, HEIGHT - block_size - 32, 16, 32),
               Spike(block_size * 83, HEIGHT - block_size - 32, 16, 32),Spike(block_size * 83.5, HEIGHT - block_size - 32, 16, 32),
               Block(block_size * 85.5, HEIGHT - block_size * 4, block_size), 
               Big_Plastic(block_size * 85.5, HEIGHT - block_size - 115, 41, 59), Metalcan(block_size * 88.5, HEIGHT - block_size - 88, 22, 44),
               Block(block_size * 90, HEIGHT - block_size * 5, block_size), Block(block_size * 92, HEIGHT - block_size * 6, block_size),
               Block(block_size * 98, HEIGHT - block_size * 5, block_size), Block(block_size * 99, HEIGHT - block_size * 4, block_size),
               Block(block_size * 100, HEIGHT - block_size * 5, block_size), Block(block_size * 101, HEIGHT - block_size * 4, block_size),
               Block(block_size * 102, HEIGHT - block_size * 5, block_size), Block(block_size * 103, HEIGHT - block_size * 4, block_size),
               Spike(block_size * 103, HEIGHT - block_size*4 - 32, 16, 32), Spike(block_size * 103.5, HEIGHT - block_size*4 - 32, 16, 32),
               Block(block_size * 105, HEIGHT - block_size * 7, block_size), Block(block_size * 106, HEIGHT - block_size * 6, block_size),
               Block(block_size * 107, HEIGHT - block_size * 6, block_size), Block(block_size * 108, HEIGHT - block_size * 6, block_size),
               Block(block_size * 109, HEIGHT - block_size * 6, block_size), Block(block_size * 110, HEIGHT - block_size * 6, block_size),
               Block(block_size * 111, HEIGHT - block_size * 6, block_size), Block(block_size * 112, HEIGHT - block_size * 6, block_size),
               Block(block_size * 113, HEIGHT - block_size * 6, block_size),Block(block_size * 113, HEIGHT - block_size * 7, block_size),
               Block(block_size * 113, HEIGHT - block_size * 8, block_size),Block(block_size * 113, HEIGHT - block_size * 9, block_size),
               Block(block_size * 113, HEIGHT - block_size * 10, block_size),
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
               Spike(350, HEIGHT - block_size - 32, 16, 32),Spike(1560, HEIGHT - block_size - 32, 16, 32),Metalcan(block_size * 6.5, HEIGHT - block_size - 88, 22, 44)]


    offset_x = 0
    scroll_area_width = 200
    y_floor = HEIGHT  # Define the floor level

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        # Check if the player has fallen below the floor
        if player.rect.y > y_floor:
            offset_x = player.reset_position()  # Reset player position and update offset_x

        # Check if the player has been hit 3 times
        if player.hit_count >= 3:
            offset_x = player.reset_position()  # Reset player position and update offset_x

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)