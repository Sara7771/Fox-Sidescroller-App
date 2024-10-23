import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fox Runner')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)  # Light grey for the ground
GROUND_COLOR = GRAY  # Set the ground to grey

GRAVITY = 1
GROUND_HEIGHT = HEIGHT - 40

fox_image = pygame.image.load('fox.png')  # Replace with path to fox image
fox_image = pygame.transform.scale(fox_image, (60, 60))

# Load obstacle 
rock_image = pygame.image.load('rock.png')  # Replace with path to rock image
rock_image = pygame.transform.scale(rock_image, (40, 40))
tree_image = pygame.image.load('tree.png')  # Replace with path to tree image
tree_image = pygame.transform.scale(tree_image, (50, 70))

# Fox class
class Fox:
    def __init__(self):
        self.image = fox_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.velocity = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity = -15
            self.jumping = True

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.y >= GROUND_HEIGHT - self.rect.height:
            self.rect.y = GROUND_HEIGHT - self.rect.height
            self.jumping = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Obstacle class Rock and Tree
class Obstacle:
    def __init__(self, is_tree=False):
        self.is_tree = is_tree
        if is_tree:
            self.image = tree_image
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_HEIGHT - self.rect.height
        else:
            self.image = rock_image
            self.rect = self.image.get_rect()
            self.rect.y = GROUND_HEIGHT - self.rect.height
        self.rect.x = WIDTH

    def update(self):
        self.rect.x -= 10
        if self.rect.x < -self.rect.width:
            self.rect.x = WIDTH
            self.rect.y = GROUND_HEIGHT - self.rect.height

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Main game loop
def game():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 24)

    fox = Fox()
    obstacles = [Obstacle()]
    score = 0
    game_over = False
    obstacle_timer = 0  # Timer to control obstacle spawn freq
    spawn_delay = 100  
    last_obstacle_x = WIDTH  

    while True:
        screen.fill(WHITE)

        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    fox.jump()
                if event.key == pygame.K_r and game_over:
                    # Restart the game
                    fox = Fox()
                    obstacles = [Obstacle()]
                    score = 0
                    game_over = False
                    obstacle_timer = 0  # Reset obstacle timer
                    last_obstacle_x = WIDTH  # Reset last obstacle position

        if not game_over:
            # Update game objects
            fox.update()
            for obstacle in obstacles:
                obstacle.update()

                # collisions
                if fox.rect.colliderect(obstacle.rect):
                    game_over = True

            # Update score
            score += 1

            if obstacle_timer > spawn_delay and (last_obstacle_x - obstacles[-1].rect.x) > 300:
                # Randomly add a tree or a rock
                if random.randint(0, 1):  # Random choice between tree or rock
                    new_obstacle = Obstacle(is_tree=True)
                else:
                    new_obstacle = Obstacle(is_tree=False)
                
                # Update the x position of the last obstacle added
                last_obstacle_x = new_obstacle.rect.x
                obstacles.append(new_obstacle)
                obstacle_timer = 0  # Reset the timer after spawning a new obstacle

            obstacle_timer += 1  # Increment the timer

        # Draw game objects
        fox.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display game over
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        clock.tick(30)

if __name__ == '__main__':
    game()