import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GAME')


class Player:
    def __init__(self):
        self.x_pos = 600
        self.y_pos = 600
        self.scale = 4
        self.direction = 'right'
        self.run_frame = 0
        self.run_cooldown = 100
        self.run_last_update = pygame.time.get_ticks()
        self.run_frames = []
        player_run = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_run.png')
        player_run_sheet = spritesheet.SpriteSheet(player_run)
        for i in range(6):
            self.run_frames.append(player_run_sheet.get_image(i, 48, 48, self.scale))

        self.idle_frame = 0
        self.idle_cooldown = 150
        self.idle_last_update = pygame.time.get_ticks()
        self.idle_frames = []
        player_idle = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_idle.png')
        player_idle_sheet = spritesheet.SpriteSheet(player_idle)
        for i in range(4):
            self.idle_frames.append(player_idle_sheet.get_image(i, 48, 48, self.scale))

    def reset_frame(self, animation):
        if animation == 'run':
            self.idle_frame = 0
        elif animation == 'idle':
            self.run_frame = 0

    def run(self):
        self.reset_frame("run")
        now = pygame.time.get_ticks()
        if now - self.run_last_update >= self.run_cooldown:
            self.run_frame += 1
            self.run_last_update = now
            if self.run_frame >= len(self.run_frames):
                self.run_frame = 0
        if self.direction == "right":
            screen.blit(self.run_frames[self.run_frame], (self.x_pos, self.y_pos + 80))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.run_frames[self.run_frame], True, False),
                        (self.x_pos - 48, self.y_pos + 80))

    def jump(self):
        pass

    def idle(self):
        self.reset_frame("idle")
        now = pygame.time.get_ticks()
        if now - self.idle_last_update >= self.idle_cooldown:
            self.idle_frame += 1
            self.idle_last_update = now
            if self.idle_frame >= len(self.idle_frames):
                self.idle_frame = 0
        if self.direction == "right":
            screen.blit(self.idle_frames[self.idle_frame], (self.x_pos, self.y_pos + 80))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.idle_frames[self.idle_frame], True, False),
                        (self.x_pos - 48, self.y_pos + 80))


def main():
    BG = (50, 50, 50)
    player = Player()
    run_game = True
    run_right = False
    run_left = False
    clock = pygame.time.Clock()
    print(player.y_pos)
    while run_game:
        clock.tick(FPS)
        # update background
        screen.fill(BG)

        # update animation

        # show frame image

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    run_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    run_right = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    run_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    run_left = False

        if run_right:
            player.direction = "right"
            player.run()
            player.x_pos += 4
        elif run_left:
            player.direction = "left"
            player.run()
            player.x_pos -= 4
        else:
            player.idle()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
