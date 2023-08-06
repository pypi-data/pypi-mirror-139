def add(num1, num2):
    return num1 + num2


def sub(num1, num2):
    return num1 - num2


def mult(num1, num2):
    return num1 * num2


def div(num1, num2):
    return num1 / num2


class JaiMataDi:
    def __init__(self, name, age, roll):
        self.name = name
        self.age = age
        self.roll = roll

    def get_name(self):
        return self.name

    def get_all(self):
        return [self.name, self.roll, self.age]
