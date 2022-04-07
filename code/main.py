import random
from pre_game_functions import *


def show_statistic():
    global player
    print('*' * 20)
    print('Здоровье:', player.hp_)
    print('Голод:', player.hunger_)
    print('Счёт:', player.score_)
    print('Инвентарь:', *player.inventory_)
    print('Оружие:', player.weapon_.name_)
    print('*' * 20)
    print()


def play():
    global game
    global player
    game.show_prologue()
    player.current_location_ = game.locations_[0]
    return show_location()


def show_location():
    if is_dead():
        gameover('dead')
        return
    print()
    print(player.current_location_.name_)
    show_description()
    showed_actions = show_actions()
    show_statistic()
    return choice_action(showed_actions)


def show_description():
    print()
    print('-' * 80)
    print(player.current_location_.description_)
    print('-' * 80)
    print()


def show_actions():    # Выбирает, какие действия показывать
    showed_actions_ = []
    for action in player.current_location_.actions_:
        if int(action.time_) <= player.current_location_.how_much_time_actions_[action.number_ - 1]:
            continue
        if action.condition_ == -1:
            print(action.text_)
            showed_actions_.append(action)
            pass
        else:
            if action.condition_type_ == 'if':
                if player.current_location_.how_much_time_results_[int(action.condition_) - 1] > 0:
                    print(action.text_)
                    showed_actions_.append(action)
                    pass
            else:
                if player.current_location_.how_much_time_results_[int(action.condition_) - 1] == 0:
                    print(action.text_)
                    showed_actions_.append(action)
                    pass
    print()
    return showed_actions_


def show_result(action):    # Определяет тип результата
    if isinstance(action, ActionWithRandomResult):
        choice = random.randint(0, 100)
        left_border = 0
        right_border = int(action.chances_[0])
        for i in range(len(action.chances_)):
            if left_border <= choice <= right_border:
                result = action.results_[i]
                break
            left_border = right_border + 1
            right_border = right_border + int(action.chances_[i + 1])
        for i in player.current_location_.results_:
            if i.number_ == int(result):
                result = i
                break
        if player.current_location_.how_much_time_results_[result.number_ - 1] >= int(result.time_):
            return show_result(action)
        result_process(result)
        return show_location()

    if isinstance(action, ActionWithRepeatedResult):
        if player.current_location_.how_much_time_actions_[action.number_ - 1] >= int(action.attempts_):
            result = int(action.results_[1])
        else:
            result = int(action.results_[0])
        for i in player.current_location_.results_:
            if i.number_ == result:
                result = i
                break
        result_process(result)
        return show_location()

    if isinstance(action, ActionWithItemResult):
        if action.item_ in player.inventory_:
            result = action.results_[1]
        else:
            result = action.results_[0]
        for i in player.current_location_.results_:
            if i.number_ == int(result):
                result = i
                break
        result_process(result)
        return show_location()

    if isinstance(action, Action):
        for i in player.current_location_.results_:
            if i.number_ == int(action.results_):
                result = i
                break
        if result_process(result) == 'finish':
            return gameover('finish')
        return show_location()


def result_process(result):     #Делает с результатом действия и показывает его
    player.current_location_.how_much_time_results_[result.number_ - 1] += 1
    print()
    print(result.text_)
    input()
    player.hp_ += int(result.hp_)
    player.hunger_ += int(result.hunger_)
    player.score_ += int(result.score_)
    if result.item_ != '':
        for i in game.weapons_:
            if i.name_ == result.item_:
                player.weapon_ = i
        if result.item_action_ == '+':
            player.inventory_.append(result.item_)
        else:
            player.inventory_.remove(result.item_)
    if isinstance(result, LocationResult):
        for i in game.locations_:
            if int(result.location_) == i.number_:
                player.current_location_ = i
    if isinstance(result, EndGameResult):
        return 'finish'
    if isinstance(result, FightResult):
        for i in game.enemies_:
            if i.name_ == result.fight_:
                fight(i)


def choice_action(showed_actions):     #Ожидает ввод действия
    while True:
        action = input()
        for i in player.current_location_.actions_:
            if action == i.text_:
                if i in showed_actions:
                    player.current_location_.how_much_time_actions_[i.number_ - 1] += 1
                    return show_result(i)
        else:
            pass


def fight(enemy, strong=0):
    print(f'Напротив вас стоит {enemy.name_} и смотрит злобным взглядом')
    print()
    show_statistic()
    enemy_action = random.randint(0, 2)  # 0 - блок  1 - колющий удар  2 - режущий удар
    print('Защищаться')
    print('Ударить по прямой')
    print('Рубануть с плеча')
    while True:
        action = input()
        if strong == 1 and action == 'Рубануть с плеча':
            print('Я устал и пока не могу так ударить')
            input()
            return fight(enemy, 1)
        else:
            if action == 'Защищаться':
                if enemy_action == 0:
                    print('Мы оба встали в блок и смотрим друг на друга глупыми взглядами')
                    input()
                if enemy_action == 1:
                    if strong == 1:
                        print('Я устал после силового удара и не смог хорошо защититься')
                        input()
                        player.hp_ -= int(enemy.damage_ * 0.5)
                    else:
                        print('Противник нанёс колющий удар, но я смог его отразить')
                        input()
                if enemy_action == 2:
                    if strong == 1:
                        print('Я устал после силового удара и не смог хорошо защититься')
                        player.hp_ -= int(enemy.damage_ * 0.75)
                        input()
                    else:
                        print('Противник размахнулся и ударил со всей силы. С трудом, но я смог защититься')
                        input()
                if is_dead():
                    return
                if enemy.hp_ <= 0:
                    print('Бездыханный враг падает у моих ног')
                    input()
                    return show_location()
                return fight(enemy)

            if action == 'Ударить по прямой':
                if enemy_action == 0:
                    print('Враг успел встать в блок и мой удар не нанёс вреда')
                    input()
                if enemy_action == 1:
                    success_chance = random.randint(0, 1)   # 0 - не повезло, 1 - повезло
                    if success_chance == 0:
                        player.hp_ -= enemy.damage_
                        print('Мы вдвоём сделали выпад и попытались ударить по прямой, но противник оказался проворнее и попал по мне')
                        input()
                    else:
                        enemy.hp_ -= player.weapon_.damage_
                        print('Я смог дотянуться до врага и нанёс быстрый удар')
                        input()
                if enemy_action == 2:
                    success_chance = random.randint(1, 10)
                    if success_chance > 3:
                        player.hp_ -= int(enemy.damage_ * 1.5)
                        print('Враг оказался сильнее и его рубящий улар пришелся прямо по мне')
                        input()
                    else:
                        enemy.hp_ -= player.weapon_.damage_
                        print('Пока враг размахивался, я быстро сократил дистанцию и ударил его')
                        input()
                if is_dead():
                    return
                if enemy.hp_ <= 0:
                    print('Бездыханный враг падает у моих ног')
                    input()
                    return show_location()
                return fight(enemy)

            if action == 'Рубануть с плеча':
                if enemy_action == 0:
                    print('Враг встал в блок и весь мой сильнейщий удар оказался бесполезным')
                    input()
                if enemy_action == 1:
                    success_chance = random.randint(1, 10)
                    if success_chance <= 3:
                        player.hp_ -= enemy.damage_
                        print('Я размахнулся, но враг отошел неминого в сторону и больно ударил меня в бок')
                        input()
                    else:
                        enemy.hp_ -= int(player.weapon_.damage_ * 1.5)
                        print('Мой удар пришелся точно в цель, врагу пришлось не сладко')
                        input()
                if enemy_action == 2:
                    success_chance = random.randint(0, 1)  # 0 - не повезло, 1 - повезло
                    if success_chance == 0:
                        player.hp_ -= int(enemy.damage_ * 1.5)
                        print('Враг тоже размахнулся, но оказался сильнее меня и вся его сила обрушилась на моё тело')
                        input()
                    else:
                        enemy.hp_ -= int(player.weapon_.damage_ * 1.5)
                        print('Противник тоже хотел нанести сильный удар, но в последний момент я смог пересилить и ударил его прямо по голове')
                        input()
                if is_dead():
                    return
                if enemy.hp_ <= 0:
                    print('Бездыханный враг падает у моих ног')
                    input()
                    return show_location()
                return fight(enemy, 1)
            else:
                pass

def is_dead():
    if player.hp_ > 100:
        player.hp_ = 100
    if player.hunger_ < 0:
        player.hunger_ = 0
    if player.hp_ <= 0 or player.hunger_ >= 100:
        return True


def gameover(reason):
    if reason == 'dead':
        print('Вы умерли!')
        print(f'Ваш счёт: {player.score_}')
        input()
    if reason == 'finish':
        game.show_epilogue()
        print()
        print(f'Спасибо за игру. Ваш счёт: {player.score_}')
        input()


input("Добро пожаловать! Чтобы начать игру нажмите 'Enter'")
input("Правила игры:\nЧтобы выполнить действие, напишите его в консоль\nЧтобы читать текст дальше, нажимайте 'Enter'")
read_first_info()
read_prologue()
read_locations()
read_epilogue()
game = game_tmp
game.play_music(game.music_)
player = Player()
play()
