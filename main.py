import pygame

import collisiontests
import gamestate
import graphics

game = gamestate.GameState()
button_pressed = graphics.draw_main_menu(game)

events = game.events()

if not (button_pressed == 3):
    game.start_pool()
    while not events["closed"]:
        events = game.events()
        collisiontests.check_for_collision(game)
        game.redraw_all()

        while game.all_not_moving() and not events["closed"]:
            game.cue.make_visible()
            game.redraw_all()
            events = game.events()
            if events["clicked"]:
                game.cue.check_if_clicked(game)

pygame.quit()
