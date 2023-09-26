import pygame
import opensimplex as simplex
from tile import Tile

import random, csv


pygame.init()
pygame.font.init()

text_font = pygame.font.SysFont("arial", 36)
text_font_2 = pygame.font.SysFont("arial", 8)

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

UP = 1
DOWN = -1
LEFT = -1
RIGHT = 1

GRID_SIZE = 25
WIDTH = SCREEN_WIDTH // GRID_SIZE
HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FEATURE_SIZE = 20

x_coords = random.randint(0, 400)
y_coords = random.randint(0, 400)
simplex.seed(8)

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
    0: (pygame.transform.scale(pygame.image.load("imgs/2/0.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["BBB", "BBB", "BBB", "BBB"]),
    1: (pygame.transform.scale(pygame.image.load("imgs/2/1.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["AAA", "AAA", "AAA", "AAA"]),
    2: (pygame.transform.scale(pygame.image.load("imgs/2/2.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["CCC", "CCC", "CCC", "CCC"]),
    3: (pygame.transform.scale(pygame.image.load("imgs/2/3.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["CCC", "CBB", "BBB", "BBC"]),
    4: (pygame.transform.scale(pygame.image.load("imgs/2/4.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["CCC", "CCC", "CBB", "BBC"]),
    5: (pygame.transform.scale(pygame.image.load("imgs/2/5.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["BBC", "CBB", "BBB", "BBB"]),
    6: (pygame.transform.scale(pygame.image.load("imgs/2/6.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["CCC", "CAA", "AAA", "AAC"]),
    7: (pygame.transform.scale(pygame.image.load("imgs/2/7.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["CCC", "CCC", "CAA", "AAC"]),
    8: (pygame.transform.scale(pygame.image.load("imgs/2/8.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["AAC", "CAA", "AAA", "AAA"]),
    9: (pygame.transform.scale(pygame.image.load("imgs/2/9.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["RRR", "RRR", "RRR", "RRR"]),
    10: (pygame.transform.scale(pygame.image.load("imgs/2/10.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["RRR", "RRA", "AAA", "ARR"]),
    11: (pygame.transform.scale(pygame.image.load("imgs/2/11.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["ARR", "RRA", "AAA", "AAA"]),
    12: (pygame.transform.scale(pygame.image.load("imgs/2/12.png").convert_alpha(), (GRID_SIZE, GRID_SIZE)), ["ARR", "RRA", "AAC", "CAA"])

}

make_rotations(3)
make_rotations(4)
make_rotations(5)
make_rotations(6)
make_rotations(7)
make_rotations(8)
make_rotations(10)
make_rotations(11)

running = True


def generate_noise():
    grid = [[None for i in range(WIDTH)] for _ in range(HEIGHT)]
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2((x + x_coords) / FEATURE_SIZE, (y + y_coords) / FEATURE_SIZE)
            grid[y][x] = value
    
    return grid

def generate_tile_grid(perlin):
    tile_grid = []
    for i, y in enumerate(perlin):
        row = []
        for j, x in enumerate(y):
            if 0.1 > x > 0:
                row.append(Tile([2, 3, 4, 5, 13, 14, 15, 16, 17, 18, 19, 20, 21], (j,i)))
            elif 0.17 > x > 0.1:
                row.append(Tile([2, 6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 30], (j,i)))
            elif 0.5 > x > 0.17:
                row.append(Tile([1,6, 7, 8, 22, 23, 24, 25, 26, 27, 28, 29, 30], (j,i)))
            elif x > 0.5:
                row.append(Tile([1], (j,i)))
            elif x <= 0:
                row.append(Tile([0], (j, i)))
                row[-1].collapse_tile()
        tile_grid.append(row)
    return tile_grid

def shift_tile_coords(x, y):
    for j in tile_grid:
        for i in j:
            i.pos[0] += x
            i.pos[1] += y

def generate_tile_grid_in_line(perlin_line, inrow = True, index = 0):
    row = []
    if inrow:
        for i, value in enumerate(perlin_line):
            if value > 0:
                row.append(Tile(range(1, len(images)), (i,index)))
            elif value <= 0:
                row.append(Tile([0], (i, index)))
                row[-1].collapse_tile()
        print(row)
    else:
        for i, value in enumerate(perlin_line):
            if value > 0:
                row.append(Tile(range(1, len(images)), (index,i)))
            elif value <= 0:
                row.append(Tile([0], (index, i)))
                row[-1].collapse_tile()
    return row

def generate_vertical(grid, direction):
    if direction == UP:
        grid.insert(0, grid.pop(-1))
        for x in range(len(grid[0])):
            value = simplex.noise2((x + x_coords) / FEATURE_SIZE, (y_coords) / FEATURE_SIZE)
            grid[0][x] = value
        tile_grid.pop()
        tile_grid.insert(0, generate_tile_grid_in_line(grid[0], True, 0))
    if direction == DOWN:
        grid.append(grid.pop(0))
        for x in range(len(grid[0])):
            value = simplex.noise2((x + x_coords) / FEATURE_SIZE, (y_coords + len(grid) - 1) / FEATURE_SIZE)
            grid[-1][x] = value
    
        tile_grid.pop(0)
        tile_grid.append(generate_tile_grid_in_line(grid[-1], True, -1))
    return grid

def generate_horizontal(grid, direction):
    if direction == LEFT:
        tile_line = []
        for i, y in enumerate(grid):
            y.insert(0, y.pop())
            value = simplex.noise2((x_coords) / FEATURE_SIZE, (y_coords + i) / FEATURE_SIZE)
            grid[i][0] = value
            tile_line.append(value)
        tile_line = generate_tile_grid_in_line(tile_line, False, 0)
        for i, y in enumerate(tile_line):
            tile_grid[i].pop()
            tile_grid[i].insert(0, y) 
    if direction == RIGHT:
        tile_line = []
        for i, y in enumerate(grid):
            y.append(y.pop(0))
            value = simplex.noise2((x_coords + len(grid[0]) - 1) / FEATURE_SIZE, (y_coords + i) / FEATURE_SIZE)
            grid[i][-1] = value
            tile_line.append(value)
        tile_line = generate_tile_grid_in_line(tile_line, False, -1)
        for i, y in enumerate(tile_line):
            tile_grid[i].pop(0)
            tile_grid[i].append(y) 
    return grid



def entropy_neighbours(x, y, tile_grid):
    #Вверх
    if 0 <= y - 1 < HEIGHT:
        print(x, y)
        if not tile_grid[y - 1][x].collapsed:
            tile_grid[y -1][x].possible_tiles = [value for value in tile_grid[y - 1][x].possible_tiles if check_reversed(images[value][1][2], images[tile_grid[y][x].tile_index][1][0])]  
        
    #Вниз
    if 0 <= y + 1 < HEIGHT:
        print(x, y)
        if not tile_grid[y + 1][x].collapsed:
            tile_grid[y + 1 ][x].possible_tiles = [value for value in tile_grid[y + 1][x].possible_tiles if check_reversed(images[value][1][0], images[tile_grid[y][x].tile_index][1][2])]

    #Влево
    if 0 <= x + 1 < WIDTH:
        if not tile_grid[y][x + 1].collapsed:
            tile_grid[y][x + 1].possible_tiles = [value for value in tile_grid[y][x + 1].possible_tiles if check_reversed(images[value][1][3], images[tile_grid[y][x].tile_index][1][1])]

    #Вправо
    if 0 <= x - 1 < WIDTH:
        if not tile_grid[y][x - 1].collapsed:
            tile_grid[y][x - 1].possible_tiles = [value for value in tile_grid[y][x - 1].possible_tiles if check_reversed(images[value][1][1], images[tile_grid[y][x].tile_index][1][3])]

def entropy_collapsed(tile_grid):
    for y, row in enumerate(tile_grid):
        for x, col in enumerate(row):
            if col.collapsed:
                print(col.collapsed)
                entropy_neighbours(x, y, tile_grid)

def make_collapse():
    tilesCopy = []
    for i in tile_grid:
        tilesCopy += i

    tilesCopy.sort(key= lambda x: len(x.possible_tiles))
    tilesCopy = list(filter(lambda x: not x.collapsed and len(x.possible_tiles) > 0, tilesCopy))
    if len(tilesCopy) > 0:
        tilesCopy[0].collapse_tile()
        entropy_neighbours(tilesCopy[0].pos[0], tilesCopy[0].pos[1], tile_grid)
        return True
    else:
        return False

def write_data(perlin, tiles):
    with open("data.csv", 'w', encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        # Вписываем заголовок
        writer.writerow(("perlin_value", 'selected_tile', 'x', 'y', 'collaped', 'possible_tiles'))
        for i in range(len(perlin)):
            for j in range(len(perlin[0])):
                tile = tiles[i][j]
                writer.writerow((perlin[i][j], tile.tile_index, tile.pos[0], tile.pos[1], tile.collapsed, len(tile.possible_tiles)))

perlin = generate_noise()
tile_grid = generate_tile_grid(perlin)
entropy_collapsed(tile_grid)


if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    write_data(perlin, tile_grid)
                if event.key == pygame.K_UP:
                    y_coords -= 1
                    shift_tile_coords(0, -1)
                    perlin = generate_vertical(perlin, UP)
                if event.key == pygame.K_DOWN:
                    shift_tile_coords(0, 1)
                    y_coords += 1
                    perlin = generate_vertical(perlin, DOWN)
                if event.key == pygame.K_LEFT:
                    shift_tile_coords(-1, 0)
                    x_coords -= 1
                    perlin = generate_horizontal(perlin, LEFT)
                if event.key == pygame.K_RIGHT:
                    shift_tile_coords(1, 0)
                    x_coords += 1
                    perlin = generate_horizontal(perlin, RIGHT)
        while make_collapse():
            pass
        

        screen.fill("white")
        for i, y in enumerate(perlin[1:-1]):
            for j, x in enumerate(y[1:-1]):
                if 0.1 > x > 0:
                    pygame.draw.rect(screen, (255,255,0), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if 0.17 > x > 0.1:
                    pygame.draw.rect(screen, (128,128,0), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if 0.5 > x > 0.17:
                    pygame.draw.rect(screen, (0,255,0), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if x > 0.5:
                    pygame.draw.rect(screen, (128,128,128), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if x <= 0:
                    pygame.draw.rect(screen, (0,0,255), (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        for i, y in enumerate(tile_grid[1:-1]):
            for j, x in enumerate(y[1:-1]):
                if x.collapsed:
                    screen.blit(images[x.tile_index][0], (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    

        

        
        x_coords_text = text_font.render(f"X: {x_coords}", True, (255,255,255))
        screen.blit(x_coords_text, (10, 50))
        y_coords_text = text_font.render(f"Y: {y_coords}", True, (255,255,255))
        screen.blit(y_coords_text, (10, 100))


        pygame.display.flip()
