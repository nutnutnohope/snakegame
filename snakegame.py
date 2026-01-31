import turtle  # Import turtle module for graphics
import time    # Import time module to control game speed
import random  # Import random module for random food positions
import os
import tkinter as tk

delay = 0.1    # Initial delay / game speed

# Score
score = 0      # Current score
high_score = 0 # Highest score

# Set up the game window with softer visuals
wn = turtle.Screen()              # Create main game window object
wn.title("Snake Game")           # Set the game window title
wn.bgcolor("#2e8b57")            # Softer green background for comfortable play
wn.setup(width=600, height=600)   # Set the window size to 600x600 pixels
wn.tracer(0)                      # Turn off automatic animation for manual updates

# Attempt to set a custom window icon named 'snake_icon.ico' or 'snake_icon.png'
# Place the icon file alongside this script. Falls back silently if missing.
try:
    root = wn.getcanvas().winfo_toplevel()
    icon_path = os.path.join(os.path.dirname(__file__), 'snake_icon.ico')
    png_path = os.path.join(os.path.dirname(__file__), 'snake_icon.png')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    elif os.path.exists(png_path):
        img = tk.PhotoImage(file=png_path)
        root.iconphoto(True, img)
except Exception:
    pass

# Create a subtle two-tone grid to aid orientation (smaller squares)
kotak = turtle.Turtle()           # Turtle used for drawing the squares
kotak.hideturtle()                # Hide the turtle shape while drawing
kotak.penup()                     # Lift pen to avoid drawing while moving
kotak.speed(0)                    # Set turtle speed to maximum
warna1 = "#3aa75e"              # Subtle light green
warna2 = "#2a6f3a"              # Subtle dark green
ukuran_kotak = 30                 # Smaller squares make movement feel finer

for y in range(-300, 300, ukuran_kotak):         # Loop rows top to bottom
    for x in range(-300, 300, ukuran_kotak):     # Loop columns left to right
        if ((x // ukuran_kotak) + (y // ukuran_kotak)) % 2 == 0:  # Determine checker color
            kotak.color(warna1)
        else:
            kotak.color(warna2)
        kotak.goto(x, y)
        kotak.begin_fill()
        for _ in range(4):
            kotak.pendown()
            kotak.forward(ukuran_kotak)
            kotak.left(90)
        kotak.end_fill()
        kotak.penup()

# Draw a visible but unobtrusive border for the play area
border = turtle.Turtle()
border.hideturtle()
border.penup()
border.goto(-300, -300)
border.pendown()
border.pensize(3)
border.color("#123d1f")
for _ in range(4):
    border.forward(600)
    border.left(90)
border.penup()

# Snake head (rounded for friendlier look)
head = turtle.Turtle()
head.speed(0)
head.shape("circle")            # Rounded head feels softer than square
head.color("#ffb86b")           # Warm color for visibility
head.shapesize(1.2, 1.2)          # Slightly larger head
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food (rounded and high-contrast)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ff4040")   # Contrasting red for clear visibility
food.shapesize(0.9, 0.9)
food.penup()
food.goto(0,100)

# Snake body segments (use rounded shapes for a softer look)
segments = []

# Pen to write the score
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 20, "normal"))  # Slightly smaller font

# Instruction / status pen
instr = turtle.Turtle()
instr.speed(0)
instr.hideturtle()
instr.penup()
instr.goto(0, 230)
instr.color("white")
instr.write("WASD to move  |  P to Pause/Resume", align="center", font=("Courier", 14, "normal"))

# Pause state
paused = False

def toggle_pause():
    global paused
    paused = not paused
    instr.clear()
    if paused:
        instr.write("Paused — press P to resume", align="center", font=("Courier", 14, "normal"))
    else:
        instr.write("WASD to move  |  P to Pause/Resume", align="center", font=("Courier", 14, "normal"))

# Movement control functions for the snake
def go_up():
    if head.direction != "down":  # Prevent the snake from reversing
        head.direction = "up"     # Change direction to up

def go_down():
    if head.direction != "up":    # Prevent the snake from reversing
        head.direction = "down"   # Change direction to down

def go_left():
    if head.direction != "right": # Prevent the snake from reversing
        head.direction = "left"   # Change direction to left

def go_right():
    if head.direction != "left":  # Prevent the snake from reversing
        head.direction = "right"  # Change direction to right

def move():
    # Move the snake head based on current direction
    if head.direction == "up":
        y = head.ycor()           # Get current y coordinate
        head.sety(y + 20)         # Move up by 20 pixels

    if head.direction == "down":
        y = head.ycor()           # Get current y coordinate
        head.sety(y - 20)         # Move down by 20 pixels

    if head.direction == "left":
        x = head.xcor()           # Get current x coordinate
        head.setx(x - 20)         # Move left by 20 pixels

    if head.direction == "right":
        x = head.xcor()           # Get current x coordinate
        head.setx(x + 20)         # Move right by 20 pixels

# Keyboard controls
wn.listen()                       # Enable keyboard listener
wn.onkeypress(go_up, "w")        # Bind W to move up
wn.onkeypress(go_down, "s")      # Bind S to move down
wn.onkeypress(go_left, "a")      # Bind A to move left
wn.onkeypress(go_right, "d")     # Bind D to move right
wn.onkeypress(toggle_pause, "p") # Bind P to pause/resume

# Main game loop
while True:
    wn.update() # Update the game window

    if paused:
        time.sleep(0.08)
        continue

    # Check for collision with border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)             # Pause 1 second after collision
        head.goto(0,0)            # Return head to starting position
        head.direction = "stop" # Stop movement

        # Hide the body segments
        for segment in segments:
            segment.goto(1000, 1000)  # Move segments far off-screen
        
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset game speed
        delay = 0.1

        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 20, "normal")) 

    # Check for collision with the food
    if head.distance(food) < 20:  # If the head is within 20 pixels of the food
        # Move the food to a new random spot
        x = random.randint(-290, 290)  # Random x within the screen bounds
        y = random.randint(-290, 290)  # Random y within the screen bounds
        food.goto(x,y)

        # Add a new segment to the snake's body
        new_segment = turtle.Turtle()    # Create a new body segment
        new_segment.speed(0)
        new_segment.shape("circle")    # Rounded segments
        new_segment.color("#e09a5a")   # Slightly darker than head for depth
        new_segment.shapesize(0.9, 0.9)
        new_segment.penup()
        segments.append(new_segment)

        # Increase game speed slightly
        delay -= 0.001                  # Decrease delay to increase difficulty

        # Increase score
        score += 10                     # Each food is worth 10 points

        # Update high score if needed
        if score > high_score:
            high_score = score
        
        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 20, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):  # Loop backwards from last to second
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move the first segment to where the head is

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    # Check for head collision with body segments
    for segment in segments:
        if segment.distance(head) < 20:  # If a segment is within 20 pixels of the head
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

            for segment in segments:
                segment.goto(1000, 1000)

            segments.clear()
            score = 0
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 20, "normal"))

    # Control frame rate using delay (keeps game speed consistent)
    time.sleep(delay)
