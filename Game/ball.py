import pygame
import random

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.reset()

    def move(self):
        """Updates the ball's position."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """Draws the ball on the screen."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def reset(self):
        """Resets the ball to the center with a random velocity."""
        self.x = self.original_x
        self.y = self.original_y
        
        # Start moving towards the player or AI randomly
        x_direction = 1 if random.random() < 0.5 else -1
        y_direction = 1 if random.random() < 0.5 else -1
        
        self.velocity_x = 5 * x_direction
        self.velocity_y = 5 * y_direction
        self.rect.center = (self.x, self.y)