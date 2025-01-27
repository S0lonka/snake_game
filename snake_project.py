from pygame import *
from random import randint
from time import sleep
from math import hypot


#размеры коллизии спрайта и картинки(сделано для удобства в ограничении краёв игрового поля)
picture_height = 40
picture_width  = 40

#класс родитель для спрайта
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, p_x, p_y):
        super().__init__()
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image),(picture_height, picture_width))
        self.speed = speed
        #каждый спрайт должен хранить свойство rect - прямоугольник в который, он вписан
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_height, wall_width, wall_x, wall_y):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.height = wall_height
        self.width = wall_width
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class player(GameSprite):
    def update(self):
        sprite_player.rect.x
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 3:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < window_y - picture_width:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < window_x - picture_height:
            self.rect.x += self.speed


class apple(GameSprite):
    def update(self):
        if sprite.collide_rect(sprite_apple, sprite_player):
            self.rect.x = randint(1, window_x - picture_height)
            self.rect.y = randint(1, window_y - picture_width)
            global score#без global... класс apple не видит переменную score
            score += 1

class enemy(GameSprite):
    def update(self):
        # Вычисление направления
        direction_x = sprite_player.rect.x - sprite_enemy.rect.x
        direction_y = sprite_player.rect.y - sprite_enemy.rect.y
        distance = hypot(direction_x, direction_y)

        if distance > 0:
            direction_x /= distance
            direction_y /= distance

            # Движение врага
            self.rect.x += direction_x * self.speed  # Скорость врага
            self.rect.y += direction_y * self.speed



#цвет фона
background = (200, 5, 100)

#размеры окна
window_x = 900
window_y = 640

#создай окно игры
window = display.set_mode((window_x, window_y))
display.set_caption('snake')

#создание игрового флага
game = True
clock = time.Clock()
fps = 60

sprite_player = player('snake.png', 6, window_x / 2, window_y / 2)
sprite_apple = apple('apple.png', 0, randint(1, window_x - 40), randint(1, window_y - 40) )
sprite_enemy = enemy('enemy.jpg', 4.3, 30, 30)

wall_1 = wall(0,0,0, 10,100, 100, 100)

score = 0

#нужное количество яблок для победы
"костыль, после для каждого уровня это значение разное"
apple_need = 5

#Win\Lose
font.init()
f1 = font.Font(None, 30) 
f2 = font.Font(None, 150)
'''до этого было "font = font.Font(None, 30)" ошибка была в переопределении переменной font
сначала font.init()
потом   font = ...'''

win = f2.render('YOU WIN!', True,(0, 255, 0))
lose = f2.render('YOU LOSE!', True,(100, 0, 0))

#цикл игры
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(background)#чтобы не оставался след спрайта, заливка фона должна быть в цикле и до sprite_player.update()!

    #Функционал спрайтов
    sprite_player.update()
    sprite_apple.update()
    sprite_enemy.update()

    wall_1.draw_wall()

    #надпись YOU SCORE, в цикле для того чтобы обновлять счёт
    score_txt = f1.render(f'YOU SCORE: {score}', True, (0, 0, 0))
    window.blit(score_txt,(750,10))

    #Надпись с нужным количеством яблок для каждого уровня будет своё apple_need
    apple_txt = f1.render(f"apples need:{apple_need}", True, (0, 0, 0))
    window.blit(apple_txt,(10,10))

    #Ситуация победа
    if score == apple_need :
        window.blit(win, (window_x / 5, window_y / 2) )
        '''Нужно чтобы сначала обновился экран( то что снизу"display.update() clock.tick(fps)"
        обновляется экран и появляется надпись, а уже после нужно чтобы флаг менялся на False)'''
        #получилось исправить добавив обновление экрана в условии
        display.update()
        sleep(3)
        game=False
    #ситуация проигрыш
    elif sprite.collide_rect(sprite_enemy, sprite_player) or sprite.collide_rect(sprite_player, wall_1):
        window.blit(lose, (window_x / 5, window_y / 2) )
        display.update()
        sleep(3)
        game=False

    #обновление и отображение спрайтов
    sprite_player.reset()
    sprite_apple.reset()
    sprite_enemy.reset()

    display.update()
    clock.tick(fps)
