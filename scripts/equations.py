from math import sqrt
from random import randint


class Equations():
    def __init__(self) -> None:
        self.update()
        pass

    def root_search(self, b, c):
        self.discr = b ** 2 - 4 * 1 * c
        if self.discr > 0:
            x1 = (-b + sqrt(self.discr)) / (2 * 1)
            x2 = (-b - sqrt(self.discr)) / (2 * 1)
            return x1, x2
        elif self.discr == 0:
            x = -b / (2 * 1)
            return x
        else:
            return False

    def update(self):
        self.c1 = randint(1, 30)
        self.c2 = randint(1, 30)
        self.equation = f"x²+{self.c1}x+{self.c2}=0"
        self.roots = self.root_search(self.c1, self.c2)
        if self.roots is False:
            self.update()
            return
        else:
            try:
                self.roots[0]
                self.roots[1]
                if (
                    (self.roots[0].is_integer()) is False
                    or (self.roots[1].is_integer()) is False
                ):
                    self.update()
            except Exception:
                self.update()
                return

    def get_equation(self) -> tuple:
        return self.equation, self.discr, self.roots[0], self.roots[1]
