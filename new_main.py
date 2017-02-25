import pygame
import gamestate
import graphics
import cuestick

game = gamestate.GameState()
button_pressed = game.main_menu()

events = graphics.events()

if (button_pressed==1):
    game.start_pool()
    while not events["closed"]:
        game.check_for_collision()
        game.do_one_frame()
        events = graphics.events()

        while game.all_not_moving():
            cuestick.set_cue(game,0)

pygame.quit()