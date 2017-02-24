import pygame
import gamestate
import graphics

#creating a game
game = gamestate.GameState()
#making a main menu
button_pressed = game.main_menu()
events = graphics.events()

if (button_pressed==1):
    game.start_pool()
    while not events["closed"]:
        game.check_for_collision()
        # window.draw_table_holes(table_holes, table_margin / 3)
        # window.move_all_once(balls)
        game.do_one_frame()
        events = graphics.events()

        while game.all_not_moving():
            # set_cue(0)
            pass

pygame.quit()