
class Numemy:
    # 'value' is the current health of the NUmemy, initiated at
    # 'start_val'; 'coins' is added to player wealth when Numemy
    # is killed; 'speed' is movement speed; 'square' is the current
    # location, initiated at 'spawn_square'.
    def __init__(self, start_val, coins, speed, spawn_square):
        self.value = start_val
        self.coins = coins
        self.speed = speed
        self.square = spawn_square
        pass

    # Returns the next square on the route from a starting square.
    def next_square(self):
        global route_list
        return route_list[self.square][1]

    # Moves Numemy to next square in its route.
    def move(self):
        self.square = self.next_square()

    # Used when a Tower damages a Numemy.
    def take_damage(self, operation, damage):
        if operation == '+':
            self.value += damage
        elif operation == '-':
            self.value -= damage
        elif operation == '/':
            self.value /= damage
        elif operation == '*':
            self.value *= damage
        pass
