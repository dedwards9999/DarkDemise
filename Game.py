from ursina import *

global door
global player
global playerGun
global reset

def createRandomizedLevelList():
    size = 50
    basicEmptyLevelList = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            if i == 0 or j == 0 or i == size-1 or j == size-1:
                basicEmptyLevelList[i][j] = 1
    basicEmptyLevelList[0][1] = 2
    basicEmptyLevelList[size-1][size-2] = 3
    # first run for the horizontals
    wallDividerHorizontal = random.randint(5,10)
    maxDownwardBreakthroughs = 0
    for i in range(wallDividerHorizontal,size-2,wallDividerHorizontal):
        maxDownwardBreakthroughs+=1
        for j in range(size):
            basicEmptyLevelList[i][j] = 1
    # second run for the verticals
    wallDividerVertical = random.randint(5, 10)
    maxRightBreakthroughs = 0
    for i in range(size):
        for j in range(wallDividerVertical,size-2,wallDividerVertical):
            basicEmptyLevelList[i][j] = 1
            if i == 0:
                maxRightBreakthroughs+=1

    verticalBreakthroughs = 0
    horizontalBreakthroughs = 0
    savedHorizontalSpot = 2
    savedVerticalSpot = 2
    savedHorizontalLimit = 2
    savedVerticalLimit = 2

    while verticalBreakthroughs < maxDownwardBreakthroughs or horizontalBreakthroughs < maxRightBreakthroughs:
        if verticalBreakthroughs >= maxDownwardBreakthroughs:
            breakToTheRight = True
        elif horizontalBreakthroughs >= maxRightBreakthroughs:
            breakToTheRight = False
        else:
            breakToTheRight = random.choice([True, False])
        if breakToTheRight:
            for i in range(savedVerticalSpot, size):
                if basicEmptyLevelList[i][savedHorizontalSpot] == 1:
                    savedVerticalLimit = i
                    break
            for i in range(savedHorizontalSpot,size):
                if basicEmptyLevelList[savedVerticalSpot][i] == 1:
                    savedHorizontalLimit = i
                    break
            savedVerticalSpot = savedVerticalLimit-random.randint(1,3)
            savedHorizontalSpot = savedHorizontalLimit
            basicEmptyLevelList[savedVerticalSpot][savedHorizontalSpot] = 0
            savedHorizontalSpot+=1
            horizontalBreakthroughs+=1
        else:
            for i in range(savedHorizontalSpot, size):
                if basicEmptyLevelList[savedVerticalSpot][i] == 1:
                    savedHorizontalLimit = i
                    break
            for i in range(savedVerticalSpot,size):
                if basicEmptyLevelList[i][savedHorizontalSpot] == 1:
                    savedVerticalLimit = i
                    break
            savedHorizontalSpot = savedHorizontalLimit-random.randint(1,3)
            savedVerticalSpot = savedVerticalLimit
            basicEmptyLevelList[savedVerticalSpot][savedHorizontalSpot] = 0
            savedVerticalSpot+=1
            verticalBreakthroughs+=1
    return basicEmptyLevelList


def createLevel(levelList):
    Entity(model='cube', position=(len(levelList) // 2, -1, (len(levelList) // 2)),
           scale=Vec3(len(levelList), 1, len(levelList)), texture='grass', collider='box')
    for i in range(len(levelList)):
        for j in range(len(levelList[i])):
            if levelList[i][j] == 1:
                Entity(model='cube', scale=Vec3(1, 2, 1), position=Vec3(i, 0, j), texture='brick', collider='box',
                       color=color.red)
            elif levelList[i][j] == 2:
                Entity(model='cube', scale=Vec3(1, 2, 1), position=Vec3(i, 0, j), texture='brick', collider='box', color=color.dark_gray)
            elif levelList[i][j] == 3:
                global door
                door = Entity(model='cube', scale=Vec3(1, 2, 1), position=Vec3(i, 0, j), texture='brick', collider='box', color=color.green)

def createNewLevel():
    scene.clear()
    levelList = createRandomizedLevelList()
    createLevel(levelList)


def createPlayer():
    global player
    player = Entity(model='cube',collider='box')
    player.position = (3, 2, 3)
    player.scale *= 0.2
    global playerGun
    playerGun = Sprite(model='quad',parent=camera.ui, texture='GunSprite.png', position=(0.25, -0.45), scale=(0.1, 0.1),)
    mouse.visible = False
    Entity(model='circle',parent=camera.ui ,position=(0,0),scale=(0.015,0.015), color=color.black)

def init():
    createNewLevel()
    createPlayer()

def shootGun():



def update():
    global reset
    global player
    camera.position = (player.x,player.y,player.z)
    mouse.position = (0,0)
    sensitivity = 50
    camera.rotation += (mouse.prev_y*-sensitivity, mouse.prev_x*sensitivity, 0)
    camera.rotation_x = clamp(camera.rotation_x, -85, 85)
    sideSpeed = 2
    forwardSpeed = 4
    move_dir = Vec3(0,0,0)
    if len(move_dir) > 0:
        move_dir = move_dir.normalized()
    if held_keys['shift']:
        forwardSpeed = 7
    if held_keys['w']:
        move_dir += camera.forward * forwardSpeed * time.dt
    if held_keys['s']:
        move_dir -= camera.forward * forwardSpeed * time.dt
    if held_keys['a']:
        move_dir -= camera.right * sideSpeed * time.dt
    if held_keys['d']:
        move_dir += camera.right * sideSpeed * time.dt
    player.position += move_dir
    if player.intersects(door):
        init()
    if player.intersects():
        player.position -= move_dir * 1.001
    player.y = 0.25
    if mouse.left():
        shootGun()

