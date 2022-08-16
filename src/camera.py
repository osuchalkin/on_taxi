class Camera:
    """отслеживает смещение спрайта"""
    def __init__(self):

        self.x = 5000
        self.y = 5000

    def set_position(self, x, y):
        self.x = x
        self.y = y
