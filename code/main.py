import random
from pre_game_functions import *
from gameplay import *


def play():
    global game
    global player
    player.current_location_ = game.locations_[0]
    print(game.locations_)
    show_location(player.current_location_)


def show_location(current_location):
    print()
    print(current_location.name_)
    current_location.show_description()
    current_location.show_actions()


def show_description(current_location):
    print()
    print('-' * 80)
    print(current_location.description_)
    print('-' * 80)
    print()


def show_actions(current_location):
    for action in current_location.actions_:
        if int(action.time_) <= current_location.how_much_time_actions_[action.numb_ - 1]:
            continue
        if action.condition_ == -1:
            print(action.text_)
            pass
        else:
            #print(action.condition_)
           # print(action.condition_type_)
            if action.condition_type_ == 'if':
                if current_location.how_much_time_results_[int(action.condition_[0]) - 1] > 0:
                    print(action.text_)
                    pass
            else:
                if current_location.how_much_time_results_[int(action.condition_[0]) - 1] == 0:
                    print(action.text_)
                    pass
    print()
    return current_location.choice_action()


def show_result(current_location, action):
    if isinstance(action, Action):
        for i in current_location.results_:
            if i.number_ == int(action.results_):
                result = i
        print(result.text_)
        current_location.how_much_time_results_[result.number_ - 1] += 1
        return


def choice_action(current_location):
    while True:
        action = input()
        for i in current_location.actions_:
            if action == i.text_:
                current_location.how_much_time_actions_[i.numb_ - 1] += 1
                return current_location.show_result(i)
        else:
            pass




input("Добро пожаловать! Чтобы начать игру нажмите 'Enter'")
#input("Правила игры:\nЧтобы выполнить действие, напишите его в консоль\nЧтобы читать текст дальше, нажимайте 'Enter'")
read_first_info()
read_prologue()
read_locations()
read_epilogue()
game = game_tmp
player = Player()
#game.show_prologue()
play()







#game.show_epilogue()
