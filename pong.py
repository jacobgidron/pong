import numpy as np
from ursina import *

score = Vec2(0, 0)
score_flag = False

class Ball(Entity):
    ball_num = 1
    currnt_balls =0

    def __init__(self, add_to_scene_entities=True, speed=None, **kwargs):
        Ball.currnt_balls += 1
        self.speed = Vec3(0, 0, 0) if speed == None else Vec3(*speed)
        # self.speed = Vec3(3, 1.2, 0)
        self.acc = Vec3(0, 0, 0)
        super().__init__(add_to_scene_entities, **kwargs)

    def update(self):
        global score_flag
        # self.speed += self.acc
        h = self.intersects()
        if h:
            # print(f"world norm = {h.world_normal}"
            #       f"normal = {h.normal}"
            #       f"speed = {self.speed}"
            #       f"orth speed ={self.speed.project(h.world_normal.cross((0,0,1)))}")
            self.speed = -self.speed.project(h.world_normal) + self.speed.project(h.normal.cross((0, 0, 1)))
            # self.speed += 2*h.world_normal * self.speed
            # print(f"new speed = {self.speed}")
            # print(h.hit ,'\n',
            #     h.entity ,'\n',
            #     h.point ,'\n',
            #     h.world_point, '\n',
            #     h.distance, '\n',
            #     h.normal ,'\n',
            #     h.world_normal, '\n',
            #     h.hits,'\n',
            #     h.entities)
        self.position += self.speed * time.dt
        if not -8 < self.x < 8:
            global score
            score += (-8 < self.x, self.x < 8)

            if Ball.ball_num >= Ball.currnt_balls :
                score_flag = True
                self.position = Vec3(0,0,0)

# Text.default_resolution = 1080 * Text.size

info = Text(text="A powerful waterfall roaring on the mountains", scale = 20 ,origin = (0,-4))
app = Ursina()
ball = Ball(
    position=(0, 0, 0),
    scale=(0.5, 0.5, 0.5),
    model="sphere",
    color=color.black,
    collider='sphere',
    speed=(3, 1, 0)
)

player1 = Entity(
    position=(-7, 0, 0),
    scale=(0.5, 1.5, 1),
    model="cube",
    color=color.orange,
    collider='box',
    texture='white_cube'
)
player2 = Entity(
    position=(7, 0, 0),
    scale=(0.5, 1.5, 1),
    model="cube",
    color=color.orange,
    collider='box',

    texture='white_cube'
)

wall_up = Entity(
    position=(0, 4, 0),
    scale=(14, 1, 1),
    model="cube",
    color=color.white,
    collider='box'
)
wall_down = Entity(
    position=(0, -3, 0),
    scale=(14, 1, 1),
    model="cube",
    color=color.white,
    collider='box'
)

def update():
    global score_flag
    global score
    temp1 = held_keys['w'] - held_keys['s']
    h1 = player1.intersects()
    if h1.hit and not (-3 < player1.y + temp1 < 3):
        temp1 = 0
    player1.y += 1.5 * temp1 * time.dt
    # player2.x += held_keys['d'] * 0.1 - held_keys['a'] * 0.1
    temp2 = held_keys['up arrow'] - held_keys['down arrow']
    h2 = player1.intersects()
    if h1.hit and not (-3 < player2.y + temp2 < 3):
        temp2 = 0
    player2.y += 1.5 * temp2 * time.dt

    if score_flag:
        info.text = f"{int(score[0])} : {int(score[1])}"
        score_flag = False


app.run()
