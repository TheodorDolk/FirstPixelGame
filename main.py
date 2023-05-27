import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GAME')


class Player:
    def __init__(self):
        self.run_color = (0, 0, 0)
        self.run_frame = 0
        self.run_cooldown = 100
        self.run_last_update = pygame.time.get_ticks()
        self.run_frames = []
        player_run = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_run.png').convert_alpha()
        player_run_sheet = spritesheet.SpriteSheet(player_run)
        for i in range(6):
            self.run_frames.append(player_run_sheet.get_image(i, 48, 48, 3, self.run_color))

        self.idle_color = (0, 0, 0)
        self.idle_frame = 0
        self.idle_cooldown = 150
        self.idle_last_update = pygame.time.get_ticks()
        self.idle_frames = []
        player_idle = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_idle.png').convert_alpha()
        player_idle_sheet = spritesheet.SpriteSheet(player_idle)
        for i in range(4):
            self.idle_frames.append(player_idle_sheet.get_image(i, 48, 48, 3, self.idle_color))

    def run(self):
        # update animation
        now = pygame.time.get_ticks()
        if now - self.run_last_update >= self.run_cooldown:
            self.run_frame += 1
            self.run_last_update = now
            if self.run_frame >= len(self.run_frames):
                self.run_frame = 0

        # show frame image
        screen.blit(self.run_frames[self.run_frame], (100, 100))

    def idle(self):
        # update animation
        now = pygame.time.get_ticks()
        if now - self.idle_last_update >= self.idle_cooldown:
            self.idle_frame += 1
            self.idle_last_update = now
            if self.idle_frame >= len(self.idle_frames):
                self.idle_frame = 0

        # show frame image
        screen.blit(self.idle_frames[self.idle_frame], (100, 100))


def main():
    BG = (50, 50, 50)
    player = Player()
    run = True
    run_right = False
    while run:

        # update background
        screen.fill(BG)

        # update animation

        # show frame image

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    run_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    run_right = False
        if run_right:
            player.run()
        else:
            player.idle()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
