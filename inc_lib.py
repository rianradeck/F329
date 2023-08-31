from numpy import sqrt, log

class Num:
    def __init__(self, val, inc = 0):
        self.value = val
        self.inc = inc

    def __add__(self, other):
        if not isinstance(other, Num):
            other = Num(other, 0)
        return Num(self.value + other.value, 
                   sqrt(self.inc ** 2 + other.inc ** 2))

    def __mul__(self, other):
        if not isinstance(other, Num):
            other = Num(other, 0)
        return Num(self.value * other.value,
                   sqrt((other.value * self.inc) ** 2 + (self.value * other.inc) ** 2))

    def __sub__(self, other):
        if not isinstance(other, Num):
            other = Num(other, 0)
        return Num(self.value - other.value,
                   sqrt(self.inc ** 2 + other.inc ** 2))
    
    def __truediv__(self, other):
        if not isinstance(other, Num):
            other = Num(other, 0)
        delfdely = self.value / other.value ** 2
        return Num(self.value / other.value,
                   sqrt((self.inc / other.value) ** 2 + (delfdely * other.inc) ** 2))

    def __pow__(self, other):
        if not isinstance(other, Num):
            other = Num(other, 0)
        delfdelx = other.value * self.value ** (other.value - 1)
        delfdely = self.value ** other.value * log(abs(self.value))
        return Num(self.value ** other.value, 
                   sqrt((delfdelx * self.inc) ** 2 +
                        (delfdely * other.inc) ** 2))
    
    def conjugate(self):
        return self

    def sqrt(self):
        return self ** 0.5

    def __str__(self):
        return f"{self.value} ± {self.inc}"
    
    def __repr__(self):
        return f"{self.value} ± {self.inc}"
