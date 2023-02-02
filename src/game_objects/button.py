import pygame
from src.classes.vector_2d import Vector2D
from src.classes.game_object import GameObject
class Button(GameObject):
	"""
	Button for the menu of the game.
	"""
	def __init__(self,
				 image: "pygame.Surface",
				 position: "Vector2D",
				 size: "Vector2D") -> None:
		"""
		Creates a non-clicked button

		scales should be whole numbers.
		"""
		super().__init__(position)
		self.scale = size
		self.image = pygame.transform.scale(image, (size.x, size.y))
		self.rect = self.image.get_rect()
		self.rect.topleft = tuple(position)
		self.clicked = False

	def main(self, screen: "pygame.Surface", screen_scaling: "Vector2D") -> bool:
		"""
		renders the button and also checks if it is clicked.
		returns true if clicked and false if not.
		"""
		#action is to bot register many clicks for one click of the mouse
		action = False
		#get mouse position
		pos = Vector2D(*pygame.mouse.get_pos())/screen_scaling

		#check mouseover and clicked conditions
		if self.rect.collidepoint(tuple(pos)):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		self.render(screen)

		return action

	def render(self, screen: "pygame.Surface") -> None:
		"""draw button on screen"""
		screen.blit(self.image, (self.rect.x, self.rect.y))