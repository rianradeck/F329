from math import pi, sqrt

class ValNode:
    def __init__(self):
        self.primitives = set()
        self.op = None
        self.child = ()
    
    def get_value(x):
        if isinstance(x, ValNode):
            return x.value()
        return x

    def get_deriv(x, var):
        if isinstance(x, ValNode):
            return x.deriv(var)
        return 0

    def __neg__(self):
        ret = ValNode()
        ret.primitives = self.primitives
        ret.op = 'u-'
        ret.child = (self,)
        return ret

    def __add__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '+'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '+'
        ret.child = (self, other)
        return ret
    
    def __radd__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '+'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '+'
        ret.child = (self, other)
        return ret
    
    def __sub__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '-'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '-'
        ret.child = (self, other)
        return ret

    def __rsub__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return -self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '-'
                ret.child = (other, self)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '-'
        ret.child = (other, self)
        return ret

    def __mul__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return 0
            if other == 1:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '*'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '*'
        ret.child = (self, other)
        return ret

    def __rmul__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return 0
            if other == 1:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '*'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '*'
        ret.child = (self, other)
        return ret
    
    def __truediv__(self, other):
        if not isinstance(other, ValNode):
            if other == 1:
                return self
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '/'
                ret.child = (self, other)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '/'
        ret.child = (self, other)
        return ret

    def __rtruediv__(self, other):
        if not isinstance(other, ValNode):
            if other == 0:
                return 0
            else:
                ret = ValNode()
                ret.primitives = self.primitives
                ret.op = '/'
                ret.child = (other, self)
                return ret

        ret = ValNode()
        ret.primitives = set.union(self.primitives, other.primitives)
        ret.op = '/'
        ret.child = (other, self)
        return ret


    def deriv(self, var):
        if self.op == '+':
            return ValNode.get_deriv(self.child[0], var) + ValNode.get_deriv(self.child[1], var)
        elif self.op == '*':
            return ValNode.get_deriv(self.child[0], var) * self.child[1] + ValNode.get_deriv(self.child[1], var) * self.child[0]
        elif self.op == 'u-':
            return -ValNode.get_deriv(self.child[0], var)
        elif self.op == '-':
            return ValNode.get_deriv(self.child[0], var) - ValNode.get_deriv(self.child[1], var)
        elif self.op == '/':
            aux = ValNode.get_deriv(self.child[1], var)
            
            return ValNode.get_deriv(self.child[0], var) / self.child[1] - aux * self.child[0] / (self.child[1] * self.child[1])

    def value(self):
        if self.op == '+':
            return ValNode.get_value(self.child[0]) + ValNode.get_value(self.child[1])
        elif self.op == '*':
            return ValNode.get_value(self.child[0]) * ValNode.get_value(self.child[1])
        elif self.op == 'u-':
            return -ValNode.get_value(self.child[0])
        elif self.op == '-':
            return ValNode.get_value(self.child[0]) - ValNode.get_value(self.child[1])
        elif self.op == '/':
            return ValNode.get_value(self.child[0]) / ValNode.get_value(self.child[1])

    def __str__(self):
        if self.op == '+':
            return f"({self.child[0]} + {self.child[1]})"
        elif self.op == '*':
            return f"({self.child[0]} * {self.child[1]})"
        elif self.op == 'u-':
            return f"-({self.child[0]})"
        elif self.op == '-':
            return f"({self.child[0]} - {self.child[1]})"
        elif self.op == '/':
            return f"({self.child[0]} / {self.child[1]})"

    def unc(self):
        ret = 0
        for x in self.primitives:
            aux = self.deriv(x).value() * x.unc()
            ret += aux * aux
        return sqrt(ret)

class CValNode(ValNode):

    def __init__(self, cvalue, cunc = 0, name=""):
        super().__init__()
        self.primitives = {self}
        self.cvalue = cvalue
        self.name = name
        self.cunc = cunc

    def value(self):
        return self.cvalue

    def deriv(self, var):
        return 0 if var != self else 1

    def __str__(self):
        return self.name

    def unc(self):
        return self.cunc

r = CValNode(0.55e-2 / 2, 0.00010206207261596577, name="r")
l = CValNode(2.5e-2, 0.00020412414523193154, name="l")
m = CValNode(5.1863e-3, 2.886751345948129e-08, name="m")

mi = m * (r * r / 4 + l * l / 12) * 4 * pi * pi 
print(mi)
print(ValNode.get_value(mi))
print(mi.unc())
#print(ValNode.get_value(mi))
#print(mi.deriv(r))
#print(ValNode.get_value(mi.deriv(r)))
