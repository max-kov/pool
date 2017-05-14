import pygame

import collisiontests
import gamestate
import graphics

game = gamestate.GameState()
button_pressed = graphics.draw_main_menu(game)
events = gamestate.events()

if (button_pressed == 1):
    game.start_pool()
    while not events["closed"]:
        events = gamestate.events()
        collisiontests.resolve_collisions(game)
        game.redraw_all()

        while game.all_not_moving() and not events["closed"]:
            game.cue.visible = True
            game.redraw_all()
            if game.cue.is_clicked(game):
                game.cue.cue_is_active(game)

pygame.quit()
