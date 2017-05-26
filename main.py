import pygame

import collisiontests
import gamestate
import graphics

game = gamestate.GameState()
button_pressed = graphics.draw_main_menu(game)
events = gamestate.events()

if button_pressed == 1:
    game.start_pool()
    while not events["closed"]:
        events = gamestate.events()
        collisiontests.resolve_all_collisions(game)
        game.redraw_all()

        if game.all_not_moving():
            game.check_potted()
            game.cue.make_visible(game.is_1st_players_turn())
            while game.all_not_moving() and not events["closed"]:
                game.redraw_all()
                events = gamestate.events()
                if game.cue.is_clicked(events):
                    game.cue.cue_is_active(game, events)
                elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                    game.cue.make_invisible()
                    game.white_ball.is_active(game, game.is_behind_line_break())
                    game.cue.make_visible(game.is_1st_players_turn())

pygame.quit()
