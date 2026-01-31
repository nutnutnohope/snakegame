import turtle
import time
import random
import json
import os
import tkinter as tk

DELAY = 0.1
PLAYFIELD = 300
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "snake_highscores.json")


def load_highscores():
    if os.path.exists(HIGH_SCORE_FILE):  # check if high-score file exists
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:  # open file for reading
                return json.load(f)  # parse JSON and return dict
        except Exception:  # on any error reading/parsing
            return {}  # return empty dict as fallback
    return {}  # file not found -> return empty dict


def save_highscores(data):
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:  # open file for writing
            json.dump(data, f)  # write dict as JSON
    except Exception:  # ignore file I/O errors
        pass  # best-effort save

import turtle
import random
import json
import os

# Game timing and playfield size constants
DELAY = 0.1
PLAYFIELD = 300
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "snake_highscores.json")


# Load high scores from a JSON file and return as a dict.
def load_highscores():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


# Save a highs dict to the JSON file (best-effort, ignore errors).
def save_highscores(data):
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


# Try to set a window icon from nearby files: prefer .ico, fallback to .png.
def set_window_icon(wn):
    # Determine candidate icon files in script directory
    base_dir = os.path.dirname(__file__)
    ico_path = os.path.join(base_dir, "snake_icon.ico")
    png_path = os.path.join(base_dir, "snake_icon.png")
    try:
        # Access the underlying Tk root
        root = wn.getcanvas().winfo_toplevel()
        # Try .ico first (Windows-friendly)
        if os.path.exists(ico_path):
            try:
                root.iconbitmap(ico_path)
                return True
            except Exception:
                pass
        # Try PNG via PhotoImage (works on many platforms)
        if os.path.exists(png_path):
            try:
                img = tk.PhotoImage(file=png_path)
                root.iconphoto(False, img)
                # keep a reference to prevent garbage collection
                wn._icon_img = img
                return True
            except Exception:
                pass
    except Exception:
        pass
    return False


class Player:
    """Represent a player: head turtle, segments list, score and controls."""

    # Initialize a player with start position, base RGB for coloring, key controls and name.
    def __init__(self, start_pos, base_rgb, controls, name):
        self.name = name  # store player name
        self.start_pos = start_pos  # starting (x,y) pos
        self.base_rgb = base_rgb  # tuple (r,g,b) base color
        self.controls = controls  # dict of control keys

        # Create the head turtle and configure appearance/position.
        self.head = turtle.Turtle()  # turtle object for the head
        self.head.speed(0)  # animation speed 0 (max)
        self.head.shape("circle")  # use circle shape for head
        self.head.color(self._rgb(220))  # set head color using scaled RGB
        self.head.penup()  # don't draw when moving
        self.head.goto(*start_pos)  # move to starting position
        self.head.direction = "stop"  # initial movement state

        self.segments = []  # list to hold tail segments
        self.score = 0  # current score
        self.high_score = 0  # player's high score

    # Convert base RGB and a scale into a color tuple for turtle.
    def _rgb(self, scale):
        r = min(255, int(self.base_rgb[0] * scale / 255))  # scale red channel
        g = min(255, int(self.base_rgb[1] * scale / 255))  # scale green channel
        b = min(255, int(self.base_rgb[2] * scale / 255))  # scale blue channel
        return (r, g, b)  # return RGB tuple

    # Return a color for a segment based on its index to form a gradient.
    def _seg_color(self, index):
        scale = 180 + min(75, index * 6)  # compute scale to vary color by index
        return self._rgb(scale)  # return scaled color for segment

    # Reset the player to its starting position and clear its segments and score.
    def reset(self):
        self.head.goto(*self.start_pos)  # move head back to start
        self.head.direction = "stop"  # stop movement
        for seg in self.segments:  # hide each segment off-screen
            seg.goto(1000, 1000)
        self.segments.clear()  # remove segment references
        self.score = 0  # reset player score

    # Set the player's saved high score.
    def set_high(self, high):
        self.high_score = high  # set saved high score

    # Add a new segment to the tail with a color determined by its index.
    def grow(self):
        idx = len(self.segments)  # index for new segment
        seg = turtle.Turtle()  # create new turtle for segment
        seg.speed(0)  # instant animation
        seg.shape("square")  # segment shape
        seg.shapesize(stretch_wid=0.9, stretch_len=0.9)  # slightly smaller square
        turtle.colormode(255)  # ensure 0-255 color mode
        seg.color(self._seg_color(idx))  # color the segment with gradient
        seg.penup()  # don't draw when moving
        self.segments.append(seg)  # add to tail list

    # Move the player's segments and head according to the current direction.
    def move(self):
        for index in range(len(self.segments) - 1, 0, -1):  # move tail segments forward
            x = self.segments[index - 1].xcor()  # get previous segment x
            y = self.segments[index - 1].ycor()  # get previous segment y
            self.segments[index].goto(x, y)  # move current segment to previous position

        if len(self.segments) > 0:  # position first segment at head's previous position
            x = self.head.xcor()  # head x
            y = self.head.ycor()  # head y
            self.segments[0].goto(x, y)  # move first segment to head

        if self.head.direction == "up":  # move head up
            self.head.sety(self.head.ycor() + 20)
        if self.head.direction == "down":  # move head down
            self.head.sety(self.head.ycor() - 20)
        if self.head.direction == "left":  # move head left
            self.head.setx(self.head.xcor() - 20)
        if self.head.direction == "right":  # move head right
            self.head.setx(self.head.xcor() + 20)

    # Check whether the player's head is beyond the playfield boundary.
    def check_border(self):
        x, y = self.head.xcor(), self.head.ycor()  # current head coords
        return abs(x) > PLAYFIELD - 10 or abs(y) > PLAYFIELD - 10  # True if outside boundary

    # Check whether the player's head has collided with its own segments.
    def check_self_collision(self):
        for seg in self.segments:  # check each tail segment
            if seg.distance(self.head) < 20:  # if head is too close to a segment
                return True  # collision detected
        return False  # no self-collision found


# Draw the playfield border and a faint grid to improve visual comfort.
def draw_background(wn):
    drawer = turtle.Turtle()  # turtle used to draw static background
    drawer.hideturtle()  # hide drawing turtle
    drawer.speed(0)  # draw instantly
    drawer.penup()  # lift pen while positioning
    drawer.goto(-PLAYFIELD, -PLAYFIELD)  # move to bottom-left corner
    drawer.pendown()  # begin drawing
    drawer.pensize(3)  # border thickness
    drawer.color("#0b6623")  # border color
    for _ in range(4):  # draw square border
        drawer.forward(PLAYFIELD * 2)  # draw edge
        drawer.left(90)  # turn corner

    # faint grid
    drawer.pensize(1)  # grid line thickness
    drawer.color("#2e8b57")  # grid color
    gap = 20  # spacing between grid lines
    for x in range(-PLAYFIELD + gap, PLAYFIELD, gap):  # vertical lines
        drawer.penup()
        drawer.goto(x, -PLAYFIELD)  # move to bottom of column
        drawer.pendown()
        drawer.goto(x, PLAYFIELD)  # draw up to top
    for y in range(-PLAYFIELD + gap, PLAYFIELD, gap):  # horizontal lines
        drawer.penup()
        drawer.goto(-PLAYFIELD, y)  # move to left of row
        drawer.pendown()
        drawer.goto(PLAYFIELD, y)  # draw to right
    drawer.penup()  # lift pen when finished


# Main entry: set up screen, players, controls and run the game loop via ontimer.
def main():
    highs = load_highscores()

    wn = turtle.Screen()
    wn.title("Snake Game - Two Players")
    wn.bgcolor("#b6e3b6")
    wn.setup(width=600, height=600)
    wn.tracer(0)

    # Attempt to set a custom window icon (place snake_icon.ico or snake_icon.png
    # next to this script). This is optional; function silently fails if absent.
    try:
        set_window_icon(wn)
    except Exception:
        pass

    turtle.colormode(255)  # allow 0-255 RGB color values
    draw_background(wn)  # draw static border and grid

    # Food setup
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("#e63946")
    food.penup()
    food.shapesize(0.9, 0.9)
    food.goto(0, 100)

    # Players: base RGB colors and controls
    p1 = Player(start_pos=(-100, 0), base_rgb=(30, 30, 30),
                controls={"up": "w", "down": "s", "left": "a", "right": "d"}, name="P1")
    p2 = Player(start_pos=(100, 0), base_rgb=(30, 144, 255),
                controls={"up": "i", "down": "k", "left": "j", "right": "l"}, name="P2")

    p1.set_high(highs.get("P1", 0))
    p2.set_high(highs.get("P2", 0))

    # Pen used for score display
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    pen.penup()
    pen.goto(0, 260)

    # Update the on-screen score display for both players.
    def update_display():
        pen.clear()  # erase previous text
        pen.color("#05386b")  # set text color
        pen.write(f"P1: {p1.score} (High {p1.high_score})    P2: {p2.score} (High {p2.high_score})",
                  align="center", font=("Courier", 16, "bold"))  # draw updated scores

    wn.listen()

    # Return a function that sets a player's direction, preventing immediate reverse.
    def make_dir_setter(player, dir_name):
        def set_dir():
            opp = {"up": "down", "down": "up", "left": "right", "right": "left"}  # opposite directions map
            if player.head.direction != opp[dir_name]:  # prevent reversing directly
                player.head.direction = dir_name  # set new direction
        return set_dir

    # Register keyboard handlers for both players.
    wn.onkeypress(make_dir_setter(p1, "up"), p1.controls["up"])
    wn.onkeypress(make_dir_setter(p1, "down"), p1.controls["down"])
    wn.onkeypress(make_dir_setter(p1, "left"), p1.controls["left"])
    wn.onkeypress(make_dir_setter(p1, "right"), p1.controls["right"])

    wn.onkeypress(make_dir_setter(p2, "up"), p2.controls["up"])
    wn.onkeypress(make_dir_setter(p2, "down"), p2.controls["down"])
    wn.onkeypress(make_dir_setter(p2, "left"), p2.controls["left"])
    wn.onkeypress(make_dir_setter(p2, "right"), p2.controls["right"])

    delay = DELAY

    update_display()

    # Single game step called repeatedly by ontimer to avoid blocking sleeps.
    def game_step():
        nonlocal delay
        wn.update()
        # Check for food collisions for each player and handle scoring/growth.
        for player in (p1, p2):
            if player.head.distance(food) < 20:  # head near food
                x = random.randrange(-280, 280, 20)  # random x position
                y = random.randrange(-280, 280, 20)  # random y position
                food.goto(x, y)  # move food to new spot

                player.grow()  # add a tail segment
                player.score += 10  # increase score
                if player.score > player.high_score:  # update high score if needed
                    player.high_score = player.score  # set new high
                    highs[player.name] = player.high_score  # store in highs dict
                    save_highscores(highs)  # persist highs
                delay = max(0.02, delay - 0.002)  # slightly speed up game
                update_display()  # refresh score text

        # Move both players.
        p1.move()  # update p1 position and segments
        p2.move()  # update p2 position and segments

        # Check various collision types and reset affected players.
        for player, other in ((p1, p2), (p2, p1)):
            if player.check_border() or player.check_self_collision():  # border or self hit
                player.reset()  # reset the player
                update_display()  # refresh display

            for seg in other.segments:  # check collision with other player's tail
                if seg.distance(player.head) < 20:  # collision detected
                    player.reset()  # reset player
                    update_display()  # refresh display
                    break  # stop checking other segments

        # Head-to-head collision resets both players.
        if p1.head.distance(p2.head) < 20:  # heads overlap
            p1.reset()  # reset player 1
            p2.reset()  # reset player 2
            update_display()  # refresh display

        # Schedule next step.
        wn.ontimer(game_step, int(delay * 1000))  # call game_step after delay milliseconds

    # Start the repeating game loop.
    game_step()
    wn.mainloop()


if __name__ == "__main__":
    main()
