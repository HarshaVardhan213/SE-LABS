import pygame
import sys
from .paddle import Paddle
from .ball import Ball

class GameEngine:
    def __init__(self, width, height):
        pygame.init()
        pygame.mixer.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ping Pong")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5

        self.player_paddle = Paddle(30, height // 2 - 50, 15, 100, (255, 255, 255), height)
        self.ai_paddle = Paddle(width - 45, height // 2 - 50, 15, 100, (255, 255, 255), height)
        self.ball = Ball(width // 2, height // 2, 10, (255, 255, 255), width, height)

        self.game_state = "playing"  # Can be "playing", "game_over", "replay"

        # Load sounds
        try:
            self.paddle_hit_sound = None

            self.wall_bounce_sound = None
            self.score_sound = None
        except pygame.error as e:
            print(f"Warning: Could not load sound files from 'assets' folder. {e}")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player_paddle.velocity_y = -8
                    if event.key == pygame.K_s:
                        self.player_paddle.velocity_y = 8
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        self.player_paddle.velocity_y = 0
            
            elif self.game_state == "replay":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 3
                        self.reset_game()
                    elif event.key == pygame.K_5:
                        self.winning_score = 5
                        self.reset_game()
                    elif event.key == pygame.K_7:
                        self.winning_score = 7
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update(self):
        if self.game_state != "playing":
            return

        self.player_paddle.move()
        self.ai_paddle.ai_move(self.ball)
        self.ball.move()

        # Ball collision with top/bottom walls
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.velocity_y *= -1
            if self.wall_bounce_sound: self.wall_bounce_sound.play()

        # Ball collision with paddles
        if self.ball.rect.colliderect(self.player_paddle.rect) or self.ball.rect.colliderect(self.ai_paddle.rect):
            self.ball.velocity_x *= -1
            if self.paddle_hit_sound: self.paddle_hit_sound.play()

        # Scoring
        if self.ball.rect.left <= 0:
            self.ai_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()
        elif self.ball.rect.right >= self.width:
            self.player_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()

        # Check for game over
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_state = "game_over"

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.game_state == "playing" or self.game_state == "game_over":
            self.player_paddle.draw(self.screen)
            self.ai_paddle.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.draw.aaline(self.screen, (200, 200, 200), (self.width // 2, 0), (self.width // 2, self.height))

            player_text = self.font.render(str(self.player_score), True, (255, 255, 255))
            self.screen.blit(player_text, (self.width // 4, 20))

            ai_text = self.font.render(str(self.ai_score), True, (255, 255, 255))
            self.screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width(), 20))

        if self.game_state == "game_over":
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
            text_surface = self.font.render(winner_text, True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2 - 50))
            self.screen.blit(text_surface, text_rect)
            
            # Transition to replay state after a delay
            pygame.display.flip()
            pygame.time.wait(3000) # Show winner for 3 seconds
            self.game_state = "replay"

        if self.game_state == "replay":
            self.draw_replay_screen()

        pygame.display.flip()

    def draw_replay_screen(self):
        self.screen.fill((0, 0, 0))
        title_text = self.font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(title_text, (self.width/2 - title_text.get_width()/2, self.height/4))

        options = [
            "Play Again:",
            "[3] - Best of 3",
            "[5] - Best of 5",
            "[7] - Best of 7",
            "",
            "[ESC] - Exit"
        ]
        
        for i, option in enumerate(options):
            option_text = self.small_font.render(option, True, (255, 255, 255))
            self.screen.blit(option_text, (self.width/2 - option_text.get_width()/2, self.height/2 + i * 40))

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_state = "playing"

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)