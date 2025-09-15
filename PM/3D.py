from random import randint, uniform
from ursina import * # 00
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina() # 00

player = FirstPersonController( # 01 veidojām spēlētāju ar visām kustībām, w, a, s, d taustiņi un space lekšanai strādā
    height=2,
    speed = 10,
    collider = 'box'
    #jump_height = 10
)

ground = Entity( # 04 veidojām zemi
    model = 'cube', 
    texture = 'assets\grass.jpg',
    collider = 'box', # kolizijas veidi = box (vienkāršākā), mesh (sarežģītākā)
    scale = (100, 1, 100)
)

lvl = 1
sky = Sky() # 00 debesis

#window.fullscreen = True # 05 pilnā ekrāna režīms

blocks = []
directions = []
colors =[color.azure, color.red, color.orange, color.blue, color.green, color.yellow, color.pink]
for i in range(10):
    r = uniform(-2, 2)
    block = Entity(
        position = (r, 1+i, 3 + i*5),
        model = 'cube',
        #texture = 'white_cube',
        texture = 'assets/floor.jpg',
        color = colors[randint(0, len(colors)-1)],
        scale = (5, 0.5, 5),
        collider = 'box'
    )
    blocks.append(block)
    if r < 0: 
        directions.append(1)
    else:
        directions.append(-1)

goal = Entity( # pēdējais pakāpiens
    model = 'cube',
    color = color.white,
    #texture = 'white_cube',
    texture = 'assets\grass.jpg',
    position = (0, 11, 55),
    scale = (10, 1, 10),
    collider = 'box'
)

pillar = Entity(
    color = color.green,
    model = 'cube',
    texture = 'assets\grass.jpg',
    position = (0, 36, 58),
    scale = (1, 50, 1)
)

mySphere = Entity(
    color = color.gold,
    model = 'sphere',
    texture = 'assets\grass.jpg',
    position = (0, 60, 58),
    scale = (7, 7, 7)
)

myText = Text(
    text = lvl,
    origin = (13, -17),
    color = color.white
)

myGun = Entity(
    color = color.gold,
    parent = camera.ui,
    model = 'weapon.glb',
    position = (0.35, -0.4), 
    rotation= (-20,-20,0),
    #texture = 'assets/grass.jpg',
    scale =0.3,
    flip_faces=True
)

class Target(Button):
    def __init__(self, x, y, z):
        super().__init__(
            color = color.gold,
            #texture = 'assets/floor.jpg',
            parent = scene,
            model = 'bmw.glb',
            scale = 1,
            position = (x,y,z),
            rotation = (0, -90, 0),
            collider = 'mesh'
        )

block = Entity(
    position = (20, 0.5, 20),
    model = 'bmw.glb',
    color = colors[randint(0, len(colors)-1)],
    scale = (2, 2, 2),
    collider = 'mesh'
)

num = 7
targets = [None]*num
for i in range(num):
    tx = uniform(-50, 50)
    ty = 0.5
    tz = uniform(0, 50)
    targets[i]=Target(tx, ty, tz)
    targets[i].animate_x(tx+100, duration=10, loop=True)

walk = Audio( # 06 pieslēgt audio spēlē
    'assets\walking.mp3',
    loop = False, # lai audio neatkārtotos
    autoplay = False # lai nespēlē uzreiz, ieslēdzot spēli
)

jump = Audio( # 06 pieslēgt audio spēlē
    'assets\jumping.mp3',
    loop = False, # lai audio neatkārtotos
    autoplay = False # lai nespēlē uzreiz, ieslēdzot spēli
)

def update():
    global lvl
    i = 0
    for block in blocks:
        block.x -= directions[i] * time.dt
        if abs(block.x) > 5:
            directions[i] *= -1
        if block.intersects().hit:
            player.x -= directions[i]*time.dt
        i +=1
    if player.z > 56 and player.y > 10 and lvl == 1: 
        lvl = 2
        myText.text = lvl
        print(myText.text)
    sky.texture = 'sky_sunset'
    walking = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
    if walking and player.grounded:
        if not walk.playing:
            walk.play()
    else:
        if walk.playing:
            walk.stop()

def input(key): # 02 ja nospiests kāds taustiņš, šeit var programmēt darbības, kas notiks. 
    if key == 'escape' or key =='q': #'q': # 03 iziet no spēles, ja ir nospiests taustiņš q
        quit()
    if key == 'space':
        jump.play()
    if key == 'left mouse down':
        if not myGun.color == color.red:
            myGun.color = color.red
        else:
            if myGun.color == color.red:
                myGun.color = color.yellow
        for target in targets:
            if target.hovered:
                destroy(target)
            

app.run() # 00 palaižām spēles logu !