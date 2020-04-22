import sys 
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
# sprite.groupcollide() to look for collisions between members of two groups.

def check_keydown_events(event, ai_settings, screen, ship, bullets): # bullets as an argument in the call.
	""" Respond to keypresses. """

	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
	""" Fire a bullet if limit not reached yet """
	# Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed: # Delimit the bullets.
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet) # we add the bullets to a group.


def check_keyup_events(event, ship):
	""" Respond to releases """
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""  Update position of bullets and get rid of old bullets """
	# Update bullet positions.
	bullets.update()

	# Get rid of bullets that have disappered.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets)
	#print(len(bullets)) # check if the bullets are being delete(terminal).

	# Check for any bullets that have hit aliens.
	# If so, get rid of the bullet and the alien.
	"""
	The sprite.groupcollide() method compares each bullet’s rect with 
	each alien’s rect and returns a dictionary containing the bullets and 
	aliens that have collided. Each key in the dictionary is a bullet,
	 and the corresponding value is the alien that was hit.
	"""

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	""" Respond to bullet-alien collisions """
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # False, True to
																		 # high-powered bullet.


	if collisions:
		"""
		Pygame returns a collisions dictionary. We check whether the dictionary exists,
		 and if it does, the alien’s value is added to the score
		"""
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens) 
			# We multiply the value of each alien by the number of aliens in each list
			# and add this amount to the current score.
			sb.prep_score()
		check_high_score(stats, sb) # when the collisions dictionary is present, and
									# we do so after updating the score for all the 
									# aliens that have been hit.


	if len(aliens) == 0: # Checking if exist any group of aliens.
		# Destroy existing bullets, speed up game,  and create new fleet.
		bullets.empty() # Removing the bullets (cleaning the screen).
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens) # Creating a new fleet of aliens.


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
	""" Respod to keypresses and mouse events. """

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN: # To use the mouse.
			mouse_x, mouse_y = pygame.mouse.get_pos() # Delimit the position.
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)# Move the ship to the right.
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	""" Start a new game when the player clicks Play """
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active: 
			# Play button is that the button region on the screen will continue to 
			# respond to clicks even when the Play button isn’t visible.

			# Reset the game settings.
			ai_settings.initialize_dynamics_settings()


			#Hide the mouse cursor.
			pygame.mouse.set_visible(False)

			# Reset the game statistics.
			stats.reset_stats() # reset the statistics.
			stats.game_active = True

			# Empty the list of aliens and bullets.
			aliens.empty()
			bullets.empty()

			# Create a new fleet and center the ship.
			create_fleet(ai_settings, screen, ship, aliens)
			ship.center_ship()

			
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	""" Update images on teh screen and flip to the new screen """

	# Redraw the screen during each pass through the loop.
	screen.fill(ai_settings.bg_color)

	# Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites(): # Returns a list of all sprites in the group bullets.
		bullet.draw_bullet() 
		"""
		Pygame automatically draws each element in the group at the position defined by its rect 
		attribute. In this case, aliens.draw(screen) draws each alien in 
		the group to the screen.
		"""
	ship.blitme() # Draw the ship at its current location.
	#alien.blitme() # Draw the alien appear on the screen.
	aliens.draw(screen)
	
	# draw the score information.
	sb.show_score()	

	# Draw the play button if the game is inactive.
	if not stats.game_active:
		play_button.draw_button() # draw the button.

	# Make the most recently drawn screen visible.
	pygame.display.flip() # Update the full display Surface to the screen.



def get_number_aliens_x(ai_settings, alien_width):
	""" Determine the number of aliens that fit in a row """
	available_space_x = ai_settings.screen_width - 2 * alien_width # Horizontal space.
	number_aliens_x = int(available_space_x/(2 * alien_width)) # To avoid partial aliens.
															   # and the range() needs an integer.
	return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
	""" Determine the number of rows of aliens that fit on the screen """
	Available_space_y = (ai_settings.screen_height -
		(3 * alien_height) - ship_height)
	number_rows = int(Available_space_y / (2 * alien_height)) # Int to avoid partial aliens.
	return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	""" Create an alien and place it in the row """
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number # x-coordinate(taking in count the space)
	alien.rect.x = alien.x # taking the value.
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number # distance between rows.
	aliens.add(alien) # Adding to the group.


def create_fleet(ai_settings, screen, ship, aliens):
	""" Create a full fleet of aliens """
	# Create an alien and find the number of aliens in a row.
	# Spacing between each alien is equal to one alien width.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) # Horizontal spacing.
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)



	# Create the first row of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# Create an alien an place it in the row.
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number) # Creating an alien.



def check_fleet_edges(ai_settings, aliens):
	""" Respond appropriately if any aliens have reached an edge """
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break


def change_fleet_direction(ai_settings, aliens):
	""" Drop the entire fleet and change the fleet's direction """
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	""" Respond to ship being hit by alien """
	if stats.ship_left > 0:
		# Decrement ships_left.
		stats.ship_left -= 1

		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()

		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# Pause
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True) # Make visible the mouse.


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	""" Check if any aliens have reached the bottom of the screen """
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this same as if the ship got hit.
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break



def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	"""
	Check if the fleet is at an edge,
	and then update the positions of all the aliens in the fleet.
	"""
	check_fleet_edges(ai_settings, aliens) # Check if any alien are at an edge.
	aliens.update()

	# Look for alien-ship collisions.
	"""
	akes two arguments: a sprite and a group. The method looks for any
	member of the group that’s collided with the sprite and stops looping 
	through the group as soon as it finds one mem- ber that has collided with the sprite.
	"""
	if pygame.sprite.spritecollideany(ship, aliens):
		# print("Ship Hit !!!") # Testing in the terminal.
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)


	# Look for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score.
    Description:
    The function takes two parameters, stats and sb. 
    It uses stats to check the current score and the high score,
     and it needs sb to modify the high score image when necessary
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score() # Update the image of the high score.



















