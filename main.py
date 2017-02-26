import pygame
import gamestate
import cuestick
import collisiontests

game = gamestate.GameState()
button_pressed = game.main_menu()

events = game.events()

if (button_pressed==1):
    game.start_pool()
    while not events["closed"]:
        collisiontests.check_for_collision(game)
        game.do_one_frame()
        events = game.events()

        while game.all_not_moving():
            cuestick.set_cue(game,0)

pygame.quit()