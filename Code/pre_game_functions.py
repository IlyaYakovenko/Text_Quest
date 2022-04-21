from Code.classes import *
import argparse
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument('scenario')
args = parser.parse_args()
path_scenario = Path("Scenarios", args.scenario)
scenario = open(path_scenario)
#scenario = open('scenario.txt')

game = Game()
player = Player()

def read_first_info():  # Анализирует сценарий до пролога
    all_weapons = []
    all_enemies = []
    item_flag = False
    enemy_flag = False
    music_flag = False
    for line in scenario:
        if line != '\n':
            if line == 'Пролог:\n':
                break
            if line == 'Оружие:\n':
                item_flag = True
                continue
            if line == 'Враги:\n':
                enemy_flag = True
                item_flag = False
                continue
            if line == 'Музыка:\n':
                music_flag = True
                enemy_flag = False
                continue
            if item_flag:
                line = line.rstrip()
                currline = line.split('@')
                weapon = Weapon(currline[0], int(currline[1]))
                all_weapons.append(weapon)
            if enemy_flag:
                line = line.rstrip()
                currline = line.split('@')
                enemy = Enemy(currline[0], int(currline[1]), int(currline[2]))
                all_enemies.append(enemy)
            if music_flag:
                music = line.rstrip()
    music_path = Path("Music", music)
    game.music_ = music_path
    game.enemies_ = all_enemies
    game.weapons_ = all_weapons


def read_prologue():
    prologue = []
    for line in scenario:
        if line == '\n':
            break
        prologue.append(line.rstrip())
        game.prologue_ = prologue


def read_locations():
    for line in scenario:
        if line != '\n':
            if line == 'Эпилог:\n':
                break
            if line == '-----\n':
                game.locations_.append(location)
                continue
            if line[0:7] == 'Локация':
                line = line.rstrip()
                loc_name = line.split(':')[1]
                loc_int = line.split(':')[0].split(' ')
                location = Location(int(loc_int[1]), '', [], [], loc_name)
                description_flag = False
                actions_flag = False
                results_flag = False
            if line == 'Описание:\n':
                description_flag = True
                continue
            if line == 'Действия:\n':
                description_flag = False
                actions_flag = True
                continue
            if line == 'Результаты:\n':
                results_flag = True
                actions_flag = False
                continue
            if description_flag:
                line = line.rstrip()
                location.description_ = line
            if actions_flag:
                line = line.rstrip()
                curr_action = line.split('@')
                item_flag = False
                random_flag = False
                repeat_flag = False
                condition_flag = False
                time_flag = False
                if line.find('item') != -1:
                    item_flag = True
                if line.find('repeat') != -1:
                    repeat_flag = True
                if line.find('random') != -1:
                    random_flag = True
                if line.find('time') != -1:
                    time_flag = True
                if line.find('if') != -1:
                    condition_flag = True
                res = curr_action[2].split(';')
                both = True
                time = 999999999
                condition = -1
                condition_type = ''
                if time_flag and condition_flag:
                    time = curr_action[-1].split(' ')[1]
                    condition = curr_action[-2].split(' ')[1]
                    condition_type = curr_action[-2].split(' ')[0]
                    both = False
                if time_flag and both:
                    time = curr_action[-1].split(' ')[1]
                if condition_flag and both:
                    condition = curr_action[-1].split(' ')[1]
                    condition_type = curr_action[-1].split(' ')[0]
                if random_flag:
                    results = res[0].split(' ')[1:]
                    chances = res[1].split(' ')
                    action = ActionWithRandomResult(chances, int(curr_action[0]), curr_action[1], results, condition, condition_type, time)
                    location.actions_.append(action)
                    continue
                if item_flag:
                    item = res[0].split(':')[1]
                    results = res[1].split(' ')
                    action = ActionWithItemResult(item, int(curr_action[0]), curr_action[1], results, condition, condition_type, time)
                    location.actions_.append(action)
                    continue
                if repeat_flag:
                    results = res[1].split(' ')
                    attempts = res[0].split(' ')[1]
                    action = ActionWithRepeatedResult(attempts, int(curr_action[0]), curr_action[1], results, condition, condition_type, time)
                    location.actions_.append(action)
                    continue
                action = Action(int(curr_action[0]), curr_action[1], curr_action[2], condition, condition_type, time)
                location.actions_.append(action)
            if results_flag:
                line = line.rstrip()
                curr_result = line.split('@')
                loc_flag = False
                fight_flag = False
                endgame_flag = False
                time_flag = False
                time = 999999999
                item_action = ''
                item = ''
                score_amount = 0
                hp_amount = 0
                hunger_amount = 0
                if line.find('location') != -1:
                    loc_flag = True
                if line.find('fight') != -1:
                    fight_flag = True
                if line.find('endgame') != -1:
                    endgame_flag = True
                if line.find('time') != -1:
                    time_flag = True
                if time_flag:
                    time = curr_result[-1].split(' ')[1]
                for k in range(len(curr_result)):
                    if curr_result[k].find('item') != -1:
                        if curr_result[k].find('+') != -1:
                            item_action = '+'
                            item = curr_result[k].split('+')[1]
                        if curr_result[k].find('-') != -1:
                            item_action = '-'
                            item = curr_result[k].split('-')[1]
                    if curr_result[k].find('score') != -1:
                        score_amount = curr_result[k].split(' ')[1]
                    if curr_result[k].find('hp') != -1:
                        hp_amount = curr_result[k].split(' ')[1]
                    if curr_result[k].find('hunger') != -1:
                        hunger_amount = curr_result[k].split(' ')[1]
                if loc_flag:
                    location_to = curr_result[2].split(' ')[1]
                    result = LocationResult(int(curr_result[0]), curr_result[1], item, item_action, hp_amount, hunger_amount, score_amount, time, location_to)
                    location.results_.append(result)
                   # print(result.number_, result.text_, result.location_, result.hp_, result.score_, result.hunger_, result.item_action_, result.item_,result.time_)
                    continue
                if fight_flag:
                    fight = curr_result[2].split(':')[1]
                    result = FightResult(int(curr_result[0]), curr_result[1], item, item_action, hp_amount, hunger_amount, score_amount, time, fight)
                    location.results_.append(result)
                   # print(result.number_, result.text_, result.fight_, result.hp_, result.score_, result.hunger_,
                      #    result.item_action_, result.item_, result.time_)
                    continue
                if endgame_flag:
                    result = EndGameResult(int(curr_result[0]), curr_result[1], item, item_action, hp_amount, hunger_amount, score_amount, time, True)
                    location.results_.append(result)
                   # print(result.number_, result.text_, result.endgame_, result.hp_, result.score_, result.hunger_,
                       #   result.item_action_, result.item_, result.time_)
                    continue
                result = Result(int(curr_result[0]), curr_result[1], item, item_action, hp_amount, hunger_amount, score_amount, time)
                location.results_.append(result)
               # print(result.number_, result.text_, result.hp_, result.score_, result.hunger_,
                      #result.item_action_, result.item_, result.time_)


def read_epilogue():
    epilogue = []
    for line in scenario:
        if line == '\n':
            break
        epilogue.append(line.rstrip())
        game.epilogue_ = epilogue
    scenario.close()
