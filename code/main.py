import random
from pre_game_functions import *
from gameplay import *


def show_statistic():
    global player
    print('*' * 20)
    print('Здоровье:', player.hp_)
    print('Голод:', player.hunger_)
    print('Счёт:', player.score_)
    print('Инвентарь:', *[x for x in player.inventory_])
    print('*' * 20)
    print()


def play():
    global game
    global player
    player.current_location_ = game.locations_[0]
    return show_location(player.current_location_)


def show_location(current_location):
    print()
    print(current_location.name_)
    show_description(current_location)
    showed_actions = show_actions(current_location)
    show_statistic()
    return choice_action(current_location, showed_actions)

def show_description(current_location):
    print()
    print('-' * 80)
    print(current_location.description_)
    print('-' * 80)
    print()


def show_actions(current_location):
    showed_actions_ = []
    for action in current_location.actions_:
        if int(action.time_) <= current_location.how_much_time_actions_[action.numb_ - 1]:
            continue
        if action.condition_ == -1:
            print(action.text_)
            showed_actions_.append(action)
            pass
        else:
            if action.condition_type_ == 'if':
                if current_location.how_much_time_results_[int(action.condition_[0]) - 1] > 0:
                    print(action.text_)
                    showed_actions_.append(action)
                    pass
            else:
                if current_location.how_much_time_results_[int(action.condition_[0]) - 1] == 0:
                    print(action.text_)
                    showed_actions_.append(action)
                    pass
    print()
    return showed_actions_


def show_result(current_location, action):
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
        for i in current_location.results_:
            if i.number_ == int(result):
                result = i
                break
        if current_location.how_much_time_results_[result.number_ - 1] >= int(result.time_):
            return show_result(current_location, action)
        print()
        print(result.text_)
        current_location.how_much_time_results_[result.number_ - 1] += 1
        input()
        return show_location(current_location)

    if isinstance(action, Action):
        for i in current_location.results_:
            if i.number_ == int(action.results_):
                result = i
                break
        print()
        print(result.text_)
        current_location.how_much_time_results_[result.number_ - 1] += 1
        input()
        return show_location(current_location)


def result_detector():
    pass


def choice_action(current_location, showed_actions):
    while True:
        action = input()
        for i in current_location.actions_:
            if action == i.text_:
                if i not in showed_actions:
                    pass
                else:
                    current_location.how_much_time_actions_[i.numb_ - 1] += 1
                    return show_result(current_location, i)
        else:
            pass




input("Добро пожаловать! Чтобы начать игру нажмите 'Enter'")
input("Правила игры:\nЧтобы выполнить действие, напишите его в консоль\nЧтобы читать текст дальше, нажимайте 'Enter'")
read_first_info()
read_prologue()
read_locations()
read_epilogue()
game = game_tmp
game.play_music(game.music_)
player = Player()
game.show_prologue()
play()







#game.show_epilogue()
