"""
Missionaries and Cannibals Game - Standalone Matplotlib GUI
This script runs the classic river crossing puzzle using Matplotlib's native UI widgets.
The goal is to move all 3 missionaries and 3 cannibals across the river without the
cannibals ever outnumbering the missionaries on either side.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time
from collections import deque
import matplotlib.widgets as widgets

# -------------------------------------------------------------------------
# Load Image Assets
# -------------------------------------------------------------------------
boat_img = mpimg.imread("boat.png")
human_img = mpimg.imread("human.png")
zombie_img = mpimg.imread("zombie.png")

# -------------------------------------------------------------------------
# Global Game State Variables
# -------------------------------------------------------------------------
boat_x = 6.5                  # Horizontal position of the boat (6.5 is Right, 3.5 is Left)
missionary_on_right = 3       # Number of missionaries on the starting (Right) side
cannibals_on_right = 3        # Number of cannibals on the starting (Right) side
missionary_on_left = 0        # Number of missionaries on the destination (Left) side
cannibals_on_left = 0         # Number of cannibals on the destination (Left) side
step = 0                      # Counter for the total number of moves made

# -------------------------------------------------------------------------
# Setup Matplotlib Figure and Axes
# -------------------------------------------------------------------------
fig = plt.figure(figsize=(10, 6))
# Create the main axes for the game scene, leaving room at the bottom for buttons
ax = plt.axes([0.05, 0.25, 0.9, 0.7])

def add_image(ax, img, x, y, zoom=0.08):
    """Helper function to draw an image at a specific (x, y) coordinate."""
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)

def draw_scene():
    """Clears the current axes and redraws the river, land, boat, and characters based on the state."""
    ax.clear()
    
    # Draw River (Blue rectangle in the middle)
    ax.add_patch(plt.Rectangle((0, 0), 10, 2, color='lightblue'))
    
    # Draw Land (Green rectangles on left and right)
    ax.add_patch(plt.Rectangle((0, 0), 3, 2, color='lightgreen'))
    ax.add_patch(plt.Rectangle((7, 0), 3, 2, color='lightgreen'))
    
    # Draw Boat at its current boat_x position
    imagebox = OffsetImage(boat_img, zoom=0.15)
    ab = AnnotationBbox(imagebox, (boat_x, 1.0), frameon=False)
    ax.add_artist(ab)
    
    # Draw characters on the LEFT SIDE
    for i in range(missionary_on_left):
        add_image(ax, human_img, 0.7, 1.6 - i * 0.3)
    for i in range(cannibals_on_left):
        add_image(ax, zombie_img, 1.7, 1.6 - i * 0.3)
    
    # Draw characters on the RIGHT SIDE
    for i in range(missionary_on_right):
        add_image(ax, human_img, 8.3, 1.6 - i * 0.3)
    for i in range(cannibals_on_right):
        add_image(ax, zombie_img, 7.3, 1.6 - i * 0.3)
    
    # Configure axes limits to fit the drawing
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis('off') # Hide axes ticks and borders
    
    # Update the title with the current status
    boat_pos = 'Left' if boat_x < 5 else 'Right'
    ax.set_title(f"Boat position: {boat_pos} | Step {step}", fontsize=14)
    
    # Notify Matplotlib that the drawing has updated
    fig.canvas.draw_idle()

def animate_boat(start_x, end_x):
    """Animates the boat sliding from one side of the river to the other."""
    global boat_x
    steps = 12
    for i in range(steps + 1):
        # Calculate intermediate position
        boat_x = start_x + (end_x - start_x) * i / steps
        # Clamp position to strictly stay in the water
        boat_x = max(3.5, min(6.5, boat_x))
        draw_scene()
        fig.canvas.flush_events() # Force UI to render the frame immediately
        time.sleep(0.02)          # Small delay for animation speed

def play_move(missionary, cannibals):
    """
    Executes a move involving 'missionary' amount of missionaries and 
    'cannibals' amount of cannibals. Validates the move, runs the animation, 
    updates global variables, and checks win/loss conditions.
    """
    global missionary_on_right, cannibals_on_right
    global missionary_on_left, cannibals_on_left
    global boat_x, step
    
    # The boat can only hold 1 or 2 people
    if (missionary + cannibals) not in [1, 2]:
        print("❌ Invalid move: The boat must hold 1 or 2 people.")
        return
        
    if boat_x > 5: # If boat is currently on the RIGHT going LEFT
        # Check if we have enough people on the right side to make the move
        if missionary > missionary_on_right or cannibals > cannibals_on_right:
            print("❌ Invalid move: Not enough people on this side.")
            return
        
        animate_boat(6.5, 3.5)
        # Update counts
        missionary_on_right -= missionary
        cannibals_on_right -= cannibals
        missionary_on_left += missionary
        cannibals_on_left += cannibals
        
    else: # If boat is currently on the LEFT going RIGHT
        # Check if we have enough people on the left side to make the move
        if missionary > missionary_on_left or cannibals > cannibals_on_left:
            print("❌ Invalid move: Not enough people on this side.")
            return
            
        animate_boat(3.5, 6.5)
        # Update counts
        missionary_on_right += missionary
        cannibals_on_right += cannibals
        missionary_on_left -= missionary
        cannibals_on_left -= cannibals
        
    step += 1
    draw_scene()
    fig.canvas.flush_events() # Force UI update immediately so the player sees the result
    
    # -------------------------------------------------------------------------
    # Win / Loss Condition Checks
    # -------------------------------------------------------------------------
    # Rule: If missionaries are present, they cannot be outnumbered by cannibals
    right_eaten = (missionary_on_right != 0 and missionary_on_right < cannibals_on_right)
    left_eaten = (missionary_on_left != 0 and missionary_on_left < cannibals_on_left)
    
    if right_eaten or left_eaten:
        message = "💀 YOU LOSE: Missionaries were eaten!"
        print(message)
        ax.set_title(message, color='red', fontsize=16)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        return
        
    # Rule: Win if all 3 missionaries and 3 cannibals successfully reach the left side
    if missionary_on_left == 3 and cannibals_on_left == 3:
        message = "🎉 YOU WIN"
        print(message)
        ax.set_title(message, color='green', fontsize=16)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        return

# -------------------------------------------------------------------------
# Artificial Intelligence (Breadth-First Search) Auto-Solver
# -------------------------------------------------------------------------
def is_valid_state(M_left, C_left, M_right, C_right):
    """Returns True if a hypothetical game state is safe/valid, otherwise False."""
    # Cannot have negative people
    if M_left < 0 or C_left < 0 or M_right < 0 or C_right < 0: return False
    # Check if missionaries get eaten on the left
    if (M_left != 0 and M_left < C_left): return False
    # Check if missionaries get eaten on the right
    if (M_right != 0 and M_right < C_right): return False
    return True

def bfs_solve():
    """
    Uses Breadth-First Search (BFS) to find the shortest path of moves to solve the game.
    Returns a list of tuples representing the moves: (missionaries, cannibals, target_side).
    """
    # Start with all 3 people on the Right side
    start = (3, 3, "Right")
    # Goal is to have 0 people on the Right side
    goal = (0, 0, "Left")
    
    queue = deque()
    visited = set() # Keeps track of states to prevent infinite loops
    
    # queue stores (state, path_taken_so_far)
    queue.append((start, []))
    
    # All combinations of people that can fit in the boat
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    while queue:
        (ML, CL, side), path = queue.popleft()
        
        # Avoid processing a state we've already evaluated
        if (ML, CL, side) in visited: continue
        visited.add((ML, CL, side))
        
        # If we reached the goal, return the path that got us here
        if (ML, CL, side) == goal: return path
        
        # Try all 5 possible boat moves from the current state
        for m, c in moves:
            if side == "Right":
                # Moving right to left: subtract from the right side (ML, CL represent Right side here)
                new_state = (ML - m, CL - c, "Left")
                new_ML, new_CL = ML - m, CL - c
                new_MR, new_CR = 3 - new_ML, 3 - new_CL
                if m > ML or c > CL: continue # Can't move more people than available
            else:
                # Moving left to right: add to the right side
                new_state = (ML + m, CL + c, "Right")
                new_ML, new_CL = ML + m, CL + c
                new_MR, new_CR = 3 - new_ML, 3 - new_CL
                if m > (3 - ML) or c > (3 - CL): continue
                
            # If the resulting move is safe and new, add it to the queue to explore later
            if not is_valid_state(new_ML, new_CL, new_MR, new_CR): continue
            if new_state not in visited:
                queue.append((new_state, path + [(m, c, side)]))
                
    return None # Returns None if the puzzle is unsolvable from the given start state

def solve_game(event):
    """Click handler for the Auto Solve button. Executes the BFS solution."""
    solution = bfs_solve()
    if solution is None:
        print("No solution found")
        return
    print("Solving...")
    
    # Automatically execute the moves generated by the AI
    for m, c, side in solution:
        play_move(m, c)
        plt.pause(0.5) # plt.pause allows the Matplotlib event loop to process and draw UI changes

def reset_game(event):
    """Click handler for the Reset button. Resets all global variables to their starting values."""
    global boat_x, missionary_on_right, cannibals_on_right
    global missionary_on_left, cannibals_on_left, step
    boat_x = 6.5
    missionary_on_right = 3
    cannibals_on_right = 3
    missionary_on_left = 0
    cannibals_on_left = 0
    step = 0
    draw_scene()
    fig.canvas.flush_events()

# -------------------------------------------------------------------------
# UI Creation: Generating Interactive Buttons
# -------------------------------------------------------------------------
btn_axes = []
buttons_refs = []
# Dictionary defining the button label mapped to its (missionaries, cannibals) value
moves_dict = {"1M": (1,0), "2M": (2,0), "1C": (0,1), "2C": (0,2), "1M1C": (1,1)}

def make_click_handler(m, c):
    """Factory function to generate a specific callback for each move button."""
    def handler(event):
        play_move(m, c)
    return handler

# Create axes and button widgets for each available move
x_offset = 0.05
for label, (m, c) in moves_dict.items():
    ax_btn = plt.axes([x_offset, 0.05, 0.1, 0.07]) # [left, bottom, width, height]
    btn = widgets.Button(ax_btn, label)
    btn.on_clicked(make_click_handler(m, c))
    btn_axes.append(ax_btn)
    buttons_refs.append(btn) # Keep reference to prevent python garbage collection
    x_offset += 0.12

# Create Reset Button
ax_reset = plt.axes([x_offset, 0.05, 0.1, 0.07])
btn_reset = widgets.Button(ax_reset, 'Reset')
btn_reset.on_clicked(reset_game)
buttons_refs.append(btn_reset)

# Create Auto Solve Button
ax_auto = plt.axes([x_offset + 0.12, 0.05, 0.15, 0.07])
btn_auto = widgets.Button(ax_auto, 'Auto Solve')
btn_auto.on_clicked(solve_game)
buttons_refs.append(btn_auto)

# Set the window title frame
fig.canvas.manager.set_window_title('Missionary and Cannibal Game')

# Initial drawing of the scene before showing the window
draw_scene()
# Start the blocking Matplotlib event loop
plt.show()
