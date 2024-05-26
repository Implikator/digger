import pygame, time
from random import randint

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Копатель 2D")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

back_photo = pygame.image.load('images/Background.jpg').convert()
screen.blit(back_photo, (0, 0))




player_left = pygame.image.load('images/HitLeft/Hitleft1.png').convert_alpha()



game_hit_left = [
    pygame.image.load('images/HitLeft/Hitleft1.png').convert_alpha(),
    pygame.image.load('images/HitLeft/Hitleft2.png').convert_alpha(),
    pygame.image.load('images/HitLeft/Hitleft3.png').convert_alpha(),
    pygame.image.load('images/HitLeft/Hitleft4.png').convert_alpha()
]
game_hit_right = [
    pygame.image.load('images/hitRight/Hitright1.png').convert_alpha(),
    pygame.image.load('images/hitRight/Hitright2.png').convert_alpha(),
    pygame.image.load('images/hitRight/Hitright3.png').convert_alpha(),
    pygame.image.load('images/hitRight/Hitright4.png').convert_alpha()
]
game_run_left = [
    pygame.image.load('images/runLeft/runLeft1.png').convert_alpha(),
    pygame.image.load('images/runLeft/runLeft2.png').convert_alpha(),
    pygame.image.load('images/runLeft/runLeft3.png').convert_alpha()
]
game_run_right = [
    pygame.image.load('images/rulRight/runRight1.png').convert_alpha(),
    pygame.image.load('images/rulRight/runRight1.png').convert_alpha(),
    pygame.image.load('images/rulRight/runRight1.png').convert_alpha()
]
# player = pygame.transform.scale(player, (1024, 768)) #Изменение размера фото


def life(life_counter):
    full_heart = pygame.image.load('images/lifeCount/fullHeart.png').convert_alpha()
    half_heart = pygame.image.load('images/lifeCount/halfHeart.png').convert_alpha()
    empty_heart = pygame.image.load('images/lifeCount/emptyHeart.png').convert_alpha()

    if life_counter == 3:
        screen.blit(full_heart, (980, 20))
        screen.blit(full_heart, (980 + 60, 20))
        screen.blit(full_heart, (980 + 60*2, 20))
    elif life_counter == 2:
        screen.blit(full_heart, (980, 20))
        screen.blit(full_heart, (980 + 60, 20))
        screen.blit(empty_heart, (980 + 60 * 2, 20))
    elif life_counter == 1:
        screen.blit(full_heart, (980, 20))
        screen.blit(empty_heart, (980 + 60, 20))
        screen.blit(empty_heart, (980 + 60 * 2, 20))
    elif life_counter == 0:
        screen.blit(empty_heart, (980, 20))
        screen.blit(empty_heart, (980 + 60, 20))
        screen.blit(empty_heart, (980 + 60 * 2, 20))



def ground_lines(counter_ground_x, counter_ground_y, ground_broken, fire_area):
    fire = pygame.image.load('images/fire.png').convert_alpha() #Создание огня
    ground = pygame.image.load('images/fossils/ground.PNG').convert_alpha() #Создание блока земли
    size_ground_x = 60
    size_ground_y = 53
    gr_x = 0
    gr_y = 120
    for i in range(counter_ground_y):
        for j in range(counter_ground_x):
            if j + i * counter_ground_x in fire_area:
                screen.blit(fire, (gr_x, gr_y))
            if j + i * counter_ground_x in ground_broken: #Проверка на уничтоженный блок земли
                gr_x += size_ground_x
                continue
            screen.blit(ground, (gr_x, gr_y))
            gr_x+=size_ground_x
        gr_x = 0
        gr_y+= size_ground_y

def fire_create(level):
    fire_set = set()
    if level == 1:
        while len(fire_set) != 30:
            fire_set.add(randint(0, 20*13))
    if level == 2:
        fire_set = set()
        while len(fire_set) != 40:
            fire_set.add(randint(0, 20*13))
    if level == 3:
        fire_set = set()
        while len(fire_set) != 60:
            fire_set.add(randint(0, 20*13))

    return list(fire_set)

def level_counter(level):
    if level == 1:
        level_photo = pygame.image.load('images/levelList/level1.png')
        level_photo = pygame.transform.scale(level_photo, (135, 63))
        screen.blit(level_photo, (20, 8))
    if level == 2:
        level_photo = pygame.image.load('images/levelList/level2.png')
        level_photo = pygame.transform.scale(level_photo, (135, 63))
        screen.blit(level_photo, (20, 8))
    if level == 3:
        level_photo = pygame.image.load('images/levelList/level3.png')
        level_photo = pygame.transform.scale(level_photo, (135, 63))
        screen.blit(level_photo, (20, 8))

pl_x = 490
pl_y = 65
screen.blit(player_left, (pl_x, pl_y))

speed_x = 60
speed_y = 53

level = 1

fire_area = fire_create(level)
life_counter = 3 #Счетчик для жизней
ground_broken = [] #Список разбитых блоков


running = True

while running:
    ground_lines(20, 13, ground_broken, fire_area)

    life(life_counter)

    screen.blit(player_left, (pl_x, pl_y)) #Аимация удара в левую сторону
    level_counter(level)

    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]: #Анимация копания вниз
        for i in range(4):
            screen.blit(game_hit_left[i], (pl_x, pl_y))
            pygame.display.update()
            screen.blit(back_photo, (0, 0))
            ground_broken.append(pl_x // speed_x + (pl_y//speed_y - 1)*20) # Уничтоженный блок
            ground_lines(20, 13, ground_broken, fire_area)
            life(life_counter)
            level_counter(level)
            pl_y += speed_y/4
            clock.tick(10)
        if (pl_x // speed_x + (pl_y//speed_y - 2)*20) in fire_area: #Проверка на попадание в огонь
            life_counter-=1
            fire_area.remove(pl_x // speed_x + (pl_y//speed_y - 2)*20)
            pygame.display.update()
            screen.blit(back_photo, (0, 0))



    if keys[pygame.K_a]: #Анимация движения влево
        if (pl_x // 60 - 1 + (pl_y // speed_y - 1) * 20 - 20) not in ground_broken and (pl_y != 65):
            for j in range(4):
                if pl_x <= 10:
                    break
                screen.blit(game_hit_left[j], (pl_x, pl_y))
                pygame.display.update()
                screen.blit(back_photo, (0, 0))
                ground_broken.append(pl_x // 60 - 1 + (pl_y // speed_y - 1) * 20 - 20)
                ground_lines(20, 13, ground_broken, fire_area)
                life(life_counter)
                level_counter(level)
                clock.tick(10)
        for i in range(3): #Проверка на стену
            if pl_x <= 10:
                break
            screen.blit(game_run_left[i], (pl_x, pl_y))
            pygame.display.update()
            screen.blit(back_photo, (0, 0))
            ground_lines(20, 13, ground_broken, fire_area)
            life(life_counter)
            level_counter(level)
            pl_x -= speed_x/3
            clock.tick(10)
        if (pl_x // speed_x + (pl_y//speed_y - 2)*20) in fire_area: #Проверка на попадание в огонь
            life_counter-=1
            fire_area.remove(pl_x // speed_x + (pl_y//speed_y - 2)*20)
            pygame.display.update()
            screen.blit(back_photo, (0, 0))

    if keys[pygame.K_d]: #Анимация движения вправо
        if (pl_x // 60 + 1 + (pl_y // speed_y - 1) * 20 - 20) not in ground_broken and (pl_y != 65):
            for j in range(4):
                if pl_x >= 1140:
                    break
                screen.blit(game_hit_right[j], (pl_x, pl_y))
                pygame.display.update()
                screen.blit(back_photo, (0, 0))
                ground_broken.append(pl_x // 60 + 1 + (pl_y // speed_y - 1) * 20 - 20)
                ground_lines(20, 13, ground_broken, fire_area)
                life(life_counter)
                level_counter(level)
                clock.tick(10)
        for i in range(3): #Проверка на стену
            if pl_x >= 1140:
                break
            screen.blit(game_run_right[i], (pl_x, pl_y))
            pygame.display.update()
            screen.blit(back_photo, (0, 0))
            ground_lines(20, 13, ground_broken, fire_area)
            life(life_counter)
            level_counter(level)
            pl_x += speed_x/3
            clock.tick(10)

        if (pl_x // speed_x + (pl_y//speed_y - 2)*20) in fire_area: #Проверка на попадание в огонь
            life_counter -= 1
            fire_area.remove(pl_x // speed_x + (pl_y//speed_y - 2)*20)
            pygame.display.update()
            screen.blit(back_photo, (0, 0))



    if life_counter == 0:  # Проверка на смерть
        game_over = pygame.image.load('images/GameIvent/GameOver.PNG').convert()
        screen.blit(game_over, (0, 0))
        pygame.display.update()
        time.sleep(3)

        level = 1

        fire_area = fire_create(level)
        pl_x = 490
        pl_y = 65
        screen.blit(back_photo, (0, 0))
        screen.blit(player_left, (pl_x, pl_y))
        life_counter = 3  # Счетчик для жизней
        ground_broken = []  # Список разбитых блоков
        pygame.display.update()


    if pl_y > 750:
        print(level)
        level += 1
        if level > 3: #Проверка на победу
            game_win = pygame.image.load('images/GameIvent/GameWin.PNG').convert()
            screen.blit(game_win, (0, 0))
            pygame.display.update()
            time.sleep(3)

            level = 1

            fire_area = fire_create(level)
            pl_x = 490
            pl_y = 65
            screen.blit(back_photo, (0, 0))
            screen.blit(player_left, (pl_x, pl_y))
            life_counter = 3  # Счетчик для жизней
            ground_broken = []  # Список разбитых блоков
            pygame.display.update()


        else: #Проверка на следующий уровень
            level_up = pygame.image.load('images/GameIvent/LevelUp.PNG').convert()
            screen.blit(level_up, (0, 0))
            pygame.display.update()
            time.sleep(3)

            fire_area = fire_create(level)
            pl_x = 490
            pl_y = 65
            screen.blit(back_photo, (0, 0))
            screen.blit(player_left, (pl_x, pl_y))
            life_counter = 3  # Счетчик для жизней
            ground_broken = []  # Список разбитых блоков
            pygame.display.update()







    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()



    clock.tick(20)

