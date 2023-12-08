class Vector3D:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return Vector3D(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x + other, self.y + other, self.z + other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        raise ArithmeticError()

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x - other, self.y - other, self.z - other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        raise ArithmeticError()

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)
        raise ArithmeticError()

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x / other, self.y / other, self.z / other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)
        raise ArithmeticError()

    def __floordiv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x // other, self.y // other, self.z // other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x // other.x, self.y // other.y, self.z // other.z)
        raise ArithmeticError()

    def __mod__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x % other, self.y % other, self.z % other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x % other.x, self.y % other.y, self.z % other.z)
        raise ArithmeticError()

    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3D(self.x ** other, self.y ** other, self.z ** other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        raise ArithmeticError()

    def __pos__(self):
        return Vector3D(+self.x, +self.y, +self.z)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __rfloordiv__(self, other):
        return self.__floordiv__(other)

    def __rmod__(self, other):
        return self.__mod__(other)

    def __rpow__(self, other):
        return self.__pow__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __ifloordiv__(self, other):
        return self.__floordiv__(other)

    def __imod__(self, other):
        return self.__mod__(other)

    def __ipow__(self, other):
        return self.__pow__(other)

    @staticmethod
    def zero():
        return Vector3D(0, 0, 0)

    @staticmethod
    def right():
        return Vector3D(1, 0, 0)

    @staticmethod
    def left():
        return Vector3D(-1, 0, 0)

    @staticmethod
    def forward():
        return Vector3D(0, 1, 0)

    @staticmethod
    def backwards():
        return Vector3D(0, -1, 0)

    @staticmethod
    def up():
        return Vector3D(0, 0, 1)

    @staticmethod
    def down():
        return Vector3D(0, 0, -1)
