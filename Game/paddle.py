import pygame

class Paddle:
    def __init__(self, x, y, width, height, color, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen_height = screen_height
        self.velocity_y = 0
        self.rect = pygame.Rect(x, y, width, height)

    def move(self):
        """Moves the paddle and keeps it within screen bounds."""
        self.y += self.velocity_y
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height
        self.rect.y = self.y

    def ai_move(self, ball):
        """AI logic to track the ball's position."""
        if self.rect.centery < ball.rect.centery:
            self.velocity_y = 6
        elif self.rect.centery > ball.rect.centery:
            self.velocity_y = -6
        else:
            self.velocity_y = 0
        self.move()

    def draw(self, screen):
        """Draws the paddle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)