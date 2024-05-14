# DX-Ball Game

# Developers:
# Ryana Binte Imtiaz, Roll 48
# Fardin Selim Khan, Roll 43

# CSE-4169: Computer Graphics Lab
# Dept of Computer Science and Engineering, University of Dhaka

# Game Controls:
# - **'LEFT Arrow' Key:** Move the paddle to the left.
# - **'RIGHT Arrow' Key:** Move the paddle to the right.
# - **'p' Key:** Pause/Resume the game.
# - **'q' Key:** Quit the game.
# - **'UP Arrow' Key:** Increase the speed of the ball. (Press when the ball hits the paddle)
# - **'SPACE' Key:** Start a new game. (Press after game over)

# Break blocks to increase your score!

import sys
import random
import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Global variables
bx = 800        # Ball x-coordinate
by = 100         # Ball y-coordinate
br = 10         # Ball radius
bdx = 0.3       # Ball x-axis velocity (reduced initial speed)
bdy = 0.3       # Ball y-axis velocity (reduced initial speed)

px = 750        # Paddle x-coordinate
py = 00         # Paddle y-coordinate
pw = 150        # Paddle width
ph = 20         # Paddle height

ww = 1900        # Window width
wh = 900        # Window height

n_blocks_x = 10     # Number of blocks in x-direction
n_blocks_y = 6      # Number of blocks in y-direction
bw = ww // n_blocks_x   # Block width
bh = 30         # Block height
speed_boost_active = False # Flag to increase speed
new_game = False # Flag to start new game
print_game_over = False # Flag to print GameOver message 


blx = [[1 for _ in range(n_blocks_x)] for _ in range(n_blocks_y)]  # 2D array representing the state of blocks (1: active, 0: destroyed)

pc = [           # Paddle colors
   (0.0, 1.0, 0.0),  # Green
   (1.0, 0.0, 0.0),  # Red
   (0.0, 0.0, 1.0),  # Blue
   (1.0, 1.0, 0.0),  # Yellow
   (1.0 , 0.0 , 0.4), # Magenta
   (0.6, 0.0, 0.8), # Violet
   (0.0, 0.6, 1.0), # Indigo
   (1.0, 0.2, 0.0), # Orange
   (0.0, 1.0, 1.0), # Cyan
   (1.0, 0.4, 1.0), # Pink
   (0.8, 0.6, 1.0), # Lavender
   (0.8, 1.0, 0.4), # Mint
   (1.0, 0.6, 0.6), # Peach
   (0.6, 0.0, 0.2), #Burgundy
   (0.6, 0.4, 0.2), # Brown
   (1.0 , 0.4 , 0.4) # Coral Pink

]

cp_color = random.choice(pc)   # Current paddle color

game_over = False   # Flag indicating whether the game is over
is_paused = False   # Flag indicating whether the game is paused
scr = 0             # Player's score

pressed_keys = set()

# This fuction is used to Initialize the OpenGL environment and set up the window
def initialize():
    """
    Initialize the OpenGL environment and set up the window.
    """
    if not glfw.init():
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

    window = glfw.create_window(ww, wh, "DX-Ball", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, keyboard)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_window_pos(window, 0, 50)

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, ww, 0, wh, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glfw.set_time(0)

    while not glfw.window_should_close(window):
        update(window, glfw.get_time())
        draw(window)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

# This fuction is used to Draw a circle at the specified coordinates with the given radius. 
# We call it to draw the ball
def draw_circle(x, y, r):
    """
    Draw a circle at the specified coordinates with the given radius.
    """
    num_segments = 100
    angle_increment = 2.0 * math.pi / num_segments

    glBegin(GL_TRIANGLE_FAN)

    for i in range(num_segments + 1):
        angle = i * angle_increment
        dx = r * math.cos(angle)
        dy = r * math.sin(angle)
        glVertex2f(x + dx, y + dy)

    glEnd()

# This fuction is used to Draw a rectangle at the specified coordinates with the given width, height, and color
# We call it to draw the Paddle
def draw_rectangle(x, y, w, h, color):
    """
    Draw a rectangle at the specified coordinates with the given width, height, and color.
    """
    glColor3f(*color)
    glBegin(GL_QUADS)

    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)

    glEnd()

brick_colors = [[random.choice(pc) for _ in range(n_blocks_x)] for _ in range(n_blocks_y)]  # Store colors for each brick

# This fuction is used to Draw the blocks (bricks) on the screen based on their state
def draw_blocks():
    """
    Draw the blocks on the screen based on their state.
    """
    for i in range(n_blocks_y):
        for j in range(n_blocks_x):
            if blx[i][j]:
                draw_rectangle(j * bw, wh - (i + 1) * bh, bw, bh, brick_colors[i][j])  # Use assigned color for each block

# This is the main draw function that renders the game elements on the screen
def draw(window):
    """
    The main draw function that renders the game elements on the screen.
    """
    global game_over, new_game, print_game_over

    if not game_over:          # Only draw if game is not over
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the white ball by calling draw_circle function
        glColor3f(1.0, 1.0, 1.0)
        draw_circle(bx, by, br)  

        # Draw the random colored paddle by calling draw_rectangle function
        global cp_color
        draw_rectangle(px, py, pw, ph, cp_color)   

        # Draw the blocks(bricks) by calling draw_blocks function
        draw_blocks()  
    else:                     # When game is over
        if print_game_over:
            print(f"...............GAME OVER!...............")    # Print GAME OVER! to terminal 
            print(f"TOTAL SCORE: {round(scr, 2)}")  # Print score to terminal
            print(f"Press the SPACE Key to start a NEW GAME!") 
            print_game_over = False
        if new_game:        # Check if user wants to play new game  
            print(f"...............NEW GAME!...............") # Print to terminal before starting new game
            reset_game()  # Reset the game state for a new game
            new_game = False

# This function Reset all game variables to their initial values for a NEW GAME after GAME OVER
def reset_game():
    """
    Reset all game variables to their initial values.
    """
    global bx, by, bdx, bdy, game_over, scr, speed_boost_active, cp_color, brick_colors, new_game, print_game_over

    bx = 800        # Ball x-coordinate
    by = 100        # Ball y-coordinate
    bdx = 0.2       # Ball x-axis velocity (reduced initial speed)
    bdy = 0.2       # Ball y-axis velocity (reduced initial speed)

    game_over = False   # Flag indicating whether the game is over
    scr = 0             # Player's score
    speed_boost_active = False  # Reset speed boost flag
    new_game = False            # Reset the new game flag
    print_game_over = False     # Reset the flag for printing game over

    cp_color = random.choice(pc)   # Randomize paddle color for a new game

    # Reset block state
    global blx
    blx = [[1 for _ in range(n_blocks_x)] for _ in range(n_blocks_y)]
    # Randomize block colors
    brick_colors = [[random.choice(pc) for _ in range(n_blocks_x)] for _ in range(n_blocks_y)]

# This function Update the game state
def update(window, current_time):
    """
    Update the game state based on events.
    """
    global bx, by, bdx, bdy, game_over, scr, speed_boost_active, print_game_over

    if game_over:
        return

    if not is_paused:
        # Update ball's position
        bx += bdx
        by += bdy

        # Check for collisions with walls
        if bx + br > ww or bx - br < 0:
            bdx *= -1

        if by + br > wh:
            game_over = True
            bdy *= -1

        if by - br < 0:
            bdy *= -1

        # Check for collision with the paddle for direction change of ball
        if (
            bx >= px 
            and bx <= px + pw 
            and by - br <= py + ph
        ):
            bdy *= -1
            change_paddle_color() # Change the paddle color randomly

        # Check for collision with the paddle for manual speed increase
        if (
            bx + br >= px - 10
            and bx - br <= px + pw + 10
            and by - br <= py + ph + 10
            and speed_boost_active
        ):
            increase_speed()
            speed_boost_active = False  # Reset the flag after increasing speed
            
        # Check for collision with blocks
        hit_block_y = int((wh - by) // bh)
        hit_block_x = int(bx // bw)

        if hit_block_y >= 0 and hit_block_y < n_blocks_y and hit_block_x >= 0 and hit_block_x < n_blocks_x and blx[hit_block_y][hit_block_x]:
            bdy *= -1
            blx[hit_block_y][hit_block_x] = 0
            scr += (20*abs(bdx))  # Increament Score according to speed
            print(f"Score: {round(scr, 2)}")  # Print score update to terminal

        # Check for game over condition
        if by - br < 0:
            game_over = True
            print_game_over = True

# This function increases the ball speed and prints the new speed to terminal
# Called when UP arrow key is pressed during ball-paddle collision 
def increase_speed():
    """
    Increase the speed of the ball.
    """
    global bdx, bdy
    bdx *= 1.35
    bdy *= 1.35
    print(f"Speed increased. New Speed: {abs(round(bdx, 2))}")  # Print updated speed to terminal

# This function is used to reset the flag used for speed increase
def reset_speed_boost_flag():
    """
    Reset the speed boost flag.
    """
    global speed_boost_active
    speed_boost_active = False

def change_paddle_color():
    """
    Change the color of the paddle randomly.
    """
    global cp_color
    cp_color = random.choice(pc)

def keyboard(window, key, scancode, action, mods):
    """
    Handle keyboard inputs.
    """
    global px, is_paused, speed_boost_active, new_game

    # Q key is used to Quit the game
    if key == glfw.KEY_Q and action == glfw.PRESS:
        glfw.terminate()
        sys.exit(0)
    # LEFT Arrow key is used to move the paddle to left
    elif key == glfw.KEY_LEFT:
        if action == glfw.PRESS:
            pressed_keys.add(glfw.KEY_LEFT)
        elif action == glfw.RELEASE:
            pressed_keys.discard(glfw.KEY_LEFT)
    # RIGHT Arrow key is used to move the paddle to right
    elif key == glfw.KEY_RIGHT:
        if action == glfw.PRESS:
            pressed_keys.add(glfw.KEY_RIGHT)
        elif action == glfw.RELEASE:
            pressed_keys.discard(glfw.KEY_RIGHT)
    # P key is used to Pause the game
    elif key == glfw.KEY_P and action == glfw.PRESS:
        is_paused = not is_paused
    # UP Arrow key is used to set the speed boost flag
    # The flag is checked when ball hits paddle, to increase speed
    elif key == glfw.KEY_UP:
        if action == glfw.PRESS:
            speed_boost_active = True
        elif action == glfw.RELEASE:
            speed_boost_active = False
    # SPACE key is used to to set the new game flag
    # The flag is checked when game is over, to start a New Game
    elif key == glfw.KEY_SPACE:
        if action == glfw.PRESS:
            new_game = True
        elif action == glfw.RELEASE:
            new_game = False

    # Move paddle continuously if one of the arrow keys is kept pressed
    if glfw.KEY_LEFT in pressed_keys and px > 0:
        px -= 50
    if glfw.KEY_RIGHT in pressed_keys and px + pw < ww:
        px += 50    

def framebuffer_size_callback(window, width, height):
    """
    Callback function for framebuffer size changes.
    """
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == "__main__":
    initialize()
