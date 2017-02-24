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
        check_for_collision(table_holes)
        window.draw_table_holes(table_holes, table_margin / 3)
        window.move_all_once(balls)
        events = graphics.events()

        while are_all_not_moving():
            set_cue(0)

pygame.quit()