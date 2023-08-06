class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def get(self):
        return (self.x, self.y)

class Vector3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def get(self):
        return (self.x, self.y, self.z)

def lerp(a, b, t):
    return a + (b - a) * t