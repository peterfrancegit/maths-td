from enum import Enum


class GameState(Enum):
    IN_OPENING_SCENE = 0
    MAIN_MENU = 1
    IN_GAME = 2
    GAME_OVER = 3