from playsound import playsound


#class Item:
 #   def __init__(self, name, typee):
  #      self.name_ = name
   #     self.type_ = typee


class Player:
    current_location_ = 0

    def __init__(self, hp=100, score=0, hunger=0):
        self.hp_ = hp
        self.score_ = score
        self.slot1_ = ''
        self.slot2_ = ''
        self.slot3_ = ''
        self.hunger_ = hunger


class Enemy:
    def __init__(self, name, damage, hp):
        self.name_ = name
        self.hp_ = hp
        self.damage_ = damage


class Weapon:
    def __init__(self, name, damage):
        self.name_ = name
        self.damage_ = damage


class Location:
    how_much_time_actions_ = [0] * 100
    how_much_time_results_ = [0] * 100

    def __init__(self, number, description, actions, results, name):
        self.number_ = number
        self.description_ = description
        self.actions_ = actions
        self.results_ = results
        self.name_ = name


class Action:
    def __init__(self, number, text, results, condition, condition_type, time):
        self.numb_ = number
        self.text_ = text
        self.results_ = results
        self.condition_ = condition
        self.time_ = time
        self.condition_type_ = condition_type


class ActionWithRandomResult(Action):
    def __init__(self, chances, number, text, results, condition, condition_type, time):
        super().__init__(number, text, results, condition, condition_type, time)
        self.chances_ = chances


class ActionWithRepeatedResult(Action):
    def __init__(self, attempts, number, text, results, condition, condition_type, time):
        super().__init__(number, text, results, condition, condition_type, time)
        self.attempts_ = attempts


class ActionWithItemResult(Action):
    def __init__(self, item, number, text, results, condition, condition_type, time):
        super().__init__(number, text, results, condition, condition_type, time)
        self.item_ = item


class Result:
    def __init__(self, number, text, item, item_action, hp, hunger, score, time):
        self.number_ = number
        self.text_ = text
        self.item_ = item
        self.item_action_ = item_action
        self.hp_ = hp
        self.hunger_ = hunger
        self.score_ = score
        self.time_ = time


class LocationResult(Result):
    def __init__(self, number, text, item, item_action, hp, hunger, score, time, location):
        super().__init__(number, text, item, item_action, hp, hunger, score, time)
        self.location_ = location


class FightResult(Result):
    def __init__(self, number, text, item, item_action, hp, hunger, score, time, fight):
        super().__init__(number, text, item, item_action, hp, hunger, score, time)
        self.fight_ = fight


class EndGameResult(Result):
    def __init__(self, number, text, item, item_action, hp, hunger, score, time, endgame):
        super().__init__(number, text, item, item_action, hp, hunger, score, time)
        self.endgame_ = endgame


class Game:
    items_ = []
    weapons_ = []
    enemies_ = []
    locations_ = []
    music_ = ''
    prologue_ = []
    epilogue_ = []

    def play_music(self, music):
        playsound(music, False)

    def show_prologue(self):
        for line in self.prologue_:
            print(line, end='')
            input()

    def show_epilogue(self):
        for line in self.epilogue_:
            print(line, end='')
            input()

