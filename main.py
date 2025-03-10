import pygame
import sys

import module1
import module2

pygame.init()
wight = 830
height = 500
surface = pygame.display.set_mode((wight, height))
pygame.display.set_caption(module1.GAME_NAME)

# Попытка загрузки финального окна
try:
    finale_image = pygame.image.load(module1.FINALE_WINDOW_WAY)
except:
    pass

# Попытка загрузки музыки
try:
    sound = pygame.mixer.Sound(module1.MUSIC_WAY)
except:
    pass

# Попытка загрузки правил игры
try:
    rules = pygame.image.load(module1.RULES_IMAGE_WAY)
except:
    pass

# Попытка загрузки иконки
try:
    icone = pygame.image.load(module1.ICONE_IMAGE_WAY)
    pygame.display.set_icon(icone)
except:
    pass

# Попытка загрузки фона
try:
    background = pygame.image.load(module1.BACK_IMAGE_WAY)
    background1 = pygame.image.load(module1.BACK1_IMAGE_WAY)
    background2 = pygame.image.load(module1.BACK2_IMAGE_WAY)
except:
    # Если файла нет, делаем серый фон
    background = pygame.Surface((wight, height))
    background.fill((50, 50, 50))

# Попытка загрузки изображения при смерти
try:
    dead_img = pygame.image.load(module1.DEAD_IMAGE_WAY)
    dead_img = pygame.transform.scale(dead_img, (int(dead_img.get_width() * 0.16), int(dead_img.get_height() * 0.16)))
except:
    dead_img = pygame.Surface((50, 50))
    dead_img.fill((255, 0, 0))

# Попытка загрузки изображения монетки
try:
    coin_image = pygame.image.load(module1.COIN_IMAGE_WAY)
    coin_image = pygame.transform.scale(
        coin_image,
        (int(coin_image.get_width() * 0.02), int(coin_image.get_height() * 0.02))
    )
except:
    coin_image = pygame.Surface((10, 10))
    coin_image.fill((255, 255, 0))

# Попытка загрузки изображения пули
try:
    bullet_img = pygame.image.load(module1.BULLET_IMAGE_WAY)
    bullet_img = pygame.transform.scale(bullet_img, (10, 5))
except:
    bullet_img = pygame.Surface((10, 5))
    bullet_img.fill((255, 255, 0))

tile_size = 30
game_over = False
start_game = False
clock = pygame.time.Clock()
sound.play(-1)

# Глобальные переменные
current_level = 0
player_health = 3.0
coin_count = 0
door_count = 0
bullets = []
enemies = []
coins = []
door = None
flag_level3 = False
flag_level2 = False
last_bullet_time = 0
bullet_cooldown = 500  # Задержка между выстрелами (мс)
hit_cooldown = 1000  # Задержка между ударами врага (мс)

# Данные уровней
level1_data = module2.level1_data


# ======== Классы ========

class World:
    """
    Класс для представление основного уровня игры
    """

    def __init__(self, data):
        # Пытаемся загрузить текстуры для плит
        try:
            grass_image = pygame.image.load(module1.GRESS_IMAGE_WAY)
        except:
            grass_image = pygame.Surface((tile_size, tile_size))
            grass_image.fill((0, 255, 0))
        try:
            water_image = pygame.image.load(module1.WATER_IMAGE_WAY)
        except:
            water_image = pygame.Surface((tile_size, tile_size))
            water_image.fill((0, 0, 255))
        self.water_list = []
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(water_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.water_list.append(img_rect)
                    self.tile_list.append((img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self):
        """
        Рисуем клетки
        :return:
        """
        for tile in self.tile_list:
            surface.blit(tile[0], tile[1])


class World2:
    """
    Класс для представление второго уровня в игре
    """

    def __init__(self, data):
        # Пытаемся загрузить текстуры для плит
        try:
            grass_image = pygame.image.load(module1.GRESS_IMAGE_WAY)
        except:
            grass_image = pygame.Surface((tile_size, tile_size))
            grass_image.fill((0, 255, 0))
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))


level2_data = module2.level2_data

level3_data = module2.level3_data


class Button(pygame.sprite.Sprite):
    """
    Класс для создания кнопок меню
    """

    def __init__(self, x, y, text_str):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.text_str = text_str
        self.screen = surface
        font = pygame.font.Font(None, 24)
        self.button_surface = pygame.Surface((150, 50))
        self.text = font.render(self.text_str, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(75, 25))
        self.button_rect = pygame.Rect(self.x, self.y, 150, 50)


class Player(pygame.sprite.Sprite):
    """
    Класс основного игрока
    """

    def __init__(self, player_x, player_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.walk_right = []
        self.walk_left = []
        self.player_anim_count = 0
        self.count = 0
        self.direction = 1  # вправо
        for i in range(1, 5):
            try:
                img_right = pygame.image.load(f'files/player_walk/guy{i}.png')
            except:
                img_right = pygame.Surface((50, 50))
                img_right.fill((200, 200, 200))
            img_right = pygame.transform.scale(
                img_right,
                (int(img_right.get_width() * size), int(img_right.get_height() * size))
            )
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
        self.last_hit_time = 0

    def move(self):
        """
        Функция для осуществления движений и анимации персонажа
        :return:
        """
        dx = 0
        dy = 0
        walk_cooldown = 5
        keys = pygame.key.get_pressed()

        # Прыжок
        if keys[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not keys[pygame.K_SPACE]:
            self.jumped = False

        # Движение влево/вправо
        if keys[pygame.K_LEFT]:
            dx -= 5
            self.direction = -1
            self.count += 1
        if keys[pygame.K_RIGHT]:
            dx += 5
            self.direction = 1
            self.count += 1

        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.count = 0
            self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            else:
                self.image = self.walk_left[self.player_anim_count]

        if self.count > walk_cooldown:
            self.count = 0
            self.player_anim_count += 1
            if self.player_anim_count >= len(self.walk_right):
                self.player_anim_count = 0
            if self.direction == 1:
                self.image = self.walk_right[self.player_anim_count]
            else:
                self.image = self.walk_left[self.player_anim_count]

        # Гравитация
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
                else:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy
        surface.blit(self.image, self.rect)

    def player_dead(self):
        """
        Рисуем смерть персонажа
        :return:
        """
        surface.blit(dead_img, (self.rect.x - 15, self.rect.y - 25))


class Enemy(pygame.sprite.Sprite):
    """
    Класс для представления врагов в игре
    """

    def __init__(self, enemy_x, enemy_y, size):
        pygame.sprite.Sprite.__init__(self)
        self.animation = []
        self.update_time = pygame.time.get_ticks()
        self.enemy_anim_count = 0
        for i in range(1, 4):
            try:
                img = pygame.image.load(f'files/enemy/img{i}.png')
            except:
                img = pygame.Surface((30, 30))
                img.fill((255, 0, 255))
            img = pygame.transform.scale(img, (int(img.get_width() * size), int(img.get_height() * size)))
            self.animation.append(img)
        self.image = self.animation[self.enemy_anim_count]
        self.rect = self.image.get_rect(topleft=(enemy_x, enemy_y))
        self.direction = 1
        self.speed = 1
        self.min_x = enemy_x - 10
        self.max_x = enemy_x + 10

    def update_movement(self):
        """
        Движение врагов
        :return:
        """
        self.rect.x += self.speed * self.direction
        if self.rect.x <= self.min_x or self.rect.x >= self.max_x:
            self.direction *= -1

    def draw_enemy(self):
        """
        Рисуем врагов
        :return:
        """
        surface.blit(self.animation[self.enemy_anim_count], self.rect)

    def animation_enemy(self):
        """
        Анимация врагов
        :return:
        """
        animation_clock = 125
        if pygame.time.get_ticks() - self.update_time > animation_clock:
            self.update_time = pygame.time.get_ticks()
            self.enemy_anim_count += 1
        if self.enemy_anim_count >= len(self.animation):
            self.enemy_anim_count = 0


class Coin(pygame.sprite.Sprite):
    """
    Класс для представления монет в игре
    """

    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.coin_flag = True

    def colision(self):
        """
        Проверка столкновений с монетой
        :return:
        """
        global coin_count
        if self.coin_flag and abs(player.rect.x - self.x) < 35 and abs(player.rect.y - self.y) < 35:
            self.coin_flag = False
            coin_count += 1

    def draw(self):
        """
        Рисуем монету
        :return:
        """
        surface.blit(coin_image, (self.x, self.y))


class Bullet(pygame.sprite.Sprite):
    """
    Класс для представления пули от игрока
    """

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction if direction != 0 else 1
        self.speed = 10 * self.direction

    def update(self):
        """
        Движение пули
        :return:
        """
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > wight:
            return False
        return True


class Door(pygame.sprite.Sprite):
    """
    Класс для представления дверей на другие уровни
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(module1.DOOR_IMAGE_WAY)
            self.image = pygame.transform.scale(self.image, (tile_size * 1, tile_size * 1))
        except:
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((150, 75, 0))
        self.rect = self.image.get_rect(topleft=(x + 100, y - 315))

    def draw(self):
        """
        Рисуем дверь
        :return:
        """
        surface.blit(self.image, self.rect)


class HealthBar:
    """
    Класс для представления шкалы здоровья игрока
    """

    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        """
        Рисуем шкалу
        :param health:
        :return:
        """
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(surface, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(surface, (0, 128, 0), (self.x, self.y, 150 * ratio, 20))


healthbar = HealthBar(30, 30, 4, 3)
font = pygame.font.Font(None, 36)


def load_level(level):
    """
    Функция для добалвения уровней в игру
    :param level:
    :return:
    """
    global world, player, enemies, coins, door, current_level, player_health, coin_count, \
        bullets, game_over, flag_level2, flag_level3, door_count
    current_level = level
    door_count = 0
    game_over = False
    bullets = []
    if level == 1:
        world = World(level1_data)
        player.rect.x = 0
        player.rect.y = 160
        door_pos_x = 700  # правая часть экрана
        door_pos_y = 376  # верх
        door = Door(door_pos_x, door_pos_y)
        door_count = 1

        enemies.clear()
        enemies.append(Enemy(330, 445, 0.05))
        enemies.append(Enemy(415, 298, 0.05))
        enemies.append(Enemy(580, 298, 0.05))

        coins.clear()
        coins.append(Coin(250, 450, 5))
        coins.append(Coin(150, 450, 5))
        coins.append(Coin(426, 220, 5))
        coins.append(Coin(516, 247, 5))
        coins.append(Coin(779, 98, 5))

    elif level == 2:
        flag_level2 = True
        surface.blit(background1, (0, 0))
        world = World(level2_data)
        player.rect.x = 0
        player.rect.y = 160
        door_pos_x = 700  # правая часть экрана
        door_pos_y = 380  # верх
        door = Door(door_pos_x, door_pos_y)
        door_count = 2

        enemies.clear()
        enemies.append(Enemy(580, 296, 0.05))
        enemies.append(Enemy(260, 358, 0.05))

        coins.clear()
        coins.append(Coin(250, 370, 5))
        coins.append(Coin(513, 250, 5))
        coins.append(Coin(730, 190, 5))

    elif level == 3:
        flag_level3 = True
        surface.blit(background2, (0, 0))
        world = World(level3_data)
        player.rect.x = 0
        player.rect.y = 160
        door_count = 3
        door = Door(685, 435)

        enemies.clear()
        enemies.append(Enemy(120, 355, 0.05))
        enemies.append(Enemy(565, 298, 0.05))
        enemies.append(Enemy(520, 180, 0.05))

        coins.clear()
        coins.append(Coin(120, 370, 5))
        coins.append(Coin(360, 370, 5))
        coins.append(Coin(760, 190, 5))
        coins.append(Coin(380, 130, 5))
        coins.append(Coin(535, 190, 5))
        coins.append(Coin(543, 40, 5))


# Создаём игрока
player = Player(0, 160, 0.4)
# Загружаем 1-й уровень
load_level(1)


def pause_menu():
    """
    Функция для создания pause menu в игре
    :return:
    """
    paused = True
    global player_health, coin_count, flag_level3, flag_level2, game_over
    resume_button = Button(315, 150, module1.RESUME_BUTTON)
    restart_button = Button(315, 230, module1.RESTART_BUTTON)
    exit_button = Button(315, 310, module1.EXIT_BUTTON)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.button_rect.collidepoint(event.pos):
                    paused = False
                elif restart_button.button_rect.collidepoint(event.pos):
                    player.rect.x = 0
                    player.rect.y = 160
                    player_health = 3.0
                    load_level(1)
                    coin_count = 0
                    flag_level3 = False
                    flag_level2 = False
                    game_over = False
                    paused = False
                elif exit_button.button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        overlay = pygame.Surface((wight, height))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        surface.blit(overlay, (0, 0))

        for btn in [resume_button, restart_button, exit_button]:
            # Проверяем наведение курсора
            if btn.button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(btn.button_surface, (216, 177, 191), (1, 1, 148, 48))
            else:
                pygame.draw.rect(btn.button_surface, (0, 0, 0), (0, 0, 150, 50))
                pygame.draw.rect(btn.button_surface, (255, 255, 255), (1, 1, 148, 48))
                pygame.draw.rect(btn.button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
                pygame.draw.rect(btn.button_surface, (216, 177, 191), (1, 48, 148, 10), 2)

            btn.button_surface.blit(btn.text, btn.text_rect)
            btn.screen.blit(btn.button_surface, (btn.button_rect.x, btn.button_rect.y))

        pygame.display.update()
        clock.tick(60)


start_button = Button(315, 150, module1.START_BUTTON)
exit_button_main = Button(315, 230, module1.EXIT_BUTTON)

finale_window = False
running = True
while running:
    clock.tick(90)
    # проверяем началась ли игра
    if not start_game:
        if finale_window:
            surface.blit(finale_image, (0, 0))
            coin_text = font.render(f"Score: {coin_count} coins", True, (255, 255, 255))
            surface.blit(coin_text, (wight / 2 - 90, height / 2 - 200))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                coin_count = 0
                finale_window = False
        else:
            surface.fill((0, 0, 0))
            surface.blit(rules, (600, 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.button_rect.collidepoint(event.pos):
                        start_game = True
                    elif exit_button_main.button_rect.collidepoint(event.pos):
                        running = False

                        # Рисуем кнопки стартового меню
            for btn in [start_button, exit_button_main]:
                if btn.button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(btn.button_surface, (216, 177, 191), (1, 1, 148, 48))
                else:
                    pygame.draw.rect(btn.button_surface, (0, 0, 0), (0, 0, 150, 50))
                    pygame.draw.rect(btn.button_surface, (255, 255, 255), (1, 1, 148, 48))
                    pygame.draw.rect(btn.button_surface, (0, 0, 0), (1, 1, 148, 1), 2)
                    pygame.draw.rect(btn.button_surface, (216, 177, 191), (1, 48, 148, 10), 2)

                btn.button_surface.blit(btn.text, btn.text_rect)
                btn.screen.blit(btn.button_surface, (btn.button_rect.x, btn.button_rect.y))

        pygame.display.update()

    elif start_game:
        clock.tick(60)
        if not flag_level2 and not flag_level3:
            surface.blit(background, (0, 0))
        elif flag_level3 and not flag_level2:
            surface.blit(background2, (0, 0))
        else:
            surface.blit(background1, (0, 0))
        world.draw()
        door.draw()

        # Монеты
        for c in coins:
            if c.coin_flag:
                c.draw()
            c.colision()

            # Игрок
        if not game_over:
            player.move()

        for enemy in enemies[:]:
            enemy.update_movement()
            enemy.animation_enemy()
            enemy.draw_enemy()
            # Проверка столкновения с игроком
            if player.rect.colliderect(enemy.rect):
                now = pygame.time.get_ticks()
                if now - player.last_hit_time > hit_cooldown:
                    player_health -= (4 / 3)
                    player.last_hit_time = now

            # Проверка попадания пули
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break

            # Пули
        for bullet in bullets[:]:
            if not bullet.update():
                bullets.remove(bullet)
            else:
                surface.blit(bullet.image, bullet.rect)

            # Переход между уровнями (дверь)
        if player.rect.colliderect(door.rect) and door_count == 1:
            if current_level == 1:
                load_level(2)
            else:
                load_level(1)

        if player.rect.colliderect(door.rect) and door_count == 2:
            flag_level2 = False
            if current_level == 2:
                load_level(3)
            else:
                load_level(3)

        if player.rect.colliderect(door.rect) and door_count == 3:
            player.rect.x = 0
            player.rect.y = 160
            player_health = 3.0
            load_level(1)
            flag_level3 = False
            flag_level2 = False
            finale_window = True
            start_game = False

        # Здоровье и монеты
        healthbar.draw(player_health)
        coin_text = font.render(f"Coins: {coin_count}", True, (255, 255, 255))
        surface.blit(coin_text, (wight - 150, 30))

        # Выстрел по кнопке "j"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            now = pygame.time.get_ticks()
            if now - last_bullet_time > bullet_cooldown:
                last_bullet_time = now
                new_bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                bullets.append(new_bullet)

        # Меню паузы по "q"
        if keys[pygame.K_q]:
            pause_menu()

        # Если здоровье <= 0 – смерть
        if player_health <= 0:
            game_over = True
            player.player_dead()

        # Если здоровье > 0, но игрок упал в бездну или воду – смерть
        if player_health > 0 and player.rect.y >= height:
            healthbar.draw(0)
            game_over = True
            player.player_dead()

        # стодкновение с границей экрана
        if player.rect.x > wight:
            player.rect.x = wight
        if player.rect.x < 0:
            player.rect.x = 0

        pygame.display.update()

        # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Завершаем игру
pygame.quit()
sys.exit()
