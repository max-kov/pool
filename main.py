import pygame
import gamestate
import collisiontests

game = gamestate.GameState()
button_pressed = game.main_menu()

events = game.events()

if not (button_pressed==3):
    game.start_pool()
    while not events["closed"]:
        game.do_one_frame()
        events = game.events()
        collisiontests.check_for_collision(game)

        while game.all_not_moving():
            game.cue.make_visible()
            game.do_one_frame()
            events = game.events()
            if events["clicked"]:
                game.cue.check_if_clicked(game,pygame.mouse.get_pos())

pygame.quit()