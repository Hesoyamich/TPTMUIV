import pygame
from tile import Tile
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# random.seed(90)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TILE_GRID = 10
TILE_SIZE = 50
OFFSET_BETWEEN = 0

def rotate_image(img, directions):
    img = pygame.transform.rotate(img, -90)
    new_directions = directions[:]
    new_directions.insert(0, new_directions.pop(-1))
    return (img, new_directions)

def make_rotations(index):
    img_pair = images[index]
    for i in range(3):
        img_pair = rotate_image(img_pair[0], img_pair[1])
        images[max(sorted(images.keys())) + 1] = (img_pair[0], img_pair[1])

def check_reversed(str_1, str_2):
    return str_1 == str_2[::-1]


images = {
    0: (pygame.transform.scale(pygame.image.load("imgs/2/0.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["BBB", "BBB", "BBB", "BBB"]),
    1: (pygame.transform.scale(pygame.image.load("imgs/2/1.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["AAA", "AAA", "AAA", "AAA"]),
    2: (pygame.transform.scale(pygame.image.load("imgs/2/2.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["CCC", "CCC", "CCC", "CCC"]),
    3: (pygame.transform.scale(pygame.image.load("imgs/2/3.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["CCC", "CBB", "BBB", "BBC"]),
    4: (pygame.transform.scale(pygame.image.load("imgs/2/4.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["CCC", "CCC", "CBB", "BBC"]),
    5: (pygame.transform.scale(pygame.image.load("imgs/2/5.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["BBC", "CBB", "BBB", "BBB"]),
    6: (pygame.transform.scale(pygame.image.load("imgs/2/6.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["CCC", "CAA", "AAA", "AAC"]),
    7: (pygame.transform.scale(pygame.image.load("imgs/2/7.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["CCC", "CCC", "CAA", "AAC"]),
    8: (pygame.transform.scale(pygame.image.load("imgs/2/8.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["AAC", "CAA", "AAA", "AAA"]),
    9: (pygame.transform.scale(pygame.image.load("imgs/2/9.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["RRR", "RRR", "RRR", "RRR"]),
    10: (pygame.transform.scale(pygame.image.load("imgs/2/10.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["RRR", "RRA", "AAA", "ARR"]),
    11: (pygame.transform.scale(pygame.image.load("imgs/2/11.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["ARR", "RRA", "AAA", "AAA"]),
    12: (pygame.transform.scale(pygame.image.load("imgs/2/12.png").convert_alpha(), (TILE_SIZE, TILE_SIZE)), ["ARR", "RRA", "AAC", "CAA"])

}



make_rotations(3)
make_rotations(4)
make_rotations(5)
make_rotations(6)
make_rotations(7)
make_rotations(8)
make_rotations(10)
make_rotations(11)




tiles = [[Tile([i for i in range(len(images))], (i, j)) for i in range(TILE_GRID)] for j in range(TILE_GRID)]


rand_x, rand_y = random.randint(0, TILE_GRID - 1), random.randint(0, TILE_GRID - 1)

tiles[rand_y][rand_x].collapse_tile()



def entropy_neighbours(x, y):
    #Вверх
    if 0 <= y - 1 < TILE_GRID:
        if not tiles[y - 1][x].collapsed:
            tiles[y -1][x].possible_tiles = [value for value in tiles[y - 1][x].possible_tiles if check_reversed(images[value][1][2], images[tiles[y][x].tile_index][1][0])]
            # print(tiles[y -1][x].possible_tiles)
            
            
        
    #Вниз
    if 0 <= y + 1 < TILE_GRID:
        if not tiles[y + 1][x].collapsed:

            tiles[y + 1 ][x].possible_tiles = [value for value in tiles[y + 1][x].possible_tiles if check_reversed(images[value][1][0], images[tiles[y][x].tile_index][1][2])]
            # print(tiles[y + 1][x].possible_tiles)

    #Влево
    if 0 <= x + 1 < TILE_GRID:
        if not tiles[y][x + 1].collapsed:
            
            tiles[y][x + 1].possible_tiles = [value for value in tiles[y][x + 1].possible_tiles if check_reversed(images[value][1][3], images[tiles[y][x].tile_index][1][1])]
            # print(tiles[y ][x + 1].possible_tiles)

    #Вправо
    if 0 <= x - 1 < TILE_GRID:
        if not tiles[y][x - 1].collapsed:
            
            tiles[y][x - 1].possible_tiles = [value for value in tiles[y][x - 1].possible_tiles if check_reversed(images[value][1][1], images[tiles[y][x].tile_index][1][3])]
            # print(tiles[y][x - 1].possible_tiles)



entropy_neighbours(rand_x,rand_y)

def make_collapse():
    tilesCopy = []
    for i in tiles:
        tilesCopy += i

    tilesCopy.sort(key= lambda x: len(x.possible_tiles))
    tilesCopy = list(filter(lambda x: not x.collapsed and len(x.possible_tiles) > 0, tilesCopy))
    if len(tilesCopy) > 0:
        tilesCopy[0].collapse_tile()
        entropy_neighbours(tilesCopy[0].pos[0], tilesCopy[0].pos[1])


if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_collapse()

        make_collapse()

        screen.fill("white")

        for y, row in enumerate(tiles):
            for x, col in enumerate(row):
                if col == None or col.tile_index == -1:
                    pygame.draw.rect(screen, (80,80,80), (x * TILE_SIZE + OFFSET_BETWEEN * x, y * TILE_SIZE + OFFSET_BETWEEN * y, TILE_SIZE, TILE_SIZE))
                else:
                    screen.blit(images[col.tile_index][0], (x * TILE_SIZE + OFFSET_BETWEEN * x, y * TILE_SIZE + OFFSET_BETWEEN * y, TILE_SIZE, TILE_SIZE))


        pygame.display.flip()