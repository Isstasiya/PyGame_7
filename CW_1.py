import os
import pygame
from random import randrange
import sys


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "Герой двигается",
                  "Карта на месте"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def generate_level(level):
    new_player, x, y, x1, y1 = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x1 = int(x)
                y1 = int(y)
    new_player = Player(x1, y1)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            self.add(evil_group)
        else:
            self.add(good_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if obj.rect.x >= size[0]:
            obj.rect.x = 23
        if obj.rect.y >= size[1]:
            obj.rect.y = 25
        if obj.rect.x < 0:
            obj.rect.x = size[0] - 27
        if obj.rect.y < 0:
            obj.rect.y = size[1] - 27
    
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - size[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - size[1] // 2)



if __name__ == '__main__':
    mapq = input()
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    squ = pygame.USEREVENT + 25
    clock = pygame.time.Clock()
    pygame.time.set_timer(squ, 10)
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    evil_group = pygame.sprite.Group()
    good_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level(mapq))
    camera = Camera()
    start_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.topleft = (player.rect.topleft[0] - tile_width, player.rect.topleft[1])
                    if pygame.sprite.spritecollideany(player, evil_group) or not pygame.sprite.spritecollideany(player, good_group):
                        player.rect.topleft = (player.rect.topleft[0] + tile_width, player.rect.topleft[1])
                if event.key == pygame.K_RIGHT:
                    player.rect.topleft = (player.rect.topleft[0] + tile_width, player.rect.topleft[1])
                    if pygame.sprite.spritecollideany(player, evil_group) or not pygame.sprite.spritecollideany(player, good_group):
                        player.rect.topleft = (player.rect.topleft[0] - tile_width, player.rect.topleft[1])
                if event.key == pygame.K_UP:
                    player.rect.topleft = (player.rect.topleft[0], player.rect.topleft[1] - tile_height)
                    if pygame.sprite.spritecollideany(player, evil_group) or not pygame.sprite.spritecollideany(player, good_group):
                        player.rect.topleft = (player.rect.topleft[0], player.rect.topleft[1] + tile_height)
                if event.key == pygame.K_DOWN:
                    player.rect.topleft = (player.rect.topleft[0], player.rect.topleft[1] + tile_height)
                    if pygame.sprite.spritecollideany(player, evil_group) or not pygame.sprite.spritecollideany(player, good_group):
                        player.rect.topleft = (player.rect.topleft[0], player.rect.topleft[1] - tile_height)
        screen.fill(pygame.Color((0, 0, 0)))
        camera.update(player); 
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
