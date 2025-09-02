import camera
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

def createRandomizedLevelList():
    size = 50
    basicEmptyLevelList = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            if i == 0 or j == 0 or i == size-1 or j == size-1:
                basicEmptyLevelList[i][j] = 1
    basicEmptyLevelList[0][1] = 2
    basicEmptyLevelList[size-1][size-2] = 2
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
    printTwoDimenisonalList(size, size, basicEmptyLevelList)
    return basicEmptyLevelList

def printTwoDimenisonalList(xm, ym, list):
    for i in range(xm):
        for j in range(ym):
            print(list[i][j], end='')
        print()

def createLevel(levelList):
    Entity(model='cube', position=(len(levelList) // 2, -1, (len(levelList) // 2)),
           scale=Vec3(len(levelList), 1, len(levelList)), texture='grass', collider='box')
    for i in range(len(levelList)):
        for j in range(len(levelList[i])):
            if levelList[i][j] == 1:
                Entity(model='cube', scale=Vec3(1, 1, 1), position=Vec3(i, 0, j), texture='brick', collider='box',
                       color=color.red)
            elif levelList[i][j] == 2:
                Entity(model='cube', scale=Vec3(1, 1, 1), position=Vec3(i, 0, j), texture='brick', collider='box', color=color.white)

def createNewLevel():
    scene.clear()
    levelList = createRandomizedLevelList()
    createLevel(levelList)


def init():
    createNewLevel()
    player = FirstPersonController()
    player.scale *= 0.25
    player.jump_height *= 0.5
    player.cursor.color = color.black
    player.cursor.scale *= 0.5

