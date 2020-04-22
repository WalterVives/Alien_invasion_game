import pygame 
from pygame.sprite import Sprite


class Alien(Sprite):
	""" Aclass to represent a single alien in the fleet """

	def __init__(self, ai_settings, screen):
		""" Initialize the alien and set ist starting position """
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Load the alien image and set its rect attribute.
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()

		# Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Storage the alien's exact position.
		self.x = float(self.rect.x)

	def blitme(self):
		""" Draw the alien at its current location
		blit(image, (left, top))
		Draw the image to the screen at the given position.
		blit() accepts either a Surface or a string as its image parameter.
		If image is a str then the named image will be loaded from 
		the images/ directory.
			"""
		self.screen.blit(self.image, self.rect)


	def check_edges(self):
		""" Return True if alien is at edge of screen """
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True


	def update(self):
		""" Move the alien right or left """
		self.x += (self.ai_settings.alien_speed_factor * 
						self.ai_settings.fleet_direction) # We track the alien’s exact position,
														  # if it's 1 add and if -1 substraction.
		self.rect.x = self.x # We then use the value of self.x to update the position of the alien’s rect.







