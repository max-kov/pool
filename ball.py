friction_coeff = 0.994


class Ball():
    def __init__(self, ball_mass, planet_x, planet_y,is_striped,color,number,number_text):
        self.mass = ball_mass
        self.x = planet_x
        self.y = planet_y
        self.dx = 0
        self.dy = 0
        self.size = ball_mass
        self.is_striped = is_striped
        self.color = color
        self.number = number
        self.number_info = number_text

    def move_to(self,gameState, pos_x, pos_y):
        gameState.canvas.delete_ball(gameState,self)

        self.x = pos_x
        self.y = pos_y

        gameState.canvas.draw_ball(gameState, self)

    def add_force(self, delta_x, delta_y):
        self.dx += delta_x / self.mass
        self.dy += delta_y / self.mass

    def move_once(self,gameState, scale=1):
        tempx = self.x + self.dx*scale
        tempy = self.y + self.dy*scale
        self.move_to(gameState,tempx, tempy)
        self.dx = self.dx*friction_coeff
        self.dy = self.dy*friction_coeff

        if abs(self.dy)<0.01:
            self.dy = 0

        if abs(self.dx) < 0.01:
            self.dx = 0

    def set_vector(self, delta_x, delta_y):
        self.dx = delta_x
        self.dy = delta_y

    def destroy(self,gameState):
        gameState.canvas.delete_ball(gameState,self)