import pygame
import os
import sys
import random

pygame.init()  # инициализирую pygame
SIZE = 550, 400  # размеры экрана начального окна
SIZE_GAME = WIDTH, HEIGHT = 708, 472  # размеры окна игры
screen = pygame.display.set_mode(SIZE)
screen.fill((0, 0, 0))
pygame.mixer.init()  # инициализирую класс звука mixer(без аудиоустройства будет ошибка)
pygame.mixer.set_num_channels(10)  # устанавливаю кол-во каналов
music = pygame.mixer.Sound(file='data/cosmo music1.wav')  # музыка игры
music_channel = pygame.mixer.Channel(0)  # создание канала музыки


def terminate():  # функция выхода из потока(и из игры)
    sys.exit()


def start_screen():  # функция начального экрана
    global cursor_group  # устанавливая глобальную переменную, чтобы исп. в других функциях
    intro_text = ["Новая Игра",  # текст кнопок
                  "Выйти"]
    fon = load_image('Start fon.png')  # фон
    font = pygame.font.SysFont('Times New Roman', 40)  # 1 шрифт
    font_for_winners = pygame.font.SysFont('Times New Roman', 20)  # шрифт для списка победителей
    text_coord = 90  # отступ по y для текста
    text_coords = [30, 60, 90]  # отступ по y для списка победителей
    cursor_group = pygame.sprite.Group()  # группа только для курсора
    cursor = Cursor(cursor_group)  # создаю экземпляр курсора
    all_sprites = pygame.sprite.Group()
    winners = ['', '', '']  # список победителей по умалчанию
    player_index = 0  # индекс победителя
    music_channel.play(music, loops=-1)  # начинаю музыка с бесконечным кол-вом повторов
    with open('data/results.txt', 'r', encoding='utf8') as results:  # открываю фаул с победителями
        for line in results.readlines():  # в файл может быть пуст или нет
            if player_index == 3:  # но мне нужны только первые трое
                break
            else:
                winners[player_index] = line.split(': ')[0]  # победитель и время разделены ': '
            player_index += 1
    for line in intro_text:  # создаю классы текста(класс потому что проверяю коллизию текста и мыши)
        string_rendered = font.render(line, 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30  # увеличиваю отступ по y
        intro_rect.top = text_coord
        intro_rect.x = 210
        text_coord += intro_rect.height
        Text(string_rendered, intro_rect, all_sprites)
    while True:  # бесконечный цикл
        screen = pygame.display.set_mode(SIZE)  # ещё раз меняю размеры для случая повторной игры
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))  # накладываю фон
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in {1, 2, 3}:  # если это нажатие, а не кручение колёсика
                    collide_state = pygame.sprite.spritecollideany(cursor, all_sprites)  # коллизия кнопки и курсора
                    number = 0  # номер кнопки
                    if collide_state:
                        for rectangle in all_sprites:  # цикл для нахождения кнопки
                            if rectangle == collide_state:
                                break
                            number += 1
                        if number == 0:  # если 'начать игру'
                            pygame.key.set_repeat(1, 100)  # устанавливаю повтор клавиш(для ввода ника медленнее)
                            nick, font1 = Foreword(fon, font)  # функция заставки
                            minutes, seconds = Game(fon, font, cursor, cursor_group, font1)  # фукнция игры, основная
                            End(fon, font1, nick, str(minutes), str(seconds))  # функция конца
                            player_index = 0
                            with open('data/results.txt', 'r', encoding='utf8') as results:  # смотрю обновились ли
                                for line in results.readlines():  # результаты
                                    if player_index == 3:
                                        break
                                    else:
                                        winners[player_index] = line.split(': ')[0]
                                    player_index += 1
                        else:
                            terminate()
            if event.type == pygame.MOUSEMOTION:  # изменяю позицию мыши при движении
                cursor.move(*event.pos)
        screen.blit(font_for_winners.render('Победители:', 1, pygame.Color('White')), (20, 0))  # надпись Победители
        for i in range(3):  # рисую список победителей
            screen.blit(font_for_winners.render(f'{i + 1}. {winners[i]}', 1, pygame.Color('White')),
                        (20, text_coords[i]))
        screen.blit(pygame.transform.scale(load_image('star.png'), (20, 20)), (0, 30))  # картинка рекордсмена
        all_sprites.draw(screen)  # рисую всё
        pygame.display.flip()  # обновляю экран


def Foreword(fon, font):  # принимаю, чтобы не делать новые и не засорять память
    global screen  # т. к. буду изменять глобальный экран
    nickname = ''  # ник игрока
    font1 = pygame.font.SysFont('Times New Roman', 30)
    screen = pygame.display.set_mode((WIDTH + 25, HEIGHT))  # спец. размеры для текста
    text = ['     "А? Что? Где Я?" - таковы ваши ',  # относительно хорошее начало сюжета
            'первые слова когда вы очнулись.',
            'Вы пытаетесь подняться. Вам очень тяжело,',
            'но вы смогли поднять туловище.',
            'Вы пытаетесь напрячь голову, что-то вспомнить -',
            'боль, невыносимая боль.',
            'Вы что-то припоминаете - "Да!"',
            '     Вдруг до вас донёсся душераздирающий звук -',
            'Вам страшно. Вы протираете глаза, всё ещё слепнувшие.',
            'Осматриваетесь и понимаете, что вы в космосе ',
            'на космическом корабле. Вы встаёте и',
            'видите рядом переносную батарею.',
            'Взяв её, вы побежали от источника звука, но вы '
            'не знаете, что вас ждёт на пути к спасению.',
            'Вам предстоит через многое пройти,',
            'чтобы выбраться из этого гиблого места.']
    text_coord = 370  # сначала текст должен быть ниже экрана по y
    all_sprites = pygame.sprite.Group()
    tell_foreword = False  # начать рассказ истории или нет
    MOVE_TEXT = 28  # id события движени текста
    for line in text:  # опять заполняю all_sprites классами строк
        foreword_line = font1.render(line, 1, pygame.Color('White'))
        foreword_rect = foreword_line.get_rect()
        text_coord += 30
        foreword_rect.top = text_coord
        foreword_rect.x = 5
        text_coord += foreword_rect.height
        Text(foreword_line, foreword_rect, all_sprites)
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not tell_foreword:
                if event.type == pygame.KEYDOWN:  # если нажата клавиша
                    if event.key != pygame.K_BACKSPACE:  # если 'убрать' - то символ удаляется
                        if event.key == pygame.K_RETURN:  # ввод ника
                            tell_foreword = True  # теперь можно показать начало сюжета
                            pygame.time.set_timer(MOVE_TEXT, 40)  # таймер движения текста
                        else:
                            if len(nickname) < 10:  # не больше 10 символов
                                nickname = nickname + pygame.key.name(event.key)
                    else:
                        if nickname:  # если есть сиволы
                            nickname = nickname[:-1]
            else:
                if event.type == MOVE_TEXT:  # событие движения текста
                    pygame.time.set_timer(MOVE_TEXT, 40)
                    all_sprites.update()

        if not tell_foreword:  # экран ника
            screen.blit(font.render('Введите ник:', 1, pygame.Color('White')), (20, 200))
            screen.blit(font.render(nickname.capitalize(), 1, pygame.Color('White')), (260, 200))
        else:  # рисую экран сюжета
            all_sprites.draw(screen)
        pygame.display.flip()
        if all_sprites.sprites()[-1].rect.bottom < 0:  # если весь текст прокрутился, то начать игру
            return nickname.capitalize(), font1  # возвращаю фон и ник


def End(fon, font, nick, minutes, seconds):  # фон для текста, ник и время для записи в файл
    global screen
    screen = pygame.display.set_mode((WIDTH + 25, HEIGHT))
    text = ['Когда вы вошли в портал, то вокруг вас',
            'всё закружилось, начало переливаться красками.',
            'Потом темнота, голова раскалывается.',
            'Вы открываете глаза и видите голубой фон.',
            'Это небо. "Небо? Я на Земле!?" - подумали вы',
            'и уже со счастливым лицом встаёте и видите',
            'близкие сердцу места.',
            'Увидев всё это вы смиряетесь со своим',
            'прошлым и отпускаете его, чтобы начать',
            'новую беззаботною и радостную жизнь.',
            '',
            '',
            '',
            f'   Поздравляю {nick}. Вы победили!',
            f'   Время игры: {minutes}:{seconds}']
    text_coord = 370
    all_sprites = pygame.sprite.Group()
    MOVE_TEXT = 28
    pygame.time.set_timer(MOVE_TEXT, 40)
    with open('data/results.txt', 'r', encoding='utf8') as results:  # открываю файл
        list_of_winners = list(  # список победителей
            map(lambda x: (x[0], int(x[1])), map(lambda line: line.split(': '), results.readlines())))
    list_of_winners.append(
        (nick, int(minutes + seconds)))  # добавляю нового победителя(ник и время(как сложение строк))
    list_of_winners.sort(key=lambda x: x[1])  # сортировка по времени
    with open('data/results.txt', 'w', encoding='utf8') as results:  # открываю файл для записи новых данных
        for line in list(map(lambda x: (x[0], str(x[1])), list_of_winners)):
            results.write(': '.join(line) + '\n')
    for line in text:  # добавление текста в группу классов
        foreword_line = font.render(line, 1, pygame.Color('White'))
        foreword_rect = foreword_line.get_rect()
        text_coord += 30
        foreword_rect.top = text_coord
        foreword_rect.x = 30
        text_coord += foreword_rect.height
        Text(foreword_line, foreword_rect, all_sprites)
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == MOVE_TEXT:
                pygame.time.set_timer(MOVE_TEXT, 40)
                all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        if all_sprites.sprites()[-1].rect.bottom < 0:  # если текст закончился, то завершить функцию
            return


def Game(fon, font, cursor, cursor_group, font1):  # игра принимает курсор, группу курсора
    global lose, win, movement, level_number, new_game, state, kill_count, pause_state \
        , move_cam_like_video, kill_sprite, draw_frame_group, new_level  # глобальные т. к. будут изменяться
    # создание id таймеров и их приостановка(если повторная игра)
    FRAME_TIME = 20  # для фиол. шариков
    pygame.time.set_timer(FRAME_TIME, 0)
    FRAME_TIME2 = 22  # для маленьких оранжевых
    pygame.time.set_timer(FRAME_TIME2, 0)
    ENERGY_ACCUMULATION_EVENT = 26  # для события перезарядки аккумулятора
    pygame.time.set_timer(ENERGY_ACCUMULATION_EVENT, 0)
    ENERGY_GIVING_EVENT = 27  # событие вырабатывания энергии
    pygame.time.set_timer(ENERGY_GIVING_EVENT, 0)
    ENEMY_TIME = 30  # появление врага
    ALIEN_MOVE = 21  # движение врага
    BOSS_SHOOT = 19  # атака босса
    pygame.time.set_timer(BOSS_SHOOT, 0)
    BOSS_CHOICE = 18  # движение босса(рандомный алгоритм)
    pygame.time.set_timer(BOSS_CHOICE, 0)
    PORTAL_TIME = 16  # изменение фрейма портала
    SECOND_TIME = 15  # секундомер
    clock = pygame.time.Clock()
    dark_souls = pygame.mixer.Sound(file='data\DarkSouls.wav')  # отдельный звук в игре(смерть игрока)
    dark_souls_channel = pygame.mixer.Channel(1)  # на следующей строке канал, по которому пойдёт звук
    turret_sound = pygame.mixer.Sound(file='data/big shot12.wav')  # выстрел обычной турели
    turret_sound.set_volume(0.5)
    turret_sound_channel = pygame.mixer.Channel(2)
    defense_turret_sound = pygame.mixer.Sound(file='data/small shot.wav')  # выстрел защитной турели
    defense_turret_sound_channel = pygame.mixer.Channel(3)
    alien_death_sound = pygame.mixer.Sound(file='data/alien_death.wav')  # звук умирания пришельца
    alien_death_sound_channel = pygame.mixer.Channel(4)
    destroy_sound = pygame.mixer.Sound(file='data/building_destroy1.wav')  # звук разрушения постройки
    destroy_sound_channel = pygame.mixer.Channel(5)
    alien_attack_sound = pygame.mixer.Sound(file='data/big shot1.wav')  # звук атаки пришельца
    alien_attck_sound_channel = pygame.mixer.Channel(6)
    charging_sound = pygame.mixer.Sound(file='data/charging.wav')  # звук выработки энергии
    charging_sound.set_volume(0.5)
    charging_sound_channel = pygame.mixer.Channel(7)
    boss_attack_sound = pygame.mixer.Sound(file='data/enemy_shoot.wav')  # звук атаки босса
    boss_attack_sound_channel = pygame.mixer.Channel(8)
    boss_death_sound = pygame.mixer.Sound(file='data/robot death.wav')  # звук смерти босса
    boss_death_sound_channel = pygame.mixer.Channel(9)
    # группы спрайтов
    new_game_all_sprites = pygame.sprite.Group()  # группа спрайтов не перемещающихся при анимации камеры
    turret_group = pygame.sprite.Group()  # группа турелей
    floor_group = pygame.sprite.Group()  # группа поля
    player_group = pygame.sprite.Group()  # группа игрока
    bullet_group = pygame.sprite.Group()  # группа пуль игрока
    alien_group = pygame.sprite.Group()  # группа пришельцев
    defense_turret_group = pygame.sprite.Group()  # группа защитных турелей
    bullets = pygame.sprite.Group()  # группа всех пуль
    frame_group = pygame.sprite.Group()  # группа окна построки
    object_group = pygame.sprite.Group()  # объекты окна постройки
    battery_group = pygame.sprite.Group()  # группа генераторов
    buildings_group = pygame.sprite.Group()  # группа построек
    border_group = pygame.sprite.Group()  # группа границ
    end_of_cam_group = pygame.sprite.Group()  # группа границ перемещения камеры
    arrow_group = pygame.sprite.Group()  # группа стрелки направления к выходу
    boss_group = pygame.sprite.Group()  # группа босса
    enemy_bullets = pygame.sprite.Group()  # группа вражеских пуль
    portal_group = pygame.sprite.Group()  # группа портала
    cd_for_turret = (23, 12000)  # id и время события обновления постройки турели
    cd_for_def_turret = (24, 24000)  # id и время события обновления постройки защитной турели
    cd_for_battery = (25, 8000)  # id и время события обновления постройки генератора
    draw_frame_group = False  # переменная рисования окна постройки
    FPS = 60
    enemy_count = 0  # кол-во противников
    movement = 150  # время таймера для ALIEN_MOVE
    level_number = 0  # номер уровня
    count_text = [100, 600, 50, 100]  # затраты энергии на постройку и нач-ное кол-во энергии
    damage_cost_inscription = [2, 1]  # атакка турелей
    state = 0  # переменная работы камеры
    kill_count = 0  # кол-во убитых противников
    pause_state = 0  # переменная паузы
    move_cam_like_video = 0  # переменная специальной анимации камеры(при смерти и зачистки уровня)
    kill_sprite = 0  # спрайт который убьёт игрока
    lose, win = False, False  # поражение, победа
    font2 = pygame.font.SysFont('Times New Roman', 15)
    energy_sign = pygame.transform.scale(load_image('electricity.png'), (40, 40))  # спрайт энергии
    small_energy_sign = pygame.transform.scale(load_image('electricity.png'),
                                               (15, 15))  # спрайт энергии для окна построек
    small_damage_sign = pygame.transform.scale(load_image('fist.png'), (15, 15))  # спрайт силы для окна построек
    clock_image = pygame.transform.scale(load_image('clock.png'), (30, 30))  # спрайт часов
    seconds, minutes = 0, 0  # сукунды минуты
    pygame.time.set_timer(SECOND_TIME, 1000)
    screen = pygame.display.set_mode(SIZE_GAME)
    new_level = 1
    arrow_text = 'Вперёд'
    pygame.key.set_repeat(1, 50)

    def load_level(filename):  # функция загрузки уровня
        with open('data/' + filename, 'r') as mapFile:  # первые 6 строк - номер дорожки, и кол-во противников на ней
            lines = list(map(lambda x: x[:-1], mapFile.readlines()))  # потом идёт задержка между появление врагов
        return list(filter(lambda x: x[1] > 0, [list(map(int, i.split(','))) for i in lines[:6]])), \
               int(lines[6]), int(lines[-1])  # и общее кол-во врагов

    def new_enemy(lines, enemy_count):  # список путей, кол-во врагов
        if enemy_count:
            ways = [way[0] for way in lines]  # список номеров путей
            choosen_way = random.choice(ways)  # случайный путь
            line_index = ways.index(choosen_way)  # индекс пути в списке
            Alien(710, 59 + 59 * choosen_way)  # создание пришельца
            if lines[line_index][1] == 1:  # если противник на этом пути один
                lines.pop(line_index)  # то удалить этот путь
            else:
                lines[line_index][1] -= 1  # уменьшить кол-во противников на пути

    class Floor(pygame.sprite.Sprite):  # класс пола
        def __init__(self, x, y):
            super().__init__(floor_group, new_game_all_sprites)  # группа пола для коллизии с курсором -> создания
            self.image = random.choice(tile_images['floor'])  # окна постройки
            self.rect = self.image.get_rect().move(59 * x - 708, 118 + 59 * y)

    class Battery(pygame.sprite.Sprite):  # класс генератора
        def __init__(self, x, y):
            super().__init__(battery_group,  # группа генераторов
                             buildings_group,  # группа строений
                             new_game_all_sprites)
            self.tile = 0  # начальный id фрейма
            self.image = tile_images['battery'][self.tile]  # начальный фрейм
            self.rect = self.image.get_rect().move(x + 1, y + 3)  # создание коллизии по прямоугольнику
            self.mask = pygame.mask.from_surface(self.image)  # создание коллизии по маске
            self.hp = 30  # кол-во жизней

        def update(self, color, count_text):
            if color == 'yellow':  # если цвет жёлтый, то выработка энергии и увеличение токена энергии
                self.tile = 1
                count_text[3] += 25
            else:
                self.tile = 0
            self.image = tile_images['battery'][self.tile]  # изменяю фрейм

        def collide_bullet(self):  # если пересечение пуль босса и постройки - уменьшение жизней. Аналогично
            collision = pygame.sprite.spritecollide(self, enemy_bullets, dokill=True,  # для всех строений
                                                    collided=pygame.sprite.collide_mask)
            if collision:
                self.hp -= 5
            if self.hp < 1:  # если нет жизней, то удалить
                destroy_sound_channel.play(destroy_sound)
                self.kill()

    class DefenseTurret(pygame.sprite.Sprite):  # защитная турель
        def __init__(self, x, y):
            super().__init__(defense_turret_group,
                             buildings_group,
                             new_game_all_sprites)
            self.tile = 0
            self.image = tile_images['defense_turret'][self.tile]
            self.rect = self.image.get_rect().move(x + 5, y + 3)
            self.mask = pygame.mask.from_surface(self.image)
            self.hp = 160

        def update(self):  # изменяю фрейм турели(анимация)
            self.tile = (self.tile + 1) % 2
            self.image = tile_images['defense_turret'][self.tile]
            self.mask = pygame.mask.from_surface(self.image)
            if self.tile == 1:  # если id фрейма 1, то создать оранжевый снаряд
                defense_turret_sound_channel.play(defense_turret_sound)
                Bullet2(self.rect.right - 4, self.rect.top + 8)

        def collide_bullet(self):
            collision = pygame.sprite.spritecollide(self, enemy_bullets, dokill=True,
                                                    collided=pygame.sprite.collide_mask)
            if collision:
                self.hp -= 5
            if self.hp < 1:
                destroy_sound_channel.play(destroy_sound)
                self.kill()

    class Turret(pygame.sprite.Sprite):  # класс турели
        def __init__(self, x, y):
            super().__init__(turret_group, buildings_group,
                             new_game_all_sprites)
            self.tile = 0
            self.image = tile_images['turret'][self.tile]
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)
            self.hp = 20

        def update(self):
            self.tile = (self.tile + 1) % 3
            self.image = tile_images['turret'][self.tile]
            self.mask = pygame.mask.from_surface(self.image)
            if self.tile == 2:
                turret_sound_channel.play(turret_sound)
                Bullet(self.rect.right - 10, self.rect.top)

        def collide_bullet(self):
            collision = pygame.sprite.spritecollide(self, enemy_bullets, dokill=True,
                                                    collided=pygame.sprite.collide_mask)
            if collision:
                self.hp -= 5
            if self.hp < 1:
                destroy_sound_channel.play(destroy_sound)
                self.kill()

    class Bullet(pygame.sprite.Sprite):  # обычный фиолетовый снаряд
        def __init__(self, x, y):
            super().__init__(bullet_group, bullets, new_game_all_sprites)
            self.image = tile_images['bullet']
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):  # если за экраном, то удалить
            self.rect = self.rect.move(3, 0)
            if self.rect.x > 708:
                self.kill()

    class Bullet2(pygame.sprite.Sprite):  # кскоренный в два раза снаряд
        def __init__(self, x, y):
            super().__init__(bullet_group, bullets, new_game_all_sprites)
            self.image = tile_images['orange_bullet']
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.rect = self.rect.move(6, 0)
            if self.rect.x > 708:
                self.kill()

    class Alien(pygame.sprite.Sprite):  # пришелец
        def __init__(self, x, y):
            super().__init__(alien_group, new_game_all_sprites)
            self.tile = 0  # id фрейма
            self.sheet = 'alien_move'  # название списка фреймов
            self.image = tile_images[self.sheet][0]  # фрейм
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)
            self.hp = 20  # 20 хп
            self.count_of_frames = 6  # кол-во фреймов в списке tile_images[self.sheet]
            self.state = 1  # состояние: 1 -движение, 2 - смерть, 3 - атака
            self.kill_sprite = False  # является ли убивающим спрайтом
            self.offset = 0  # смещение коллизии(для атаки)
            self.from_scope = False  # за экраном
            pygame.time.set_timer(ALIEN_MOVE, movement)  # установка таймера

        def update(self):  # провверяет события движения, смерти, атаки
            global kill_count, state, move_cam_like_video
            if self.state == 2:  # если состояние смерти
                if self.kill_sprite:  # если убрать класс
                    kill_count -= 1  # уменьшение общего кол-ва противников
                    if not kill_count and not boss_group:  # если больше нет противников(ни пришельцев, ни босса)
                        state = 1  # то движение камеры
                        move_cam_like_video = 1  # анимация зачистки уровня
                    self.kill()
                if self.tile == 4:  # если id фрейма равен 4, то в следющий раз убрать класс
                    self.kill_sprite = True
            else:
                if self.hp < 1:  # если нет жизней
                    self.rect = self.rect.move(self.offset, 0)
                    self.count_of_frames = 5
                    self.tile = 0
                    self.sheet = 'alien_death'
                    self.state = 2  # поменять состояние на 'смерть'
                    alien_death_sound_channel.play(alien_death_sound)
                elif self.state == 1:
                    collision = pygame.sprite.spritecollide(self, buildings_group, dokill=False,  # коллизия
                                                            collided=pygame.sprite.collide_mask)  # с постройкой
                    if collision or pygame.sprite.spritecollideany(self, player_group):
                        self.rect = self.rect.move(-10, 0)  # передвижение коллизии
                        self.state = 3  # состояние атаки
                        self.sheet = 'alien_attack'
                        self.tile = 0
                        self.count_of_frames = 4
                        if collision:  # коллизия с постройкой
                            self.collision_obj = collision[0]
                        else:  # коллизия с игроком(событие смерти игрока, проигрыш)
                            self.collision_obj = player

                elif self.state == 3:  # событие атаки
                    if self.tile == 0:  # изменение x, чтобы спрайт не перемещался при атаке(разные длины)
                        self.rect = self.rect.move(34, 0)
                        self.offset = 4
                    elif self.tile == 1:
                        self.rect = self.rect.move(-5, 0)
                        self.offset += 5
                    elif self.tile == 2:
                        self.offset += 11
                        self.rect = self.rect.move(-11, 0)
                    elif self.tile == 3:  # если последний фрейм в списке фреймов атаки
                        alien_attck_sound_channel.play(alien_attack_sound)
                        self.offset += 18
                        self.rect = self.rect.move(-18, 0)
                        self.collision_obj.hp -= 2  # уменьшить жизни объекта коллизии
                    if self.collision_obj.hp < 1:  # если у объекта коллизии нет хп
                        self.rect = self.rect.move(self.offset, 0)
                        self.state = 1  # продолжить движение
                        self.tile = 0
                        self.sheet = 'alien_move'
                        self.count_of_frames = 6
            self.image = tile_images[self.sheet][self.tile]  # обновление фрейма
            self.tile = (self.tile + 1) % self.count_of_frames  # обновление id  фрейма
            self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)  # обновление коллизии
            self.mask = pygame.mask.from_surface(self.image)  # обновление маски

        def collide_bullet(self):  # пересечение с шариками игрока
            if self.state != 2:
                collision = pygame.sprite.spritecollide(self, bullet_group, dokill=True,
                                                        collided=pygame.sprite.collide_mask)
                if collision:
                    if collision[0].image == tile_images['bullet']:  # если фиол. шарик
                        self.hp -= 2  # -2 хп
                    else:
                        self.hp -= 1  # оранжевый наносит 1 хп

        def move(self):  # функция движения(проверка на движении обычном и при проигрыше)
            global kill_sprite
            if not kill_sprite:
                if self.rect.x <= 0:
                    kill_sprite = self  # сделать убивающим спрайтом. Потом update и move будут только для него
                else:
                    self.rect = self.rect.move(-4, 0)
            else:
                if not self.kill_event():  # если не за экраном
                    self.rect = self.rect.move(-4, 0)
                else:
                    if self == kill_sprite:  # если убивающий спрайт
                        self.left_y_coords = (self.left_y_coords + self.remainder) % 1  # добавление остатка y
                        if self.y_offset > 0:  # если смещение по y пришельца положительное
                            self.rect = self.rect.move(-4, self.y_offset + self.left_y_coords)
                        else:
                            self.rect = self.rect.move(-4, self.y_offset - self.left_y_coords)

        def kill_event(self):  # проверка на событие проигрыша
            global movement, draw_frame_group, state, move_cam_like_video, kill_sprite
            if not self.from_scope:  # если не за экраном
                condition = kill_sprite.rect.x + kill_sprite.rect.w <= 0
            else:  # при перемещении камеры нужно поменять условие перемещения(вместо <= 0, <= WIDTH)
                condition = kill_sprite.rect.x + kill_sprite.rect.w <= WIDTH
            if condition and self == kill_sprite and not self.from_scope:  # если убивающий спрайт ушёл за экран
                movement *= 2  # увеличить задержку движения пришельца
                pygame.time.set_timer(ALIEN_MOVE, 1500)  # установить паузу
                draw_frame_group = False  # нельзя показывать постройки
                self.from_scope = True
                self.y_offset = (player.rect.y - self.rect.y) / ((self.rect.x - player.rect.x - player.rect.w) // 4)
                self.remainder = self.y_offset - int(self.y_offset)
                self.left_y_coords = 0  # y_offset - перемещение по y за раз, remainder - остаток y_offset
                state = True  # движение камеры
                move_cam_like_video = True  # анимация при проигрыше
            return condition

    class Boss(pygame.sprite.Sprite):  # Босс
        def __init__(self):
            super().__init__(boss_group, new_game_all_sprites)
            self.tile = 0
            self.image1 = pygame.transform.scale(load_image('robot1.png'), (59, 59))
            self.image = self.image1
            self.sheet = tile_images['boss']  # список фреймов движения
            self.robot_death_sheet = tile_images['boss_death']  # список фреймов смерти
            self.rect = self.image.get_rect().move(708 - 118, 59 * 5)
            self.mask = pygame.mask.from_surface(self.image)
            self.hp = 200  # 200 хп
            self.move_to = self.rect.y  # координата y  к которой надо двигаться
            self.state = 0  # состояние
            self.step = 0  # шаг
            pygame.time.set_timer(BOSS_CHOICE, 1200)
            pygame.time.set_timer(BOSS_SHOOT, 400)

        def update(self):
            global kill_count, state, move_cam_like_video
            if self.state:  # если событие смерти
                self.tile = self.tile + 1
                if self.tile == 5:  # если id фрейма 5
                    self.kill()
                    if not kill_count and not boss_group:  # если нет противников
                        state = 1  # событие зачистки уровня
                        move_cam_like_video = 1
                else:
                    self.image = self.robot_death_sheet[self.tile]  # изменения анимации смерти
            else:
                if self.hp < 1:  # если нет жизней
                    self.tile = 0
                    self.state = 1
                    boss_death_sound_channel.play(boss_death_sound)
                if self.rect.y == self.move_to or self.rect.bottom == self.move_to:  # если дошёл до y
                    self.tile = 0
                    self.image = self.image1
                else:  # изменение фрейма
                    self.tile = (self.tile + 1) % 9
                    self.image = tile_images['boss'][self.tile]
                self.mask = pygame.mask.from_surface(self.image)

        def move(self):
            if not self.state:
                if not (self.rect.y == self.move_to or self.rect.bottom == self.move_to):  # если не дошёл до move_to
                    self.rect = self.rect.move(0, self.step)

        def collide_bullet(self):  # пересечение с снарядами игрока
            if not self.state:
                collision = pygame.sprite.spritecollide(self, bullet_group, dokill=True,
                                                        collided=pygame.sprite.collide_mask)
                if collision:
                    if collision[0].image == tile_images['bullet']:
                        self.hp -= 2
                    else:
                        self.hp -= 1

        def shoot(self):  # функция стрельбы
            boss_attack_sound_channel.play(boss_attack_sound)
            Boss_Bullet(self.rect.x - 20, self.rect.y + 22)

    class Boss_Bullet(pygame.sprite.Sprite):  # снаряд босса
        def __init__(self, x, y):  # конструктор
            super().__init__(enemy_bullets, bullets, new_game_all_sprites)
            self.image = pygame.transform.scale(load_image('boss_bullet.png'), (20, 12))
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):  # функция перемещения
            self.rect = self.rect.move(-6, 0)
            if self.rect.right < 0:
                self.kill()

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(player_group, new_game_all_sprites)
            self.vector = 0
            self.tiles1 = tile_images['player_move_down']  # список движения вниз
            self.tiles2 = tile_images['player_move_up']  # список движения вверх
            self.tiles3 = tile_images['player_move_rigth']  # список движения вправо
            self.tiles4 = tile_images['player_move_left']  # список движения влево
            self.list_of_tile_groups = [self.tiles1, self.tiles2, self.tiles3, self.tiles4]  # список списков фреймов
            self.tile = 0
            self.image = self.list_of_tile_groups[self.vector][self.tile]  # начальный фрейм
            self.mask = pygame.mask.from_surface(self.image)  # маска
            self.rect = self.image.get_rect().move(-374, (118 + 59 * 7 // 2) - 27)
            self.hp = 2  # 2 жизни(один удар пришельца)

        def update(self):  # проверка на кол-во жизней
            global lose, music_channel
            if self.hp < 1:  # если нет - проиграл
                self.kill()
                music_channel.stop()
                lose = True

        def move(self, x, y, vector):
            global new_level, move_cam_like_video
            if self.vector == vector:  # если предыдущее направление равно этому
                self.tile = (self.tile + 1) % 9
            else:
                self.vector = vector  # новое направление
                self.tile = 0
            self.image = self.list_of_tile_groups[self.vector][self.tile]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.rect.move(x, y)
            if pygame.sprite.spritecollideany(self, border_group):  # нельзя заходить за границы
                self.rect = self.rect.move(-x, -y)
            if self.rect.x > 708:
                global new_level  # новый уровень
                if level_number != 4:  # только если не последний
                    new_level = True

    class Border(pygame.sprite.Sprite):  # граница, стена
        def __init__(self, x1, y1, widht, heigth):
            super().__init__(new_game_all_sprites)
            if x1 == -374 or x1 == 374:  # граница для камеры
                self.image = pygame.Surface([widht, heigth])
                self.rect = pygame.Rect(x1, y1, widht, heigth)
                self.add(end_of_cam_group)
            else:  # граница для игрока
                self.image = pygame.Surface([widht, heigth])
                self.rect = pygame.Rect(x1, y1, widht, heigth)
                self.add(border_group)

    class Portal(pygame.sprite.Sprite):  # портал
        def __init__(self):
            super().__init__(portal_group, new_game_all_sprites)
            self.tile = 0
            self.tiles = tile_images['portal']
            self.image = self.tiles[self.tile]
            self.rect = self.image.get_rect().move(708 - 59, 59 * 5)
            self.mask = pygame.mask.from_surface(self.image)
            pygame.time.set_timer(PORTAL_TIME, 100)

        def update(self):  # изменение фрейма и проверка коллизии с игроком
            global win
            self.tile = (self.tile + 1) % 8
            self.image = self.tiles[self.tile]
            self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
            self.mask = pygame.mask.from_surface(self.image)
            if pygame.sprite.collide_mask(self, player):  # если есть коллизия
                win = True  # Победа

    class White_Arrow(pygame.sprite.Sprite):  # стрелка направления
        def __init__(self):
            super().__init__(arrow_group)
            self.image = tile_images['arrow']
            self.rect = self.image.get_rect().move(530, 80)
            self.dx = 0

        def update(self):
            if self.rect.left < 560:  # границы движения
                self.dx = 2
            elif self.rect.right > 700:
                self.dx = -2
            self.rect = self.rect.move(self.dx, 0)

    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, group):
            for obj in group.sprites():
                obj.rect.x += self.dx

        # позиционировать камеру на объекте target(player)
        def update(self, target):
            global move_cam_like_video
            if move_cam_like_video:  # если анимация
                if target.rect.x + target.rect.w // 2 - WIDTH // 2 != 0:  # если середина фрейма игрока !=
                    self.dx = 1  # середине экрана
                else:
                    self.dx = 0
                    move_cam_like_video = 0
                    if not kill_count:  # если это не событие смерти
                        White_Arrow()
            else:  # обычная функция следования камеры за игроком
                self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)

    class Pause:  # пауза
        def __init__(self):
            self.state = 0
            self.tiles = tile_images['pause']
            self.image = self.tiles[self.state]
            self.rect = self.image.get_rect().move(WIDTH // 2 - 14, 0)
            self.mask = pygame.mask.from_surface(self.image)

        def change_state_of_pause(self):  # смена состояния
            global pause_state
            pause_state = not pause_state  # глобальная переменная
            self.state = not self.state  # индекс фрейма
            self.image = self.tiles[self.state]
            if pause_state:  # если пауза, то все звуки остановить
                pygame.mixer.pause()
            else:
                pygame.mixer.unpause()

    class Frame(pygame.sprite.Sprite):  # рамка окна постройки
        def __init__(self, x, y):
            super().__init__(frame_group)
            self.image = tile_images['frame']
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)

    class Img_Turret(pygame.sprite.Sprite):  # объект турели
        def __init__(self, x, y):
            super().__init__(frame_group, object_group)
            self.state = 0  # состояние(можно ставить или нет)
            self.image = tile_images['turret'][0]
            self.states = [self.image, pygame.transform.scale(load_image('turret12.png'), (59, 52))]
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)
            self.energy_consumption = 100  # затраты энергии на постройку

        def update(self):  # изменение состояния
            self.state = not self.state
            self.image = self.states[self.state]

    class Img_Def_turret(pygame.sprite.Sprite):  # объект защитной турели
        def __init__(self, x, y):
            super().__init__(frame_group, object_group)
            self.state = 0
            self.image = tile_images['defense_turret'][self.state]
            self.states = [self.image, pygame.transform.scale(load_image('defense_turret12.png'), (53, 51))]
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)
            self.energy_consumption = 600

        def update(self):
            self.state = not self.state
            self.image = self.states[self.state]

    class Img_battery(pygame.sprite.Sprite):  # обьект генератора
        def __init__(self, x, y):
            super().__init__(frame_group, object_group)
            self.state = 0
            self.image = tile_images['battery'][0]
            self.states = [self.image, pygame.transform.scale(load_image('battery12.png'), (58, 52))]
            self.rect = self.image.get_rect().move(x, y)
            self.mask = pygame.mask.from_surface(self.image)
            self.energy_consumption = 50

        def update(self):
            self.state = not self.state
            self.image = self.states[self.state]

    pause = Pause()  # пауза
    camera = Camera()  # камера
    player = Player()  # игрок
    set_building = [Frame(0, 0),
                    Img_Turret(0, 0),
                    Img_Def_turret(0, 0),
                    Img_battery(0, 0)]  # список элементов окна постройки
    Border(-708, 118, 1416, 1)  # границы
    Border(-708, 472, 1416, 1)
    Border(-708, 118, 1, 472 - 118)
    Border(-374, 118, 1, 472 - 118)
    Border(374, 118, 1, 472 - 118)
    for i in range(24):  # создание поля
        for j in range(6):
            Floor(i, j)
    while True:
        screen.blit(fon, (0, 0))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)
            if new_level:  # если новый уровень
                for building in buildings_group.sprites():  # очищение почти всех групп
                    building.kill()
                player.kill()
                for obj in object_group:
                    obj.state = 0
                    obj.image = obj.states[obj.state]
                for arrow in arrow_group:
                    arrow.kill()
                player = Player()  # замена игрока(в том чиле и его позиции)
                state = 0  # замена переменных
                pause_state = 0
                move_cam_like_video = 0
                draw_frame_group = False
                movement = 150
                state_for_battery_cd = 1  # переменная перезарядки генератора
                states_for_cd = [0, 0, 0]  # список объектов на перезарядке
                level_number += 1
                new_level = 0  # атакующие линии, задержка между врагами, кол-во врагов
                attack_lines, delay, enemy_count = load_level('level' + str(level_number) + '.txt')
                kill_count = enemy_count  # kill_count == 0, то уровень зачищен
                pygame.time.set_timer(ENEMY_TIME, delay)  # событие появления врага
                if level_number == 4:  # последний уровень
                    boss = Boss()
                    Portal()
                    arrow_text = 'В портал'
            if event.type == pygame.KEYDOWN:  # если нажатие на пробел - изменение паузы
                if event.key == pygame.K_SPACE:
                    pause.change_state_of_pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lose:  # если поражение
                    screen = pygame.display.set_mode(SIZE)
                    dark_souls_channel.stop()
                    start_screen()
                else:
                    if pygame.sprite.spritecollideany(pause, cursor_group):  # нажатие на паузу
                        pause.change_state_of_pause()
                    elif not pause_state:
                        collide_with_flore = pygame.sprite.spritecollideany(cursor, floor_group)
                        if draw_frame_group:  # если рисовать окно построек
                            collide_with_object = pygame.sprite.spritecollideany(cursor, object_group)
                            if collide_with_object:  # если коллизия с объектом
                                obj = collide_with_object  # объект коллизии
                                if not obj.state and count_text[3] >= obj.energy_consumption:  # если хватает энергии
                                    count_text[3] -= obj.energy_consumption  # на постройку
                                    draw_frame_group = False
                                    coords = (x_floor, y_floor)  # нужно будет для перемещения коллизии объектов
                                    if obj == set_building[1]:  # при инициализации
                                        Turret(*coords)
                                        states_for_cd[0] = 1
                                        pygame.time.set_timer(FRAME_TIME, 400)  # таймер на обновление постройки
                                        pygame.time.set_timer(
                                            *cd_for_turret)  # таймер на обновление перезарядки строения
                                    elif obj == set_building[2]:
                                        DefenseTurret(*coords)
                                        states_for_cd[1] = 1
                                        pygame.time.set_timer(FRAME_TIME2, 200)
                                        pygame.time.set_timer(*cd_for_def_turret)
                                    elif obj == set_building[3]:
                                        Battery(*coords)
                                        states_for_cd[2] = 1
                                        pygame.time.set_timer(ENERGY_ACCUMULATION_EVENT, 4500)
                                        pygame.time.set_timer(*cd_for_battery)
                                    set_building[set_building.index(obj)].update()
                            else:
                                collide_with_frame = pygame.sprite.spritecollideany(cursor, frame_group)
                                if not collide_with_frame:  # если коллизия не с окном построек
                                    draw_frame_group = False
                        else:
                            if collide_with_flore and not kill_sprite:  # если коллизия с полом нет события смерти
                                if not pygame.sprite.spritecollideany(collide_with_flore, buildings_group):  # если
                                    energy_cost_list, damage_cost_list = [], []  # на плитке ещё нет построек
                                    obj = collide_with_flore
                                    x_floor, y_floor = obj.rect.x, obj.rect.y
                                    draw_frame_group = True
                                    # перемещение коллизий окна
                                    set_building[0].rect.x, set_building[0].rect.y = obj.rect.x, obj.rect.y - 40
                                    set_building[1].rect.x, set_building[
                                        1].rect.y = obj.rect.x + 10, obj.rect.y - 36
                                    set_building[2].rect.x, set_building[
                                        2].rect.y = obj.rect.x + 79, obj.rect.y - 36
                                    set_building[3].rect.x, set_building[
                                        3].rect.y = obj.rect.x + 155, obj.rect.y - 37
                                    energy_cost_list.append((obj.rect.x + 48, obj.rect.y - 24))
                                    damage_cost_list.append((obj.rect.x + 48, obj.rect.y - 9))
                                    energy_cost_list.append((obj.rect.x + 142, obj.rect.y - 24))
                                    damage_cost_list.append((obj.rect.x + 142, obj.rect.y - 9))
                                    energy_cost_list.append((obj.rect.x + 216, obj.rect.y - 24))
            if not pause_state:  # если нет паузы
                if not kill_count and not kill_sprite and not boss_group:  # если событие зачистки уровня
                    if event.type == pygame.KEYDOWN:
                        pressed_keys = pygame.key.get_pressed()
                        if pressed_keys[pygame.K_a]:
                            player.move(-4, 0, 3)
                        elif pressed_keys[pygame.K_d]:
                            player.move(4, 0, 2)
                        elif pressed_keys[pygame.K_w]:
                            player.move(0, -4, 1)
                        elif pressed_keys[pygame.K_s]:
                            player.move(0, 4, 0)
                    if event.type == PORTAL_TIME:  # изменение фрейма портала
                        portal_group.update()
                        pygame.time.set_timer(PORTAL_TIME, 100)
                else:
                    if not kill_sprite or not kill_sprite.kill_event():
                        if event.type == FRAME_TIME:  # изменение турели
                            pygame.time.set_timer(FRAME_TIME, 400)
                            turret_group.update()
                        if event.type == FRAME_TIME2:  # изменение защитной турели
                            pygame.time.set_timer(FRAME_TIME2, 200)
                            defense_turret_group.update()
                        if event.type == ENERGY_ACCUMULATION_EVENT:  # событие зарядки
                            pygame.time.set_timer(ENERGY_ACCUMULATION_EVENT, 4500)
                            pygame.time.set_timer(ENERGY_GIVING_EVENT, 300)  # т. к. у меня не получилось с
                            state_for_battery_cd = 0  # pygame 2.0.0, то пришлось вводить переменную состояния батареи
                        if event.type == ENERGY_GIVING_EVENT:  # событие выработки энергии
                            if not state_for_battery_cd and battery_group:  # если 'не ждать зарядки' и есть генераторы
                                charging_sound_channel.play(charging_sound)
                                battery_group.update('yellow', count_text)  # изменение фрейма на выработку
                                state_for_battery_cd = 1
                            else:
                                battery_group.update('blue', count_text)
                        if event.type == cd_for_turret[0]:  # событие перезарядки объекта турели
                            if states_for_cd[0]:
                                set_building[1].update()
                            states_for_cd[0] = 0
                        if event.type == cd_for_def_turret[0]:  # событие перезарядки объекта защитной турели
                            if states_for_cd[1]:
                                set_building[2].update()
                            states_for_cd[1] = 0
                        if event.type == cd_for_battery[0]:  # событие перезарядки объекта генератора
                            if states_for_cd[2]:
                                set_building[3].update()
                            states_for_cd[2] = 0
                        if event.type == ENEMY_TIME:  # появление врага
                            if enemy_count:
                                new_enemy(attack_lines, enemy_count)
                                enemy_count -= 1
                                pygame.time.set_timer(ENEMY_TIME, delay)
                                delay -= 50  # уменьшаю задержку
                        if event.type == BOSS_CHOICE:  # собыитие движения босса
                            boss_rect = boss.rect  # коллизия босса
                            if boss_rect.y == boss.move_to or boss_rect.bottom == boss.move_to:  # если в точке назначения
                                if boss_rect.y == 118:  # если касается верхней границы
                                    vector = 1  # идёт вниз
                                elif boss_rect.bottom == HEIGHT:
                                    vector = 0  # идёт вверх
                                else:
                                    vector = random.choice([0, 1])  # случайный выбор направления
                                if vector:  # если вниз, то от низа фрейма до HEIGHT
                                    boss.move_to = random.randint(boss_rect.bottom, HEIGHT)
                                    boss.step = 1
                                else:  # иначе от y фрейма до границы поля
                                    boss.move_to = random.randint(118, boss_rect.y)
                                    boss.step = -1
                            else:
                                boss.update()
                                boss.move()
                            pygame.time.set_timer(BOSS_CHOICE, 200)
                        if event.type == BOSS_SHOOT:  # стрельба босса
                            boss.shoot()
                            pygame.time.set_timer(BOSS_SHOOT, 1200)
                        if event.type == ALIEN_MOVE:  # движение пришельца
                            alien_group.update()
                            for i in alien_group:
                                if i.state != 3:  # если не атакует
                                    i.move()
                            pygame.time.set_timer(ALIEN_MOVE, movement)
                        if event.type == PORTAL_TIME:  # событие портала
                            portal_group.update()
                            pygame.time.set_timer(PORTAL_TIME, 100)
                    else:
                        if event.type == ALIEN_MOVE:
                            kill_sprite.update()  # если есть убивающий спрайт
                            if kill_sprite.state != 3:
                                kill_sprite.move()
                            pygame.time.set_timer(ALIEN_MOVE, movement)
            if event.type == SECOND_TIME:  # изменение времени
                seconds += 1
                minutes = minutes + seconds // 60
                seconds %= 60
                pygame.time.set_timer(SECOND_TIME, 1000)
        if lose:  # если проигрыш
            screen.blit(pygame.transform.scale(load_image('you died.jpg'), screen.get_size()), (0, 0))
            dark_souls_channel.play(dark_souls, loops=1)
        elif win:  # если победа
            return minutes, seconds  # завершить функцию и вернуть время игры
        else:  # рисование всех обьектов
            screen.blit(energy_sign, (5, 5))
            screen.blit(font.render(str(count_text[3]), 1, pygame.Color('White')), (40, 5))
            screen.blit(pause.image, (WIDTH // 2 - 14, 0))
            screen.blit(clock_image, (600, 5))
            screen.blit(font1.render(str(minutes) + ':' + str(seconds), 1, pygame.Color('White')), (635, 5))
            if not kill_count and not pause_state:  # обновление положения указательной стрелки
                arrow_group.update()
            if arrow_group:  # если есть указательная стрела
                screen.blit(font1.render(arrow_text, 1, pygame.Color('White')), (580, 40))
                arrow_group.draw(screen)
            floor_group.draw(screen)
            portal_group.draw(screen)
            buildings_group.draw(screen)
            alien_group.draw(screen)
            if state and not pause_state:  # если камера двигается и нет паузы
                rectangle = player.rect  # колизия игрока
                if end_of_cam_group.sprites()[0].rect.x <= rectangle.x and rectangle.x + rectangle.w <= \
                        end_of_cam_group.sprites()[1].rect.x:  # если середина игрока не в середине экрана
                    camera.update(player)
                    camera.apply(new_game_all_sprites)
            player_group.draw(screen)
            boss_group.draw(screen)
            bullets.draw(screen)
            # проверка на пересечение со снарядами
            for alien in alien_group:
                alien.collide_bullet()
            for bos in boss_group:
                bos.collide_bullet()
            for building in buildings_group:
                building.collide_bullet()
            if draw_frame_group:  # отрисовка окна построек
                frame_group.draw(screen)
                for i in range(3):
                    screen.blit(
                        font2.render(str(object_group.sprites()[i].energy_consumption), 1, pygame.Color('White')),
                        energy_cost_list[i])
                    screen.blit(small_energy_sign, (energy_cost_list[i][0] - 15, energy_cost_list[i][1]))
                for i in range(2):
                    screen.blit(font2.render(str(damage_cost_inscription[i]), 1, pygame.Color('White')),
                                damage_cost_list[i])
                    screen.blit(small_damage_sign, (damage_cost_list[i][0] - 15, damage_cost_list[i][1]))
            if not pause_state:  # обновление движения снарядов и игрока
                bullets.update()
                player.update()
        pygame.display.flip()


def load_image(name, colorkey=None):  # функция загрузки картинки(из яндекса)
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cursor(pygame.sprite.Sprite):  # курсор
    def __init__(self, cursor_group):
        super().__init__(cursor_group)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Text(pygame.sprite.Sprite):  # текст
    def __init__(self, surf, rectangle, all_sprites):
        super().__init__(all_sprites)
        self.image = surf
        self.rect = rectangle

    def update(self):
        self.rect.y -= 1


attack_aliens = [pygame.transform.scale(load_image('green_alien7.png'), (44, 55)),
                 pygame.transform.scale(load_image('green_alien8.png'), (49, 55)),
                 pygame.transform.scale(load_image('green_alien9.png'), (59, 55)),
                 pygame.transform.scale(load_image('green_alien10.png'), (79, 55))]
tile_images = {'wall': load_image('box.png'),
               'floor': [load_image('floor' + str(i) + '.png') for i in range(1, 5)],
               'turret': [pygame.transform.scale(load_image('turret' + str(i) + '.png'), (59, 52))
                          for i in range(1, 4)],
               'bullet': pygame.transform.scale(load_image('bullet.png'), (15, 15)),
               'alien_move': [pygame.transform.scale(load_image('green_alien' + str(i) + '.png'), (40, 55))
                              for i in range(1, 7)],
               'alien_attack': attack_aliens,
               'alien_death': [pygame.transform.scale(load_image('green_alien' + str(i) + '.png'), (40, 55))
                               for i in range(11, 16)],
               'defense_turret': [pygame.transform.scale(load_image('defense_turret' + str(i) + '.png'), (53, 51))
                                  for i in range(1, 3)],
               'orange_bullet': pygame.transform.scale(load_image('orange_bullet.png'), (10, 10)),
               'battery': [pygame.transform.scale(load_image('battery' + str(i) + '.png'), (58, 52))
                           for i in range(1, 3)],
               'frame': pygame.transform.scale(load_image('frame.png'), (240, 60)),
               'pause': [pygame.transform.scale(load_image('pause.png'), (35, 35)),
                         pygame.transform.scale(load_image('play.png'), (35, 35))],
               'player_move_down': [load_image('down' + str(i) + '.png') for i in range(1, 10)],
               'player_move_up': [load_image('up' + str(i) + '.png') for i in range(1, 10)],
               'player_move_left': [load_image('left' + str(i) + '.png') for i in range(1, 10)],
               'player_move_rigth': [load_image('rigth' + str(i) + '.png') for i in range(1, 10)],
               'arrow': pygame.transform.scale(load_image('white arrow.png'), (70, 20)),
               'boss': [pygame.transform.scale(load_image('robot_move' + str(i) + '.png'), (59, 59))
                        for i in range(1, 10)],
               'boss_death': [pygame.transform.scale(load_image('robot_death' + str(i) + '.png'), (59, 59))
                              for i in range(1, 6)],
               'portal': [pygame.transform.scale(load_image('portal' + str(i) + '.png', -1), (59, 59))
                          for i in range(1, 9)]}

start_screen()
