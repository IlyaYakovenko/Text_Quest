from Code.gameplay import read_epilogue, read_prologue, read_locations, read_first_info, game, play

if __name__ == '__main__':
    input("Добро пожаловать! Чтобы начать игру нажмите 'Enter'")
    input("Правила игры:\nЧтобы выполнить действие, напишите его в консоль\nЧтобы читать текст дальше, нажимайте 'Enter'")
    read_first_info()
    read_prologue()
    read_locations()
    read_epilogue()
    game.play_music(game.music_)
    play()
