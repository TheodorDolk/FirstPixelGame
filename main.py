import json
import sys
import pygame as py

import spritesheet
from math import ceil
from button import Button

py.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('GAME')

ground_image = py.image.load('PNG Sprites\\background_sprites\\ground.png').convert_alpha()
ground_image = py.transform.scale_by(ground_image, 1.75)
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []

for i in range(1, 6):
    bg_image = py.image.load(f"PNG Sprites\\background_sprites\\plx-{i}.png").convert_alpha()
    bg_image = py.transform.scale_by(bg_image, 1.6)
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

tiles = ceil(SCREEN_WIDTH / bg_width) + 1


def draw_bg(scroll, n):
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, (n * (x * bg_width) - scroll * speed, 0))
            speed += 0.2


def draw_ground(scroll, n):
    for x in range(15):
        screen.blit(ground_image, (n * (x * ground_width) - scroll * 4, SCREEN_HEIGHT - ground_height))


class Enemy:
    def __init__(self):
        self.ground_height = (SCREEN_HEIGHT - ground_height) * 0.75
        self.x_pos = 600
        self.y_pos = self.ground_height
        self.scale = 4
        self.direction = 'right'
        self.width = 48 * self.scale
        self.height = 48 * self.scale
        self.mask = py.mask.from_surface(py.image.load('PNG Sprites\\enemy_sprites\\Biker_idle.png'))
        self.hurt = False
        self.health = 100
        self.alive = True
        self.fully_dead = False

        # idle animation
        self.idle_frame = 0
        self.idle_cooldown = 150
        self.idle_last_update = py.time.get_ticks()
        self.idle_frames = []
        enemy_idle = py.image.load('PNG Sprites\\enemy_sprites\\Biker_idle.png')
        enemy_idle_sheet = spritesheet.SpriteSheet(enemy_idle)
        for j in range(4):
            self.idle_frames.append(enemy_idle_sheet.get_image(j, 48, 48, self.scale))

        # hurt animation
        self.hurt_frame = 0
        self.hurt_cooldown = 100
        self.hurt_last_update = py.time.get_ticks()
        self.hurt_frames = []
        enemy_hurt = py.image.load('PNG Sprites\\enemy_sprites\\Biker_hurt.png')
        enemy_hurt_sheet = spritesheet.SpriteSheet(enemy_hurt)
        for j in range(2):
            self.hurt_frames.append(enemy_hurt_sheet.get_image(j, 48, 48, self.scale))

        # death animation
        self.death_frame = 0
        self.death_cooldown = 150
        self.death_last_update = py.time.get_ticks()
        self.death_frames = []
        enemy_death = py.image.load('PNG Sprites\\enemy_sprites\\Biker_death.png')
        enemy_death_sheet = spritesheet.SpriteSheet(enemy_death)
        for j in range(6):
            self.death_frames.append(enemy_death_sheet.get_image(j, 48, 48, self.scale))

    def idle(self):
        if self.alive:
            now = py.time.get_ticks()
            if now - self.idle_last_update >= self.idle_cooldown:
                self.idle_frame += 1
                self.idle_last_update = now
                if self.idle_frame >= len(self.idle_frames):
                    self.idle_frame = 0
            if self.direction == "right":
                frame = self.idle_frames[self.idle_frame]
                if self.hurt:
                    frame = self.hurt_frames[self.hurt_frame]
                    if now - self.hurt_last_update >= self.hurt_cooldown:
                        self.hurt_frame += 1
                        self.hurt_last_update = now
                        if self.hurt_frame >= len(self.hurt_frames):
                            self.hurt_frame = 0
                    self.health -= 1
                self.mask = py.mask.from_surface(self.idle_frames[self.idle_frame])
                screen.blit(frame, (self.x_pos, self.y_pos))
            elif self.direction == "left":
                frame = py.transform.flip(self.idle_frames[self.idle_frame], True, False)
                screen.blit(frame, (self.x_pos - 48, self.y_pos))
                self.mask = py.mask.from_surface(py.transform.flip(self.idle_frames[self.idle_frame], True, False))

    def die(self):
        now = py.time.get_ticks()
        if now - self.death_last_update >= self.death_cooldown and not self.fully_dead:
            self.death_frame += 1
            self.death_last_update = now
            if self.death_frame >= len(self.death_frames):
                self.death_frame = 5
                self.fully_dead = True
        if self.direction == "right":
            frame = self.death_frames[self.death_frame]
            screen.blit(frame, (self.x_pos, self.y_pos))
        elif self.direction == "left":
            frame = py.transform.flip(self.death_frames[self.death_frame], True, False)
            screen.blit(frame, (self.x_pos - 48, self.y_pos))


class Player:
    def __init__(self):
        self.punch_sound = py.mixer.Sound('MP3 Sounds\\short_punch.mp3')
        self.ground_height = (SCREEN_HEIGHT - ground_height) * 0.75
        self.x_pos = 600
        self.y_pos = self.ground_height
        self.scale = 4
        self.direction = 'right'
        self.width = 48 * self.scale
        self.height = 48 * self.scale
        self.mask = None
        self.projectiles = []
        self.projectile_speed = 25

        # run animation
        self.run_frame = 0
        self.run_cooldown = 100
        self.run_last_update = py.time.get_ticks()
        self.run_frames = []
        player_run = py.image.load('PNG Sprites\\player_sprites\\Cyborg_run.png')
        player_run_sheet = spritesheet.SpriteSheet(player_run)
        for j in range(6):
            self.run_frames.append(player_run_sheet.get_image(j, 48, 48, self.scale))

        # idle animation
        self.idle_frame = 0
        self.idle_cooldown = 150
        self.idle_last_update = py.time.get_ticks()
        self.idle_frames = []
        player_idle = py.image.load('PNG Sprites\\player_sprites\\Cyborg_idle.png')
        player_idle_sheet = spritesheet.SpriteSheet(player_idle)
        for j in range(4):
            self.idle_frames.append(player_idle_sheet.get_image(j, 48, 48, self.scale))

        # jump animation
        self.jump_frame = 0
        self.jump_cooldown = 400
        self.jump_last_update = py.time.get_ticks()
        self.jump_frames = []
        player_jump = py.image.load('PNG Sprites\\player_sprites\\Cyborg_jump.png')
        player_jump_sheet = spritesheet.SpriteSheet(player_jump)
        for j in range(4):
            self.jump_frames.append(player_jump_sheet.get_image(j, 48, 48, self.scale))

        # attack animation
        self.attack_frame = 0
        self.attack_cooldown = 80
        self.attack_last_update = py.time.get_ticks()
        self.attack_frames = []
        player_attack = py.image.load('PNG Sprites\\player_sprites\\Cyborg_attack3.png')
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
        now = py.time.get_ticks()
        if now - self.run_last_update >= self.run_cooldown:
            self.run_frame += 1
            self.run_last_update = now
            if self.run_frame >= len(self.run_frames):
                self.run_frame = 0
        if self.direction == "right":
            screen.blit(self.run_frames[self.run_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(py.transform.flip(self.run_frames[self.run_frame], True, False),
                        (self.x_pos - 48, self.y_pos))

    def idle(self):
        self.reset_frame("idle")
        now = py.time.get_ticks()
        if now - self.idle_last_update >= self.idle_cooldown:
            self.idle_frame += 1
            self.idle_last_update = now
            if self.idle_frame >= len(self.idle_frames):
                self.idle_frame = 0
        if self.direction == "right":
            frame = self.idle_frames[self.idle_frame]
            self.mask = py.mask.from_surface(frame)
            screen.blit(frame, (self.x_pos, self.y_pos))
        elif self.direction == "left":
            frame = py.transform.flip(self.idle_frames[self.idle_frame], True, False)
            self.mask = py.mask.from_surface(frame)
            screen.blit(frame, (self.x_pos - 48, self.y_pos))

    def jump(self):
        self.reset_frame("jump")
        now = py.time.get_ticks()
        if now - self.jump_last_update >= self.jump_cooldown:
            self.jump_frame += 1
            self.jump_last_update = now
            if self.jump_frame >= len(self.jump_frames):
                self.jump_frame = 0
        if self.direction == "right":
            screen.blit(self.jump_frames[self.jump_frame], (self.x_pos, self.y_pos))
        elif self.direction == "left":
            screen.blit(py.transform.flip(self.jump_frames[self.jump_frame], True, False),
                        (self.x_pos - 48, self.y_pos))

    def attack(self):
        self.reset_frame("attack")
        now = py.time.get_ticks()
        if now - self.attack_last_update >= self.attack_cooldown:
            self.attack_frame += 1
            if self.attack_frame == 5 or self.attack_frame == 7:
                py.mixer.Sound.play(self.punch_sound)
                self.projectiles.append(Projectile(self.x_pos + 142, self.y_pos + 28, self.direction, self.projectile_speed))
            self.attack_last_update = now
            if self.attack_frame >= len(self.attack_frames):
                self.attack_frame = 0
        if self.direction == "right":
            frame = self.attack_frames[self.attack_frame]
            screen.blit(frame, (self.x_pos, self.y_pos))
            self.mask = py.mask.from_surface(frame)
        elif self.direction == "left":
            frame = py.transform.flip(self.attack_frames[self.attack_frame], True, False)
            screen.blit(frame, (self.x_pos - 48, self.y_pos))
            self.mask = py.mask.from_surface(frame)

    def update_projectiles(self):
        if self.projectiles:
            for projectile in self.projectiles:
                if projectile.x_pos < -100 or projectile.x_pos > 1300:
                    self.projectiles.remove(projectile)
                projectile.update()
        print(len(self.projectiles))


projectile_frames = []
projectile = py.image.load('PNG Sprites\\player_sprites\\8_1.png')
projectile_sheet = spritesheet.SpriteSheet(projectile)
for j in range(6):
    projectile_frames.append(projectile_sheet.get_image(j, 48, 48, 3))


class Projectile:
    def __init__(self, x, y, direction, speed):
        self.x_pos = x
        self.y_pos = y
        self.direction = direction
        self.projectile_frames = projectile_frames
        self.projectile_last_update = 0
        self.projectile_speed = speed
        self.right_projectile_frame = self.projectile_frames[0]
        self.left_projectile_frame = py.transform.flip(self.projectile_frames[0], True, False)
        self.update()

    def update(self):
        if self.direction == "right":
            screen.blit(self.right_projectile_frame, (self.x_pos, self.y_pos))
            self.x_pos += self.projectile_speed
            print("lol")
        elif self.direction == "left":
            screen.blit(self.left_projectile_frame, (self.x_pos - 284, self.y_pos))
            self.x_pos -= self.projectile_speed
            print("bajs")


def play():
    py.mixer.music.load("MP3 Sounds/play_music.mp3")
    py.mixer.music.set_volume(0.15)
    py.mixer.music.play(-1)
    FPS = 60
    scroll = 0  # acts as a variable to track background position
    players_pos = 0  # acts as a variable to track player position
    BG = (50, 50, 50)

    enemy = Enemy()
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
    clock = py.time.Clock()

    while run_game:
        clock.tick(FPS)
        # update background
        screen.fill(BG)

        #################
        for tile in range(0, tiles):
            draw_bg(scroll, tile)
            draw_ground(scroll, tile)

        key = py.key.get_pressed()
        if key[py.K_d] and player.x_pos > 900:
            players_pos += player_speed
            scroll += 2

        if scroll > bg_width:
            scroll = 0

        ################
        enemy.idle()
        # event handler
        for event in py.event.get():
            if event.type == py.QUIT:
                run_game = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_d:
                    run_right = True
            if event.type == py.KEYUP:
                if event.key == py.K_d:
                    run_right = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    run_left = True
            if event.type == py.KEYUP:
                if event.key == py.K_a:
                    run_left = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    jumping = True
            if event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    attacking = True
            if event.type == py.MOUSEBUTTONUP:
                if event.button == 1:
                    attacking = False
        if attacking and not jumping and not run_left and not run_right:
            player.attack()
        player.update_projectiles()
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

        # collision detection using masks
        if player.direction == "right":
            offset = (player.x_pos - enemy.x_pos + 48, player.y_pos - enemy.y_pos)
        else:
            offset = (player.x_pos - enemy.x_pos + 96, player.y_pos - enemy.y_pos)  # 144 is 3x the width of the player
        if player.mask.overlap(enemy.mask, offset) and attacking:
            enemy.hurt = True
        else:
            enemy.hurt = False

        # text with enemy health
        enemy_health = get_font(30).render(f"Enemy Health: {enemy.health}", True, "Black")
        enemy_health_rect = enemy_health.get_rect(center=(640, 50))
        screen.blit(enemy_health, enemy_health_rect)
        if enemy.health <= 0:
            enemy.health = 0
            enemy.alive = False
            enemy.die()

        py.display.flip()
    py.quit()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return py.font.Font("assets/font.ttf", size)


def options():
    while True:
        OPTIONS_MOUSE_POS = py.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        py.display.update()


def shop(coins, attack_speed_lvl):
    while True:
        OPTIONS_MOUSE_POS = py.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render(f"COINS: {coins}", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(900, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # ATTACK SPEED LEVEL
        attack_s_image = py.image.load("shop/attack_speed_upgrade.png")
        attack_s_image = py.transform.scale_by(attack_s_image, 0.5)
        attack_s_upgrade = Button(image=attack_s_image, pos=(200, 300),
                                  text_input="", font=get_font(75), base_color="Black", hovering_color="Green")
        attack_s_upgrade.update(screen)

        OPTIONS_TEXT = get_font(15).render(f"Current level: {attack_speed_lvl}", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 450))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT = get_font(15).render(f"Upgrade attack speed: cost 10", True, "Red")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(250, 150))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)


        OPTIONS_BACK = Button(image=None, pos=(600, 750),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    # dump values into json file
                    with open("player_data/data.json", "r") as f:
                        player_data = json.load(f)

                    with open("player_data/data.json", "w") as f:
                        player_data["coins"] = coins
                        player_data["attack_speed_lvl"] = attack_speed_lvl
                        json.dump(player_data, f, indent=4)
                    main_menu()

                if attack_s_upgrade.checkForInput(OPTIONS_MOUSE_POS):
                    if coins >= 10:
                        # play AS upgrade sound
                        coin_click_sound = py.mixer.Sound("MP3 Sounds/AS_upgrade.wav")
                        coin_click_sound.set_volume(1.5)
                        coin_click_sound.play()
                        coins -= 10
                        attack_speed_lvl += 1
                    else:
                        # play error sound
                        coin_click_sound = py.mixer.Sound("MP3 Sounds/upgrade_fail.wav")
                        coin_click_sound.set_volume(1.5)
                        coin_click_sound.play()

        py.display.update()


def main_menu():
    # player data

    with open("player_data/data.json", "r") as f:
        player_data = json.load(f)
        # get coins value from json file
        coins = player_data["coins"]
        # get attack speed level from json file
        attack_speed_lvl = player_data["attack_speed_lvl"]

    py.mixer.music.load("MP3 Sounds/main_menu.mp3")
    py.mixer.music.set_volume(0.2)
    py.mixer.music.play(-1)
    main_menu_clock = py.time.Clock()
    main_menu_fps = 60
    bg = py.image.load("assets/Background.png").convert()
    main_menu_bg_width = bg.get_width()
    main_menu_bg_rect = bg.get_rect()
    main_menu_bg_scroll = 0
    main_menu_tiles = ceil(SCREEN_WIDTH / main_menu_bg_width) + 1

    while True:
        main_menu_clock.tick(main_menu_fps)
        # draw scrolling background
        for tile in range(0, main_menu_tiles):
            screen.blit(bg, (tile * main_menu_bg_width + main_menu_bg_scroll, 0))
            main_menu_bg_rect.x = tile * bg_width + main_menu_bg_scroll
            # py.draw.rect(screen, (255, 0, 0), main_menu_bg_rect, 1)

        # scroll background
        main_menu_bg_scroll -= 5
        # reset scroll
        if abs(main_menu_bg_scroll) > main_menu_bg_width:
            main_menu_bg_scroll = 0

        menu_mouse_pos = py.mouse.get_pos()
        game_text_img = py.image.load("assets/game_text.png")
        screen.blit(game_text_img, (
            SCREEN_WIDTH / 2 - game_text_img.get_width() / 2, SCREEN_HEIGHT / 2 - game_text_img.get_height() / 2 - 180))

        play_image = py.image.load("assets/play_button.png")
        play_image = py.transform.scale_by(play_image, 0.7)

        PLAY_BUTTON = Button(image=play_image, pos=(SCREEN_WIDTH / 2, 400),
                             text_input="", font=get_font(25), base_color="#b36b07", hovering_color="Yellow")


        shop_text = py.image.load("shop/text.png")
        shop_text = py.transform.scale_by(shop_text, 0.7)

        SHOP_BUTTON = Button(image=shop_text, pos=(SCREEN_WIDTH / 2, 500),
                             text_input="", font=get_font(25), base_color="#b36b07", hovering_color="Yellow")

        options_image = py.image.load("assets/settings_button.png")
        options_image = py.transform.scale_by(options_image, 0.7)

        OPTIONS_BUTTON = Button(image=options_image, pos=(SCREEN_WIDTH / 2, 600),
                                text_input="", font=get_font(25), base_color="#b36b07", hovering_color="Yellow")

        quit_image = py.image.load("assets/quit_button.png")
        quit_image = py.transform.scale_by(quit_image, 0.7)

        QUIT_BUTTON = Button(image=quit_image, pos=(SCREEN_WIDTH / 2, 700),
                             text_input="", font=get_font(25), base_color="#b36b07", hovering_color="Yellow")

        coin_image = py.image.load("assets/coin.png")
        coin_image = py.transform.scale_by(coin_image, 0.2)

        coin_button = Button(image=coin_image, pos=(1100, 200),
                             text_input="", font=get_font(25), base_color="#b36b07", hovering_color="Yellow")

        for button in [PLAY_BUTTON, SHOP_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, coin_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                    play()
                if SHOP_BUTTON.checkForInput(menu_mouse_pos):
                    # load new values into json file
                    with open("player_data/data.json", "w") as f:
                        player_data["coins"] = coins
                        player_data["attack_speed_lvl"] = attack_speed_lvl
                        json.dump(player_data, f, indent=4)
                    shop(coins, attack_speed_lvl)
                if OPTIONS_BUTTON.checkForInput(menu_mouse_pos):
                    options()
                if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                    py.quit()
                    sys.exit()
                if coin_button.checkForInput(menu_mouse_pos):
                    # play coin click.wav
                    coin_click_sound = py.mixer.Sound("MP3 Sounds/coin_click.wav")
                    coin_click_sound.set_volume(1.5)
                    coin_click_sound.play()
                    coins += 1
        py.display.update()


if __name__ == '__main__':
    main_menu()
