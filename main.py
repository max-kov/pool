import pygame
import gamestate
import collisiontests
import cue

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
            game.cue.make_visible()
            game.do_one_frame()
            events = game.events()
            if events["clicked"]:
                game.cue.check_if_clicked(game,pygame.mouse.get_pos())

pygame.quit()