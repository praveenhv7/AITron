#! /usr/bin/env python

"""
Tron 2- Programmed by Evan
"""

# import standard python modules
import os, random, sys, math

# import pygame module
import pygame
from pygame.locals import *
import GameState
import reflex

# Instantiate gameClock to determine the creation of "Nukes"
gameClock = pygame.time.Clock()


# Player 1 Class
class Snake(object):
    # Called when Snake() is called
    def __init__(self):
        self.pos = [160, 304]  # Position of the snake's head
        self.body = []  # List holding the coordinates of the snake's body
        self.length = 3  # Length of the snake
        self.angle = 0  # Direction that the snake is facing
        self.alive = True  # Is he alive, or dead?
        self.bombs = 3  # Number of bombs
        self.nukes = 0  # Number of nukes

    # Called once every frame
    def update(self):

        # Insert the new position of the snake's head
        self.body.insert(0, list(self.pos))

        # make sure the snake's body isn't longer than it's length
        # self.body = self.body[0:self.length]

        # Move 16 pixels according to the angle
        if self.angle == 0:
            self.pos[1] -= 16
        if self.angle == 90:
            self.pos[0] -= 16
        if self.angle == 180:
            self.pos[1] += 16
        if self.angle == 270:
            self.pos[0] += 16

        # If your head ran into your body, die!
        for b in self.body:
            if self.pos == b:
                self.alive = False

        # If your body is not in the 320x320 screen area, die!
        if self.pos[0] not in range(640):
            self.alive = False
        if self.pos[1] not in range(430):
            self.alive = False

    # Draws the character
    def draw(self, surf):

        # Draw the head
        surf.fill((0, 0, 255), (self.pos[0], self.pos[1], 16, 16))

        # Draw the body
        for b in self.body:
            surf.fill((0, 0, 255), (b[0], b[1], 16, 16))


# Snake Class
class Snake2(object):
    # Called when Snake() is called
    def __init__(self):
        self.pos = [320, 304]  # Position of the snake's head
        self.body = []  # List holding the coordinates of the snake's body
        self.length = 3  # Length of the snake
        self.angle = 0  # Direction that the snake is facing
        self.alive = True  # Is he alive, or dead?
        self.bombs = 3  # Number of bombs
        self.nukes = 0  # Number of nukes

    # Called once every frame
    def update(self):

        # Insert the new position of the snake's head
        self.body.insert(0, list(self.pos))

        # make sure the snake's body isn't longer than it's length
        # self.body = self.body[0:self.length]

        # Move 16 pixels according to the angle
        if self.angle == 0:
            self.pos[1] -= 16
        if self.angle == 90:
            self.pos[0] -= 16
        if self.angle == 180:
            self.pos[1] += 16
        if self.angle == 270:
            self.pos[0] += 16

        # If your head ran into your body, die!
        for b in self.body:
            if self.pos == b:
                self.alive = False

        # If your body is not in the 640x430 screen area, die!
        if self.pos[0] not in range(640):
            self.alive = False
        if self.pos[1] not in range(430):
            self.alive = False

    # Draws the character
    def draw(self, surf):

        # Draw the head
        surf.fill((255, 0, 0), (self.pos[0], self.pos[1], 16, 16))

        # Draw the body
        for b in self.body:
            surf.fill((255, 0, 0), (b[0], b[1], 16, 16))


# These are the Bombs
'''
class Fruit(object):

        #Called when Fruit() is called
        def __init__(self):
                self.change_pos() #Create the position of the friot

        #Move the fruit to a random position
        def change_pos(self):
                self.pos = [random.randrange(1, 40)*16, random.randrange(1, 26)*16]

        #Draw the fruit
        def draw(self, surf):
                surf.fill((0, 255, 0), (self.pos[0], self.pos[1], 16, 16))

#These are the Nukes
class Nuke(object):

        #Called when Nuke() is called
        def __init__(self):
                self.change_pos() #Create the position of the Nuke
                self.exist = 1

        #Move the Nuke to a random position
        def change_pos(self):
                self.pos = [random.randrange(1, 40)*16, random.randrange(1, 26)*16]

        #Draw the Nuke
        def draw(self, surf):
                surf.fill((255, 255, 0), (self.pos[0], self.pos[1], 16, 16))
'''


# Distance formula for collision detection
def dist(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dsquared = dx ** 2 + dy ** 2
    result = math.sqrt(dsquared)
    return result


# Main function
def main():
    # Call the SDL arg to center the window when it's inited, and then init pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Set up the pygame window
    pygame.display.set_caption("TRON 2")
    screen = pygame.display.set_mode((640, 480))

    # Init starting objects
    snake = Snake()
    snake2 = Snake2()
    # fruit = Fruit()
    # nuke= Nuke()
    gameState = GameState.GameState(snake, snake2)
    # Instantiate multiple font types
    font = pygame.font.Font(None, 32)
    defaultFont = pygame.font.Font(pygame.font.get_default_font(), 20)
    hugeFont = pygame.font.Font(pygame.font.get_default_font(), 50)

    # Score variables
    score1 = 0
    score2 = 0

    # Total time passed in the game
    totaltime = 0

    while 1:
        print('Regions : ' + str(gameState.checkNumberOfRegions()))
        # Total time accrued
        gameClock.tick()
        totaltime += gameClock.get_time()

        reflex.reflexAgent(gameState)
        # Get the key input from pygame's event module
        for e in pygame.event.get():

            # QUIT is the big red X button on the window bar
            if e.type == QUIT:
                pygame.quit()
                return

            # Check if a key was pressed
            if e.type == KEYDOWN:

                # Quit if the Escape key is pressed
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return

                # Change the snake's angle if the arrow keys are pressed



                '''
                #Bomb firing mechanism- removes the overlap of bomb and snake parts
                if (e.key == K_KP0):
                        if snake.bombs !=0:

                                circX = snake.pos[0]+7
                                circY = snake.pos[1]
                                for i in range(20,30):
                                        pygame.draw.circle(screen,(0,0,0), (circX,circY), i)
                                        for n in snake2.body:
                                                if (i > dist(circX, circY, n[0], n[1])):
                                                        snake2.body.remove(n)

                                        pygame.display.flip()
                                        pygame.time.delay(40)
                                snake.bombs = snake.bombs-1

                #Nuke firing mechanism- removes everything
                if (e.key == K_RCTRL):
                        if snake.nukes != 0:
                                circX = snake.pos[0]+7
                                circY = snake.pos[1]
                                for i in range(50,600):
                                        pygame.draw.circle(screen,(255,255,0), (circX,circY), i)
                                        for n in snake.body:
                                                snake.body.remove(n)
                                        for n in snake2.body:
                                                snake2.body.remove(n)
                                        pygame.display.flip()

                                snake.nukes = snake.nukes -1
                '''
                # Player 2 keys
                if e.key == K_w:
                    snake2.angle = 0

                if e.key == K_a:
                    snake2.angle = 90

                if e.key == K_s:
                    snake2.angle = 180

                if e.key == K_d:
                    snake2.angle = 270
                '''
                if (e.key == K_z):
                        if snake2.bombs != 0:
                                circX = snake2.pos[0]+7
                                circY = snake2.pos[1]

                                for i in range(20,30):
                                        pygame.draw.circle(screen,(0,0,0), (circX,circY), i)
                                        for n in snake.body:
                                                if (i > dist(circX, circY, n[0], n[1])):
                                                        snake.body.remove(n)
                                        pygame.display.flip()
                                        pygame.time.delay(40)
                                snake2.bombs = snake2.bombs -1
                '''
                '''
                #Nuke firing mechanism- removes everything
                if (e.key == K_x):
                        if snake2.nukes != 0:
                                circX = snake2.pos[0]+7
                                circY = snake2.pos[1]
                                for i in range(50,600):
                                        pygame.draw.circle(screen,(255,255,0), (circX,circY), i)
                                        for n in snake.body:
                                                snake.body.remove(n)
                                        for n in snake2.body:
                                                snake2.body.remove(n)
                                        pygame.display.flip()

                                snake2.nukes = snake2.nukes -1

                '''
        # call the snakes update function
        snake.update()
        snake2.update()

        '''
        #If the snake's "head" (pos) is the same as the fruit's, add one to bomb
        if snake.pos == fruit.pos:
                fruit.change_pos()
                snake.bombs+=1

        if snake2.pos == fruit.pos:
                fruit.change_pos()
                snake2.bombs+=1

        #If the snake's head is the same as the nuke, add one to nuke, and make it disappear until the next round (1 per round)
        if snake.pos == nuke.pos:
                snake.nukes+=1
                nuke.exist=2

        if snake2.pos == nuke.pos:
                snake2.nukes+=1
                nuke.exist=2
        '''
        # Collision Detection for the Snakes!
        for b in snake.body:
            if snake2.pos == b:
                snake2.alive = False

        for b in snake2.body:
            if snake.pos == b:
                snake.alive = False

        # If the snake died, draw text that says you died, and reinit the snake and fruit, reset variables.
        if not snake.alive:
            score2 += 1

            # If snake 2 has 10 points-- give winning screen
            if score2 == 10:
                gameovertext = hugeFont.render("Player 2 WINS!", 1, (0, 0, 0))
                screen.blit(gameovertext, (screen.get_width() / 2 - 200, screen.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                score1 = 0
                score2 = 0
                snake = Snake()
                snake2 = Snake2()
                # fruit = Fruit()
                # nuke= Nuke()
                totaltime = 0


            else:
                gameovertext = hugeFont.render("Player 1 has died", 1, (0, 0, 0))
                screen.blit(gameovertext, (screen.get_width() / 2 - 200, screen.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(1000)
                snake = Snake()
                snake2 = Snake2()
                gameState.setGameState(snake, snake2)
                # fruit = Fruit()
                # nuke= Nuke()
                totaltime = 0

        if not snake2.alive:
            score1 += 1

            # If snake 1 has 10 points-- give winning screen
            if score1 == 10:
                gameovertext = hugeFont.render("Player 1 WINS!", 1, (0, 0, 0))
                screen.blit(gameovertext, (screen.get_width() / 2 - 200, screen.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                score1 = 0
                score2 = 0
                snake = Snake()
                snake2 = Snake2()
                gameState.setGameState(snake, snake2)
                # fruit = Fruit()
                # nuke= Nuke()
                totaltime = 0

            else:
                gameovertext = hugeFont.render("Player 2 has died", 1, (0, 0, 0))
                screen.blit(gameovertext, (screen.get_width() / 2 - 200, screen.get_height() / 2))
                pygame.display.flip()
                pygame.time.wait(1000)
                snake = Snake()
                snake2 = Snake2()
                # fruit = Fruit()
                # nuke= Nuke()
                totaltime = 0

        # Draw everything!

        screen.fill((255, 255, 255))

        # If the time accrued is more than 10 seconds, and the nuke has not already been obtained this round
        # Create a nuke
        '''
        if totaltime > 10000 and nuke.exist==1:
                nuke.draw(screen)
        '''
        # Line to separate text from game
        pygame.draw.line(screen, (0, 0, 0), (0, 430), (640, 430), 5)

        snake.draw(screen)
        snake2.draw(screen)
        # fruit.draw(screen)


        ren1 = defaultFont.render("Player 1 Bombs: " + str('NAN'), 1, (0, 0, 0))
        ren2 = defaultFont.render("Player 2 Bombs: " + str('NAN'), 1, (0, 0, 0))
        ren3 = defaultFont.render("Player 1 Score: " + str(score1), 1, (0, 0, 0))
        ren4 = defaultFont.render("Player 2 Score: " + str(score2), 1, (0, 0, 0))
        ren5 = defaultFont.render("Player 1 Nukes: " + str('NAN'), 1, (0, 0, 0))
        ren6 = defaultFont.render("Player 2 Nukes: " + str('NAN'), 1, (0, 0, 0))

        screen.blit(ren3, (0, 440))
        screen.blit(ren4, (0, 460))
        pygame.draw.line(screen, (0, 0, 0), (180, 480), (180, 430), 5)
        screen.blit(ren1, (190, 440))
        screen.blit(ren2, (190, 460))
        pygame.draw.line(screen, (0, 0, 0), (380, 480), (380, 430), 5)
        screen.blit(ren5, (390, 440))
        screen.blit(ren6, (390, 460))

        pygame.display.flip()

        # Wait 100 milliseconds every frame. This keeps things from going a million miles per hour!
        pygame.time.wait(100)


# Run if executeed
if __name__ == "__main__":
    main()
