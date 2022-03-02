import sys
import pygame as pg
import random

"""

TODO
* Fix sound lag

"""

pg.init()
pg.mixer.init()
pg.font.init()

# Colours

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Constants

class GameConstants():
    def __init__(self, width, height, fps, background):
        self.screenWidth = width
        self.screenHeight = height
        self.fps = fps
        self.background = pg.image.load(background)
        self.score1 = 0
        self.score2 = 0
        self.winner = ""

game = GameConstants(960, 720, 60, "background.png")
screen = pg.display.set_mode((game.screenWidth, game.screenHeight))

# Sounds

hit = pg.mixer.Sound("hit.wav")
die = pg.mixer.Sound("die.wav")

# Classes

class Paddle():
    def __init__(self, vel, screen, x, y, image, width, height, colour):
        self.vel = vel
        self.screen = screen
        self.image = pg.transform.scale(pg.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.colour = colour
        self.up = False

        
    def draw(self):
        screen.blit(self.image, self.rect)
    
    def move(self):
        keys = pg.key.get_pressed()
        
        if (keys[pg.K_w] and self.colour == red) or (keys[pg.K_UP] and self.colour == blue):
            if not self.up:     
                self.vel = -self.vel
                self.up = True
            self.rect.centery += self.vel
            
        elif (keys[pg.K_s] and self.colour == red) or (keys[pg.K_DOWN] and self.colour == blue):
            if self.up:
                self.vel = -self.vel
                self.up = False
            self.rect.centery += self.vel
        
        if self.rect.bottom >= game.screenHeight:
            self.rect.bottom = game.screenHeight
        
        if self.rect.top <= 0:
            self.rect.top = 0
            
            
class Ball():
    def __init__(self, vel, screen, x, y, image, texts):
        self.xvel = vel
        self.yvel = vel / 5
        self.screen = screen
        self.image = pg.transform.scale(pg.image.load(image), (59, 41))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.directionx = random.randint(0, 1)
        self.directiony = random.randint(0, 1)
        self.texts = texts

    def draw(self):
        screen.blit(self.image, self.rect)
        
    def move(self, objects):
        if self.directionx:
            self.rect.centerx += self.xvel
        else:
            self.rect.centerx -= self.xvel
        
        if self.directiony:
            self.rect.centery += self.yvel
        else:
            self.rect.centery -= self.yvel
            
        for i in objects:
            if self.rect.colliderect(i):
                self.xvel = -self.xvel * 1.05
                self.yvel = self.yvel * (i.vel / abs(i.vel))
                hit.play()

        
        if self.rect.right >= game.screenWidth or self.rect.left <= 0:
            die.play()

            resetFunction(self, self.texts)

        
        if self.rect.bottom >= game.screenHeight or self.rect.top <= 0:
            self.yvel = -self.yvel
        
class Text():
    def __init__(self, font, size, text, colour, screen, x, y):
        self.font = pg.font.Font(font, size)
        self.text = text
        self.colour = colour
        self.screen = screen
        self.position = (x, y)
    
    def draw(self):
        text = self.font.render(self.text, True, self.colour)
        self.screen.blit(text, self.position)
        
# Other Functions

def updateDisplay(screen, **objects):
    screen.blit(game.background, (0,0))
    for kwarg in objects:
        if kwarg == "paddles":
            for item in objects[kwarg]:
                item.move()
        elif kwarg == "ball":
            for item in objects[kwarg]:
                item.move(objects["paddles"])
        for item in objects[kwarg]:
            item.draw()
    
    pg.display.flip()

def resetFunction(ball, texts):
    if abs(ball.rect.centerx - game.screenWidth) < ball.rect.centerx:
        game.score1 += 1
    else:
        game.score2 += 1
    
    if game.score1 >= 7:
        game.winner = "Red Wins!"
        winningText = Text("font.TTF", 100, game.winner, white, screen, game.screenWidth / 4, game.screenHeight / 2)
        texts.append(winningText)
        updateDisplay(screen, texts=texts)
        pg.time.wait(3000)
        sys.exit()
    elif game.score2 >= 7:
        game.winner = "Blue Wins!"
        winningText = Text("font.TTF", 100, game.winner, white, screen, game.screenWidth / 4, game.screenHeight / 2)
        texts.append(winningText)
        updateDisplay(screen, texts=texts)
        pg.time.wait(3000)
        sys.exit()
    pg.time.wait(500)
    main()

# Main Function

def main():
    
    # Object Instantiation
    score1 = Text("font.TTF", 60, str(game.score1), white, screen, game.screenWidth * 0.4, 30)
    score2 = Text("font.TTF", 60, str(game.score2), white, screen, game.screenWidth * 0.6, 30)
    winningText = Text("font.TTF", 200, game.winner, white, screen, game.screenWidth / 2, game.screenHeight / 2)
    texts = [score1, score2, winningText]
    paddle1 = Paddle(20, screen, game.screenWidth * 0.1, game.screenHeight / 2, "paddle1.png", 30, 150, red)
    paddle2 = Paddle(20, screen, game.screenWidth * 0.9, game.screenHeight / 2, "paddle2.png", 30, 150, blue)
    ball = Ball(5, screen, game.screenWidth / 2, game.screenHeight / 2, "ball.png", texts)
    paddles = [paddle1, paddle2]
    balls = [ball]

    # Game Loop
    
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(game.fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                sys.exit()
            
            
        updateDisplay(screen, paddles=paddles, ball=balls, texts=texts)
    
    pg.quit()
    
main()