import pygame.font


class Scoreboard():
	""" A class to report scoring information """

	def __init__(self, ai_settings, screen, stats):
		""" Initialize scorekeeping attributes """

		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		# Font settings for scoring inforation.
		self.text_color = (30, 30, 30) # text color.
		self.font = pygame.font.SysFont(None, 48) # font object 

		# Prepare the initial score image.
		self.prep_score() # Turn the text to be displayed into an image.
		self.prep_high_score() # Erepare the high score image.


	def prep_score(self):
		""" Turn the score into a rendered image """
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		#score_str = str(self.stats.score) # Converting the score to string.
		self.score_image = self.font.render(score_str, True, self.text_color,
			 self.ai_settings.bg_color) # Create the image.


		# Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect() 
		self.score_rect.right = self.screen_rect.right -20 # Set its right edge 20 pixels from the right screen edge.
		self.score_rect.top = 20 # We then place the top edge 20 pixels 
								 # down from the top of the screen.


	def show_score(self):
		""" Draw score to the screen """
		self.screen.blit(self.score_image, self.score_rect) # blit is to draw the score image
															# at the location of score_rect.
		self.screen.blit(self.high_score_image, self.high_score_rect)		



	def prep_high_score(self):
		"""Turn the high score into a rendered image."""
		high_score = int(round(self.stats.high_score, -1)) # Round the high score to the nearest 10.
		high_score_str = "{:,}".format(high_score) # Format it with commas.
		self.high_score_image = self.font.render(high_score_str, True, # Generate an image from the high score.
		self.text_color, self.ai_settings.bg_color)

		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx # center the high score rect horizontally.
		self.high_score_rect.top = self.score_rect.top # Set its top attribute to match the top of the score image.








