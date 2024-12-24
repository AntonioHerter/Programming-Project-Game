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
Update the Code: At the files of this repository , you will find a code snippet, called "Alternative code". Copy and paste this code into your main Python file.
Modify the Folder Name: In the main Python file, locate the placeholder "GAME PROJECT" and replace it with the name of your newly created folder.
By following these steps, you will correctly adjust the file paths, allowing the project to run without any issues.

Conclusion
Thank you for checking out the Jumpy Goat game! I hope you enjoy playing it as much as I enjoyed creating it. If you have any questions or suggestions, feel free to reach out!
