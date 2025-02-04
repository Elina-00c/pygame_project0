import pygame
# from pyvidplayer2 import Video
import random

pygame.init()
wight = 830
height = 500
surface = pygame.display.set_mode((wight, height))
pygame.display.set_caption('our game')

icone = pygame.image.load('files/icon.png')
pygame.display.set_icon(icone)

background = pygame.image.load('files/result_a5439e1.jpg')
# sound = pygame.mixer.Sound('files/music.mp3')
dead_img = pygame.image.load('files/dead.png')
dead_img = pygame.transform.scale(dead_img, (int(dead_img.get_width() * 0.1), int(dead_img.get_height() * 0.1)))
coin_image = pygame.image.load('files/coin.png')  # Загружаем изображение монетки
coin_image = pygame.transform.scale(coin_image, (int(coin_image.get_width() * 0.02), int(coin_image.get_height() * 0.02)))
surface.blit(coin_image, (0, 0))
# sound.play(-1)
start_game = False

# vid = Video('files/video.mp4')
# win = pygame.display.set_mode((1280, 720))

tile_size = 30
game_over = False


# def draw_grid():
# for line in range(0, 30):
# pygame.draw.line(surface, (255, 255, 255), (0, line * tile_size), (wight, line * tile_size))
# pygame.draw.line(surface, (255, 255, 255), (line * tile_size, 0), (line * tile_size, height))


class World:
    def __init__(self, data):
        gress_image = pygame.image.load('files/gress.jpg')
        water_image = pygame.image.load('files/water.png')
        self.tile_list = []
        self.coin_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(gress_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(water_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])
            # pygame.draw.rect(surface, (255, 255, 255), tile[1], 2)


word_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 1, 0, 3, 0, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(word_data)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.type = type
        window_size = (827, 500)
        self.screen = pygame.display.set_mode(window_size)

        # Создаем объект шрифта
        font = pygame.font.Font(None, 24)

        # Создайте поверхность для кнопки
        self.button_surface = pygame.Surface((150, 50))

        # Отображение текста на кнопке
        self.text = font.render(self.type, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(
            center=(self.button_surface.get_width() / 2,
                    self.button_surface.get_height() / 2))

        # Создайте объект pygame.Rect, который представляет границы кнопки
        self.button_rect = pygame.Rect(self.x, self.y, 200, 50)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.walk_right = []
        self.walk_left = []
        self.player_anim_count = 0
        self.count = 0
        for i in range(1, 5):
            img_right = pygame.image.load(f'files/player_walk/guy{i}.png')
            img_right = pygame.transform.scale(img_right,
                                               (int(img_right.get_width() * size), int(img_right.get_height() * size)))
            img_left = pygame.transform.flip(img_right, True, False)
            self.walk_right.append(img_right)
            self.walk_left.append(img_left)
        self.image = self.walk_right[self.player_anim_count]
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def move(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.count += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.count += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.count = 0
            self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            if self.direction == -1:
                self.image = self.walk_left[self.player_anim_count]

        if self.count > walk_cooldown:
            self.count = 0
            self.player_anim_count += 1
            if self.player_anim_count >= len(self.walk_right):
                self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            if self.direction == -1:
                self.image = self.walk_left[self.player_anim_count]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        surface.blit(self.image, self.rect)

    def player_dead(self):
        surface.blit(dead_img, (player.rect.x, player.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.animation = []
        self.enemy_rect = [enemy_x, enemy_y]
        self.update_time = pygame.time.get_ticks()
        self.enemy_anim_count = 0
        for i in range(1, 4):
            img = pygame.image.load(f'files/enemy/img{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * size), int(img.get_height() * size)))
            self.animation.append(img)
        self.image = self.animation[self.enemy_anim_count]
        self.rect = self.image.get_rect()

    def draw_enemy(self):
        surface.blit(self.animation[self.enemy_anim_count], self.enemy_rect)

    def animation_enemy(self):
        animation_clock = 125
        if pygame.time.get_ticks() - self.update_time > animation_clock:
            self.update_time = pygame.time.get_ticks()
            self.enemy_anim_count += 1
        if self.enemy_anim_count == len(self.animation):
            self.enemy_anim_count = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.coin_flag = True

    def colision(self):
        if abs(player.rect.x - self.x) < 20 and abs(player.rect.y - self.y < 20):
            self.coin_flag = False

    def draw(self):
        surface.blit(coin_image, (self.x, self.y))


class Bullet(pygame.sprite.Sprite):
    def init(self, x, y):
        pygame.sprite.Sprite.init(self)

    def func(self):
        pass


class HealthBar:
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(surface, (0, 128, 0), (self.x, self.y, 150 * ratio, 20))


class Exit:
    pass


class Title:
    pass


class Level:
    pass


class Barrier:
    pass


player = Player(0, 160, 0.4)
button = Button(315, 150, "Start")
button1 = Button(315, 230, "Exit")
enemy = Enemy(330, 445, 0.05)
enemy1 = Enemy(415, 298, 0.05)
enemy2 = Enemy(580, 298, 0.05)


coin = Coin(250, 450, 5)
coin1 = Coin(150, 450, 5)
coin2 = Coin(426, 220, 5)
coin3 = Coin(516, 247, 5)
coin4 = Coin(779, 98, 5)

clock = pygame.time.Clock()
healthbar = HealthBar(30, 30, 4, 4)

count = 0
running = True
flag = True
while running:
    clock.tick(90)
    # start window
    if not start_game:
        surface.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Вызовите функцию on_mouse_button_down()
                if button.button_rect.collidepoint(event.pos):
                    start_game = True
                elif button1.button_rect.collidepoint(event.pos):
                    running = False
        if button.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button.button_surface, (216, 177, 191), (1, 1, 148, 48))
        else:
            pygame.draw.rect(button.button_surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(button.button_surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(button.button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(button.button_surface, (216, 177, 191), (1, 48, 148, 10), 2)

        button.button_surface.blit(button.text, button.text_rect)
        button.screen.blit(button.button_surface, (button.button_rect.x, button.button_rect.y))

        if button1.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button1.button_surface, (216, 177, 191), (1, 1, 148, 48))
        else:
            pygame.draw.rect(button1.button_surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(button1.button_surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(button1.button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(button1.button_surface, (216, 177, 191), (1, 48, 148, 10), 2)

        button1.button_surface.blit(button1.text, button1.text_rect)
        button1.screen.blit(button1.button_surface, (button1.button_rect.x, button1.button_rect.y))
        pygame.display.update()
    # start window
    else:
        surface.blit(background, (0, 0))

        clock.tick(60)

        surface.blit(background, (0, 0))

        world.draw()
        if coin.coin_flag:
            coin.draw()
        if coin2.coin_flag:
            coin2.draw()
        if coin3.coin_flag:
            coin3.draw()
        if coin4.coin_flag:
            coin4.draw()

        coin.colision()
        coin1.colision()
        coin2.colision()
        coin3.colision()
        coin4.colision()

        healthbar.draw(4)
        if not game_over:
            player.move()
        enemy.draw_enemy()
        enemy1.draw_enemy()
        enemy2.draw_enemy()
        enemy.animation_enemy()
        enemy1.animation_enemy()
        enemy2.animation_enemy()
        if abs(enemy.enemy_rect[0] - player.rect.x < 20) and abs(enemy.enemy_rect[1] - player.rect.y < 20):
            healthbar.draw(0)
            game_over = True
        if abs(enemy1.enemy_rect[0] - player.rect.x < 20) and abs(enemy1.enemy_rect[1] - player.rect.y < 20):
            healthbar.draw(0)
            game_over = True
        if abs(enemy2.enemy_rect[0] - player.rect.x < 20) and abs(enemy2.enemy_rect[1] - player.rect.y < 20):
            healthbar.draw(0)
            game_over = True
        if game_over:
            player.player_dead()

        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            start_game = False
            player.rect.x = 0
            player.rect.y = 160
            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

while pygame.event.wait().type != pygame.QUIT:
    pass

pygame.quit()
