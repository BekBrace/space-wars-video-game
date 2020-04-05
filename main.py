# Author : Bek Brace
# Python 3.7.6
# OS Windows 10
# space wars  - interesting fun game for the classics lovers

import os
import random
import turtle
import winsound
import time

turtle.forward(0)
turtle.speed(0)  # speed of the animation
# title
turtle.title("Star Wars")
# background
turtle.bgcolor("black")
# hides turtle
turtle.hideturtle()
# create background image
turtle.bgpic("bg.gif")

# saving memory
turtle.setundobuffer(1)
turtle.tracer(0)  # tells you how often you want to update the screen


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.forward(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.forward(self.speed)

        # boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
            (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)) and \
                (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False


class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.left(45)

    def turn_right(self):
        self.right(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1


class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.forward(self.speed)

        # boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            # play missile sound - be careful that winsound module only supports WAV files
            # filename = "gun.wav"
            # winsound.PlaySound(filename, winsound.SND_FILENAME)
            winsound.Beep(1000, 10)
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)
        # Border check
        if self.xcor() < -290 or self.xcor() > 290  \
                or self.ycor() > 290 or self.ycor() < -290:
            self.goto(-1000, 1000)
            self.status = "ready"


class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)

        self.fd(10)


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        # Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(2)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.forward(600)
            self.pen.right(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" % (self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))


# create game object
game = Game()

# Draw border
game.draw_border()

# Show game status
game.show_status()

# Create my sprites [objects]
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "blue", 0, 0)

allies = []
for i in range(3):
    allies.append(Ally("square", "green", 100, 0))

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

particles = []
for i in range(100):
    particles.append(Particle("circle", "orange", 0, 0))

# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# Main game loop
while True:

    turtle.update()
    time.sleep(0.02)

    player.move()
    missile.move()

    for enemy in enemies:
        enemy.move()
        # check for a collision - player and enemy
        if player.is_collision(enemy):
            # play explosion sound
            # filename = "explosion.wav"
            # winsound.PlaySound(filename, winsound.SND_FILENAME)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            # Decrease score
            game.score += 0
            game.show_status()

          # check for a collision - missile and enemy
        if missile.is_collision(enemy):
            # play explosion sound
            filename = "explosion.wav"
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            # Increase score
            game.score += 100
            game.show_status()
            # Do the explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in allies:
        ally.move()
        # check for a collision - missile and ally
        if missile.is_collision(ally):
            ally.move()
            # play explosion sound
            filename = "explosion.wav"
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score = +100
            game.show_status()

        for particle in particles:
            particle.move()

delay = input("checking...")
