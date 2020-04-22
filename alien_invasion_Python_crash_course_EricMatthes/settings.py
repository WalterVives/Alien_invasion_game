class Settings():
	""" A class to store all settings fot Alien Invasion"""
	
	def __init__ (self):
		"""Initialize the game's statics settings"""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230) #  RGB colors.

		# Ship settings.
		self.ship_speed_factor = 10 # pixels.
		self.ship_limit = 3 # lifes.

		# Bullet settings.
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 50

		# Alien settings.
		self.alien_speed_factor = 5
		self.fleet_drop_speed = 10
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# How quickly the game speeds up
		self.speedup_scale = 1.1
		# How quickly the alien point values increase.
		self.score_scale = 1.5

		self.initialize_dynamics_settings() # initialize the values 
		# for attributes that need to change throughout the course of a game


	def initialize_dynamics_settings(self):
		""" Initialize settings that change throughout the game """
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1

		# Fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1 

		# Scoring.
		self.alien_points = 50

	def increase_speed(self):
		""" Increase speed settings and alien point values. 
		To increase the speed of these game elements,
		we multiply each speed setting by the value of speedup_scale.
		"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)# Now when we increase 
		# the speed of the game, we also increase the point value of each hit.


		#print(self.alien_points) # To see the value of each alien in the terminal.







