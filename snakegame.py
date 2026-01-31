import turtle  # Import turtle module for graphics
import time    # Import time module to control game speed
import random  # Import random module for random food positions

delay = 0.1    # Initial delay / game speed

# Score
score = 0      # Current score
high_score = 0 # Highest score

# Set up the game window without animation
wn = turtle.Screen()              # Create main game window object
wn.title("Snake Game")           # Set the game window title
wn.bgcolor("#00FF15")            # Set the window background color
wn.setup(width=600, height=600)   # Set the window size to 600x600 pixels
wn.tracer(0)                      # Turn off animation for instant drawing

# Create a two-tone green checkerboard pattern
kotak = turtle.Turtle()           # Turtle used for drawing the squares
kotak.hideturtle()                # Hide the turtle shape while drawing
kotak.penup()                     # Lift pen to avoid drawing while moving
kotak.speed(0)                    # Set turtle speed to maximum
warna1 = "#11BB01"              # Light green color
warna2 = "#009908"              # Dark green color
ukuran_kotak = 40                 # Size of each square in pixels

for y in range(-300, 300, ukuran_kotak):         # Loop rows top to bottom
    for x in range(-300, 300, ukuran_kotak):     # Loop columns left to right
        if ((x // ukuran_kotak) + (y // ukuran_kotak)) % 2 == 0:  # Determine checker color
            kotak.color(warna1)                  # Use color1 for this square
        else:
            kotak.color(warna2)                  # Use color2 for this square
        kotak.goto(x, y)                         # Move turtle to square position
        kotak.begin_fill()                       # Begin filling the square
        for _ in range(4):                       # Draw 4 sides of the square
            kotak.pendown()                      # Put pen down to draw
            kotak.forward(ukuran_kotak)          # Draw side of square
            kotak.left(90)                       # Turn turtle 90 degrees left
        kotak.end_fill()                         # Finish filling the square
        kotak.penup()                            # Lift pen before moving to next square

# Snake head
head = turtle.Turtle()  # Create turtle object for the snake head
head.speed(0)           # Set animation speed to maximum
head.shape("square")  # Set head shape to square
head.color("#dd954e") # Set head color to brownish
head.penup()            # Do not leave a trail when moving
head.goto(0,0)          # Start position at the center of the screen
head.direction = "stop" # Initial direction is stop

# Snake food
food = turtle.Turtle()  # Create turtle object for the food
food.speed(0)           # Set animation speed to maximum
food.shape("triangle") # Set food shape to triangle
food.color("#ffff00")  # Set food color to yellow
food.penup()            # Do not leave a trail when moving
food.goto(0,100)        # Initial food position
segments = []           # Empty list to store snake body segments

# Pen to write the score
pen = turtle.Turtle()   # Turtle used for displaying score text
pen.speed(0)            # Set animation speed to maximum
pen.shape("square")    # Pen shape (not visible)
pen.color("white")     # Text color
pen.penup()             # Do not leave a trail
pen.hideturtle()        # Hide the turtle, only display text
pen.goto(0, 260)        # Position text at the top of the window
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))  # Initial score display

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

# Main game loop
while True:
    wn.update() # Update the game window

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
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Check for collision with the food
    if head.distance(food) < 20:  # If the head is within 20 pixels of the food
        # Move the food to a new random spot
        x = random.randint(-290, 290)  # Random x within the screen bounds
        y = random.randint(-290, 290)  # Random y within the screen bounds
        food.goto(x,y)

        # Add a new segment to the snake's body
        new_segment = turtle.Turtle()    # Create a new body segment
        new_segment.speed(0)             # Set animation speed to maximum
        new_segment.shape("square")    # Set shape to square
        new_segment.color("#dd954e")   # Set segment color to match head
        new_segment.penup()              # Do not draw while moving
        segments.append(new_segment)     # Append the new segment to the list

        # Increase game speed slightly
        delay -= 0.001                  # Decrease delay to increase difficulty

        # Increase score
        score += 10                     # Each food is worth 10 points

        # Update high score if needed
        if score > high_score:
            high_score = score
        
        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):  # Loop backwards from last to second
        x = segments[index-1].xcor()    # Get x of the segment in front
        y = segments[index-1].ycor()    # Get y of the segment in front
        segments[index].goto(x, y)      # Move current segment to that position

    # Move the first segment to where the head is
    if len(segments) > 0:               # If there is at least one segment
        x = head.xcor()                 # Get head x
        y = head.ycor()                 # Get head y
        segments[0].goto(x,y)           # Move first segment to head position

    move()    # Call move() to move the head

    # Check for head collision with body segments
    for segment in segments:
        if segment.distance(head) < 20:  # If a segment is within 20 pixels of the head
            time.sleep(1)                # Pause 1 second after collision
            head.goto(0,0)               # Return head to start
            head.direction = "stop"    # Stop movement
        
            # Hide the body segments
            for segment in segments:
                segment.goto(1000, 1000) # Move segments far off-screen
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset game speed
            delay = 0.1
        
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

time.sleep(delay)  # Wait according to delay value to control game speed
