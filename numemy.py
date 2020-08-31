
class Numemy:
    def __init__(self, start_val, coins, speed):
        self.value = start_val
        self.coins = coins
        self.speed = speed
        pass

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
