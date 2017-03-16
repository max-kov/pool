import pygame
import gamestate
import collisiontests
import graphics

game = gamestate.GameState()
button_pressed = graphics.draw_main_menu(game)

events = game.events()

if not (button_pressed==3):
    game.start_pool()
    while not events["closed"]:
        game.redraw_all()
        events = game.events()
        collisiontests.check_for_collision(game)

        while game.all_not_moving():
            game.cue.make_visible()
            game.redraw_all()
            events = game.events()
            if events["clicked"]:
                game.cue.check_if_clicked(game)

pygame.quit()
