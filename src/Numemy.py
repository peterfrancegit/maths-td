from Square import Square
import pygame


class Numemy(Square):
    # 'value' is the current health of the Numemy, initiated at
    # 'start_val'; 'coins' is added to player wealth when Numemy
    # is killed; 'speed' is movement speed; 'square' is the current
    # location, initiated at 'spawn_square'.
    def __init__(self, surface, start_val, coins, speed, weight):
        Square.__init__(self, surface)
        self.value = start_val
        self.coins = coins
        self.speed = speed
        self.location = None
        self.weight = weight

    def next_square(self, grid):
        """Returns the next square on the route from a starting square"""
        if len(grid.route_dict[self.location]) == 1:
            return grid.route_dict[self.location][0]
        else:
            return grid.route_dict[self.location][1]

    # For when a Numemy reaches the exit_square
    def escape(self, grid):
        grid.lives -= self.weight
        sqr = grid.square_grid[self.location[0]][self.location[1]]
        surface = pygame.Rect(sqr.surface.x, sqr.surface.y, sqr.surface.width, sqr.surface.height)
        greySqr = Square(surface)
        grid.square_grid[self.location[0]][self.location[1]] = greySqr 
        del self

    def take_damage(self, operation, damage):
        """When a Numemy is hit"""
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
