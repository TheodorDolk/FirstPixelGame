import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Start pygame
pygame.init()

# Set up screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Window title
pygame.display.set_caption("My Game")

# Load images
player_run_frames = []
for i in range(6):
    frame = pygame.image.load(f"PNG Sprites\\player_running\\tile00{i}.png").convert_alpha()
    scaled_frame = pygame.transform.scale(frame, (frame.get_width() * 5, frame.get_height() * 5))
    player_run_frames.append(scaled_frame)
print(player_run_frames)

counter = 0
# Main game loop
run = True
while run:
    counter += (1 * 0.005)
    # update background
    screen.fill((0, 0, 0))

    # display images
    screen.blit(player_run_frames[int(counter % 6)], (400, 300))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()

    # Update game logic
