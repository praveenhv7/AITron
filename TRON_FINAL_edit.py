#! /usr/bin/env python

"""
Tron - Programmed by Evan
        Modified by Praveen HV
                    Vinay Nadagoud
                    
"""

#import standard python modules
import os, random, sys, math

#import pygame module
import pygame
from pygame.locals import *
from GameState import GameState
from reflexAgent import reflexAgent
from minimax import minimaxAgent
from alphaBetaAgent import alphaBetaAgent
from randomAgent import randomAgent
from constants import *
from Player import *


gameClock = pygame.time.Clock()


#Distance formula for collision detection
def dist(x1,y1,x2,y2):
        dx = x2 - x1
        dy = y2 - y1
        dsquared = dx**2 + dy**2
        result = math.sqrt(dsquared)
        return result

def draw(screen, player1, player2, defaultFont, score1, score2):
        screen.fill((255, 255, 255))

        # Line to separate text from game
        pygame.draw.line(screen, (0, 0, 0), (0, GAME.PLAY_AREA_HEIGHT), (GAME.SCREEN_WIDTH, GAME.PLAY_AREA_HEIGHT), 5)

        player1.draw(screen)
        player2.draw(screen)

        ren1 = defaultFont.render("Game Score: " + str('NAN'), 1, (0, 0, 0))
        ren3 = defaultFont.render("Player 1 Wins: " + str(score1), 1, (0, 0, 0))
        ren4 = defaultFont.render("Player 2 Wins: " + str(score2), 1, (0, 0, 0))

        screen.blit(ren3, (0, TEXT_AREA.PLAYER1_WINS_YPOS))
        screen.blit(ren4, (0, TEXT_AREA.PLAYER2_WINS_YPOS))
        pygame.draw.line(screen, (0, 0, 0), (TEXT_AREA.SEPERATOR_XPOS, TEXT_AREA.SEPERATOR_YSTART),
                         (TEXT_AREA.SEPERATOR_XPOS, TEXT_AREA.SEPERATOR_YEND), 5)
        screen.blit(ren1, (TEXT_AREA.GAME_SCORE_XPOS, TEXT_AREA.GAME_SCORE_YPOS))

        pygame.display.flip()

def drawWinnerInfo(screen, winner):
        hugeFont= pygame.font.Font( pygame.font.get_default_font(), 50)
        gameovertext = hugeFont.render("Player " + winner + " WINS!", 1, (0, 0, 0))
        screen.blit(gameovertext, (screen.get_width() / 2 - 200, screen.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)

def drawGameOverInfo(screen, winner):
        hugeFont= pygame.font.Font( pygame.font.get_default_font(), 40)
        gameovertext = hugeFont.render("GAME OVER", 1, (0, 245, 0))
        screen.blit(gameovertext, (screen.get_width() / 2 - 100, screen.get_height() / 2 -50))
        winnertext = hugeFont.render("Congratulations Player " + winner + "!", 1, (0, 245, 0))
        screen.blit(winnertext, (screen.get_width() / 2 - 230, screen.get_height() / 2 ))
        pygame.display.flip()
        pygame.time.wait(3000)

#Main function
def main():

        #Call the SDL arg to center the window when it's inited, and then init pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()


        #Set up the pygame window
        pygame.display.set_caption("TRON")
        screen = pygame.display.set_mode((GAME.SCREEN_WIDTH, GAME.SCREEN_HEIGHT))

        #Init starting objects
        gameState = GameState()
        #Instantiate multiple font types
        defaultFont= pygame.font.Font( pygame.font.get_default_font(), 20)

        #Score variables
        score1 =0
        score2 =0

        #Total time passed in the game
        #totaltime = 0

        while 1:

                if gameState.regions == 1:
                        gameState.checkNumberOfRegionsAstar()

                #Total time accrued
                gameClock.tick()
                #totaltime += gameClock.get_time()

                reflexAgent(gameState, "One", "LEFT")
                gameState.moveTron("One")
                #reflexAgent(gameState, "Two", "RANDOM")
                #randomAgent(gameState,"Two")
                #minimaxAgent(gameState,4,"Two")
                alphaBetaAgent(gameState,3,"Two")
                gameState.moveTron("Two")

                #minimaxAgent(gameState)

                #Get the key input from pygame's event module
                for e in pygame.event.get():

                        #QUIT is the big red X button on the window bar
                        if e.type == QUIT:
                                pygame.quit()
                                return

                        #Check if a key was pressed is escape
                        if e.type == KEYDOWN and e.key == K_ESCAPE:
                                pygame.quit()
                                return

                #Collision Detection for the Players!
                gameState.checkCollision()



                #If the player died, draw text that says you died, and reinit the player and fruit, reset variables.
                if not gameState.tronPlayer1.alive:
                        score2+=1
                        if score2 > GAME.NUM_OF_GAMES:
                                drawGameOverInfo(screen,"2")
                                break
                        else:
                                drawWinnerInfo(screen, "2")
                        #gameState.reset()
                        gameState = GameState()
                elif not gameState.tronPlayer2.alive:
                        score1+=1
                        if score1 > GAME.NUM_OF_GAMES:
                                drawGameOverInfo(screen, "1")
                                break
                        else:
                                drawWinnerInfo(screen, "1")
                        #gameState.reset()
                        gameState = GameState()

                #Draw everything!
                draw(screen, gameState.tronPlayer1, gameState.tronPlayer2, defaultFont, score1, score2)

                #Wait 100 milliseconds every frame. This keeps things from going a million miles per hour!
                pygame.time.wait(1)

#Run if executeed
if __name__ == "__main__":
        main()
