class AngledVector3D:
    x: float  # degrees
    y: float  # degrees
    value: float

    def __init__(self, x: float, y: float, value: float):
        self.x = x
        self.y = y
        self.value = value
