import pygame
import sys
import os
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
SKY_BLUE = (107, 140, 255)
DARK_BLUE = (20, 20, 60)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Game - 30 Levels")
clock = pygame.time.Clock()

def load_image(name, scale=None):
    try:
        image = pygame.image.load(name).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except:
        surf = pygame.Surface(scale if scale else (32, 32))
        surf.fill(RED)
        return surf

def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except:
        return None

# Текстуры
mario_img = load_image("MARIO.png", (40, 50))
block_img = load_image("block.png", (40, 40))
coin_img = load_image("coin.png", (30, 30))
goomba_img = load_image("monster.png", (40, 40))
thwomp_img = load_image("AHHH.png", (45, 45))
cloud_img = load_image("cloude.png", (80, 50))
flag_img = load_image("flag.png", (30, 30))
stolb_img = load_image("stolb.png", (20, 200))

# Звуки
die_sound = load_sound("mario_die.wav")
jump_sound = load_sound("jump.wav") or load_sound("mario_die.wav")

def play_background_music():
    for m in ["background.mp3", "music.mp3", "mario_theme.mp3"]:
        if os.path.exists(m):
            try:
                pygame.mixer.music.load(m)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                break
            except:
                pass

def show_nintendo_screen():
    original_img = load_image("nintendo.png")
    orig_width, orig_height = original_img.get_size()
    aspect_ratio = orig_width / orig_height if orig_height > 0 else 1
    new_height = 250
    new_width = int(new_height * aspect_ratio)
    
    nintendo_img = pygame.transform.scale(original_img, (new_width, new_height))
    start_time = pygame.time.get_ticks()
    running_logo = True
    
    while running_logo:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running_logo = False

        screen.fill((0, 0, 0))
        rect = nintendo_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(nintendo_img, rect)
        pygame.display.flip()

        if pygame.time.get_ticks() - start_time > 2500:
            running_logo = False

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = mario_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.is_jumping = False
        self.score = 0
        self.lives = 3
        self.is_sliding = False

    def update(self, blocks, coins, enemies, flags):
        if self.is_sliding:
            self.rect.y += 3
            return

        self.vel_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.is_jumping:
            self.vel_y = -15
            self.is_jumping = True
            if jump_sound: jump_sound.play()

        self.vel_y += 0.8
        if self.vel_y > 10: self.vel_y = 10

        self.rect.x += self.vel_x
        for block in pygame.sprite.spritecollide(self, blocks, False):
            if self.vel_x > 0: self.rect.right = block.rect.left
            elif self.vel_x < 0: self.rect.left = block.rect.right

        self.rect.y += self.vel_y
        for block in pygame.sprite.spritecollide(self, blocks, False):
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.is_jumping = False
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom
                self.vel_y = 0

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.is_jumping = False

        for coin in pygame.sprite.spritecollide(self, coins, True):
            self.score += 10

        for enemy in pygame.sprite.spritecollide(self, enemies, False):
            if isinstance(enemy, Goomba):
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= enemy.rect.top + 12:
                    enemy.kill()
                    self.vel_y = -8
                    self.score += 20
                else:
                    self.respawn()
            elif isinstance(enemy, Thwomp):
                self.respawn()

    def respawn(self):
        if die_sound: die_sound.play()
        self.lives -= 1
        self.rect.x = 50
        self.rect.y = 400
        self.vel_x = 0
        self.vel_y = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, distance=100):
        super().__init__()
        self.image = goomba_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.distance = distance
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.distance:
            self.direction *= -1

class Thwomp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = thwomp_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_y = y
        self.min_y = y - 120
        self.max_y = y
        self.state = "rising"
        self.speed = 1.5

    def update(self):
        if self.state == "rising":
            self.rect.y -= self.speed
            if self.rect.y <= self.min_y:
                self.state = "falling"
        elif self.state == "falling":
            self.rect.y += 8
            if self.rect.y >= self.max_y:
                self.rect.y = self.max_y
                self.state = "rising"

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = cloud_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH + random.randint(10, 100)

class Stolb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = stolb_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, is_final=False):
        super().__init__()
        self.image = flag_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_final = is_final

def load_level(level_num, all_sprites, blocks, coins, enemies, clouds, flags):
    for s in blocks: s.kill()
    for s in coins: s.kill()
    for s in enemies: s.kill()
    for s in clouds: s.kill()
    for s in flags: s.kill()
    
    for i in range(4):
        c = Cloud(random.randint(0, SCREEN_WIDTH), random.randint(30, 200))
        clouds.add(c)
        all_sprites.add(c)
        
    bg_color = SKY_BLUE if level_num % 2 != 0 else DARK_BLUE
    
    # Безопасная расстановка платформ ступенками без перекрытия проходов
    b_pos = [
        (200, 420), (240, 420),
        (350, 350), (390, 350),
        (500, 280), (540, 280)
    ]
    
    c_pos = [
        (220, 380), (370, 310), (520, 240)
    ]
    
    if level_num < 30:
        enemies.add(Goomba(300, 460, 80))
        if level_num > 2:
            enemies.add(Thwomp(650, 350))
        
        flag = Flag(750, 470)
        flags.add(flag)
        all_sprites.add(flag)
    else:
        stolb = Stolb(730, 300)
        flag = Flag(730, 300, is_final=True)
        flags.add(flag)
        flags.add(stolb)
        all_sprites.add(stolb)
        all_sprites.add(flag)

    for p in b_pos:
        b = Block(*p)
        blocks.add(b)
        all_sprites.add(b)
    for p in c_pos:
        c = Coin(*p)
        coins.add(c)
        all_sprites.add(c)
    for e in enemies:
        all_sprites.add(e)
        
    return bg_color

def main():
    show_nintendo_screen()
    play_background_music()
    
    checkpoint_level = 1
    current_level = 1

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    flags = pygame.sprite.Group()

    player = Mario(50, 400)
    all_sprites.add(player)

    bg_color = load_level(current_level, all_sprites, blocks, coins, enemies, clouds, flags)
    font = pygame.font.SysFont("Arial", 24)
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clouds.update()
        enemies.update()
        player.update(blocks, coins, enemies, flags)

        for flag in pygame.sprite.spritecollide(player, flags, False):
            if flag.is_final:
                player.is_sliding = True
                screen.fill(bg_color)
                pygame.draw.rect(screen, GREEN, (0, 500, SCREEN_WIDTH, 100))
                all_sprites.draw(screen)
                pygame.display.flip()
                pygame.time.wait(2000)
                
                screen.fill(bg_color)
                win_text = font.render("YOU WIN! THE PRINCESS IS SAVED!", True, WHITE)
                screen.blit(win_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(4000)
                running = False
                break
            else:
                current_level += 1
                checkpoint_level = current_level
                player.rect.x = 50
                player.rect.y = 400
                bg_color = load_level(current_level, all_sprites, blocks, coins, enemies, clouds, flags)

        if player.lives <= 0:
            pygame.mixer.music.stop()
            game_over_text = font.render("GAME OVER", True, RED)
            screen.fill(bg_color)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2500)
            
            checkpoint_level = 1
            current_level = 1
            player.lives = 3
            player.score = 0
            player.rect.x = 50
            player.rect.y = 400
            bg_color = load_level(current_level, all_sprites, blocks, coins, enemies, clouds, flags)
            play_background_music()

        screen.fill(bg_color)
        pygame.draw.rect(screen, GREEN, (0, 500, SCREEN_WIDTH, 100))
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {player.score} | Level: {current_level} (CP: {checkpoint_level})", True, WHITE)
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()