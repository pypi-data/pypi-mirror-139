class Color:
    def __init__(self, r, g, b, a = 255):
        self.r, self.g, self.b, self.a = r, g, b, a

    def get(self):
        return (self.r, self.g, self.b, self.a)