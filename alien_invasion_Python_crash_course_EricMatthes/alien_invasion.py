# import sys # to exit the game.
import pygame # functionality to make the game.

from pygame.sprite import Group # Used to create a group of bullets. Storage it.
from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
import game_functions as gf
from button import Button
from scoreboard import Scoreboard




def run_game():
	# Initialize pygame, settings, and screen object.
	pygame.init() # initializes the tools of pygame.
	ai_settings = Settings()
	screen = pygame.display.set_mode(
	(ai_settings.screen_width, ai_settings.screen_height)) # size of the dsiplay. 
	pygame.display.set_caption("Alien Invasion")

	# Make the Play button.
	play_button = Button(ai_settings, screen, "Play")

	# Create an instance to store game statistics and create a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	
	### Set the background color.
	### bg_color = (230, 230, 230) #  RGB colors.

	# Make a ship, a group of bullets, and a group of aliens.
	ship = Ship(ai_settings, screen)
	bullets = Group() # Creating the group outside the loop.
	aliens = Group() # Creatinga aliens group outside the loop.
	# This is to avoid use unnecessary memory creating over and over.

	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)

	# Make an alien.
	# alien = Alien(ai_settings, screen)


	# Start the main loop for the game.
	while True:
	
		# Watch for the keyboard and mouse events.
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets) # check the player input.
		# We always need to call check_events() because we need to know 
		# what is happening all the time, even if the user presses Q to quit.
		if stats.game_active:
			ship.update() # Update the ship position.
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets) # The bullets that have been fired.
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets) # Update the position.
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button) # Using the updated
		# positions to draw a new screen at.
		
		
run_game()










