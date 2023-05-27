import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GAME')

####################


ground_image = pygame.image.load('PNG Sprites\\background_sprites\\ground.png').convert_alpha()
ground_image = pygame.transform.scale_by(ground_image, 1.75)
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"PNG Sprites\\background_sprites\\plx-{i}.png").convert_alpha()
    bg_image = pygame.transform.scale_by(bg_image, 1.6)
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg(scroll):
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.05


def draw_ground(scroll):
    for x in range(15):
        screen.blit(ground_image, (n * (x * ground_width) - scroll * 4, SCREEN_HEIGHT - ground_height))



###################


class Player:
    def __init__(self):
        self.ground_height = (SCREEN_HEIGHT - ground_height) * 0.75
        self.x_pos = 600
        self.y_pos = self.ground_height
        self.scale = 4
        self.direction = 'right'
        self.width = 48 * self.scale
        self.height = 48 * self.scale

        # run animation
        self.run_frame = 0
        self.run_cooldown = 100
        self.run_last_update = pygame.time.get_ticks()
        self.run_frames = []
        player_run = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_run.png')
        player_run_sheet = spritesheet.SpriteSheet(player_run)
        for j in range(6):
            self.run_frames.append(player_run_sheet.get_image(j, 48, 48, self.scale))

        # idle animation
        self.idle_frame = 0
        self.idle_cooldown = 150
        self.idle_last_update = pygame.time.get_ticks()
        self.idle_frames = []
        player_idle = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_idle.png')
        player_idle_sheet = spritesheet.SpriteSheet(player_idle)
        for j in range(4):
            self.idle_frames.append(player_idle_sheet.get_image(j, 48, 48, self.scale))

        # jump animation
        self.jump_frame = 0
        self.jump_cooldown = 400
        self.jump_last_update = pygame.time.get_ticks()
        self.jump_frames = []
        player_jump = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_jump.png')
        player_jump_sheet = spritesheet.SpriteSheet(player_jump)
        for j in range(4):
            self.jump_frames.append(player_jump_sheet.get_image(j, 48, 48, self.scale))

        # attack animation
        self.attack_frame = 0
        self.attack_cooldown = 80
        self.attack_last_update = pygame.time.get_ticks()
        self.attack_frames = []
        player_attack = pygame.image.load('PNG Sprites\\player_sprites\\Cyborg_attack3.png')
        player_attack_sheet = spritesheet.SpriteSheet(player_attack)
        for j in range(8):
            self.attack_frames.append(player_attack_sheet.get_image(j, 48, 48, self.scale))

    def reset_frame(self, animation):
        if animation == 'run':
            self.idle_frame = 0
            self.jump_frame = 0
            self.attack_frame = 0
        elif animation == 'idle':
            self.run_frame = 0
            self.jump_frame = 0
            self.attack_frame = 0
        elif animation == 'jump':
            self.idle_frame = 0
            self.run_frame = 0
            self.attack_frame = 0
        elif animation == 'all':
            self.idle_frame = 0
            self.run_frame = 0
            self.jump_frame = 0

    def run(self):
        self.reset_frame("run")
        now = pygame.time.get_ticks()
        if now - self.run_last_update >= self.run_cooldown:
            self.run_frame += 1
            self.run_last_update = now
            if self.run_frame >= len(self.run_frames):
                self.run_frame = 0
        if self.direction == "right":
            screen.blit(self.run_frames[self.run_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.run_frames[self.run_frame], True, False),
                        (self.x_pos - 48, self.y_pos))

    def idle(self):
        self.reset_frame("idle")
        now = pygame.time.get_ticks()
        if now - self.idle_last_update >= self.idle_cooldown:
            self.idle_frame += 1
            self.idle_last_update = now
            if self.idle_frame >= len(self.idle_frames):
                self.idle_frame = 0
        if self.direction == "right":
            screen.blit(self.idle_frames[self.idle_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.idle_frames[self.idle_frame], True, False),
                        (self.x_pos - 48, self.y_pos))

    def jump(self):
        self.reset_frame("jump")
        now = pygame.time.get_ticks()
        if now - self.jump_last_update >= self.jump_cooldown:
            self.jump_frame += 1
            self.jump_last_update = now
            if self.jump_frame >= len(self.jump_frames):
                self.jump_frame = 0
        if self.direction == "right":
            screen.blit(self.jump_frames[self.jump_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.jump_frames[self.jump_frame], True, False),
                        (self.x_pos - 48, self.y_pos))

    def attack(self):
        self.reset_frame("attack")
        now = pygame.time.get_ticks()
        if now - self.attack_last_update >= self.attack_cooldown:
            self.attack_frame += 1
            self.attack_last_update = now
            if self.attack_frame >= len(self.attack_frames):
                self.attack_frame = 0
        if self.direction == "right":
            screen.blit(self.attack_frames[self.attack_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(pygame.transform.flip(self.attack_frames[self.attack_frame], True, False),
                        (self.x_pos - 48, self.y_pos))


def main():
    FPS = 60
    scroll = 0
    BG = (50, 50, 50)
    player = Player()
    player_speed = 8
    run_game = True
    run_right = False
    run_left = False

    jumping = False
    y_gravity = 0.6
    jump_height = 12
    y_velocity = jump_height

    attacking = False

    clock = pygame.time.Clock()
    print(player.y_pos)
    while run_game:
        clock.tick(FPS)
        # update background
        screen.fill(BG)

        #################
        draw_bg(scroll)
        draw_ground(scroll)
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and scroll > 0:
            scroll -= 2
        if key[pygame.K_a] and scroll < 3000:
            scroll += 2
        ################
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jumping = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    attacking = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    attacking = False
        if attacking:
            player.attack()

        if jumping:
            player.y_pos -= y_velocity
            y_velocity -= y_gravity
            if player.y_pos >= player.ground_height:
                player.y_pos = player.ground_height
                jumping = False
                y_velocity = jump_height
            else:
                player.jump()

        if run_right:
            player.direction = "right"
            if not jumping:
                player.run()
            if player.x_pos <= 900:
                player.x_pos += player_speed
        elif run_left:
            player.direction = "left"
            if not jumping:
                player.run()
            if player.x_pos >= 108:
                player.x_pos -= player_speed
        elif not jumping and not attacking:
            player.idle()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
