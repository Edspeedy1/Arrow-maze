import pygame, random,  time
pygame.init()

SCREENSIZE = 1200, 600
SCREEN = pygame.display.set_mode(SCREENSIZE)
GRIDSIZE = 8, 8
SQUARE = True

if SQUARE:
    RW, RL = 1080//GRIDSIZE[1],1920//(GRIDSIZE[0]+1)
    RL, RW = min(RL,RW),min(RL,RW)
else:
    RW, RL = 1080//GRIDSIZE[1],1920//(GRIDSIZE[0]+1)

def updateScreen(*surfaces):
    for i in surfaces:
        SCREEN.blit(pygame.transform.scale(i, SCREENSIZE), (0,0))
    pygame.display.update()

START = random.choice(((0,1),(1,0)))
END = [GRIDSIZE[0]-1, GRIDSIZE[1]-1]
GRID = [[[0] for i in range(GRIDSIZE[1])] for j in range(GRIDSIZE[0])]

baseImg = pygame.transform.scale(pygame.image.load('Arrow Maze\\Arrow.png'), (min(RL,RW),min(RL,RW)))
baseImg2 = pygame.transform.scale(pygame.image.load('Arrow Maze\\Arrow2.png'), (min(RL,RW),min(RL,RW)))
baseAImg = pygame.transform.scale(pygame.image.load('Arrow Maze\\ArrowA.png'), (min(RL,RW),min(RL,RW)))
baseAImg2 = pygame.transform.scale(pygame.image.load('Arrow Maze\\ArrowA2.png'), (min(RL,RW),min(RL,RW)))

imgSet = {
    (-2, 2):pygame.transform.rotate(baseAImg2,180),
    (-2, 0):pygame.transform.rotate(baseImg2,180),
    (-2, -2):pygame.transform.rotate(baseAImg2,90),
    (-1, 1):pygame.transform.rotate(baseAImg, 180),
    (-1, 0):pygame.transform.rotate(baseImg, 180),
    (-1, -1):pygame.transform.rotate(baseAImg, 90),
    (1, -1):pygame.transform.rotate(baseAImg, 0),
    (1, 0):pygame.transform.rotate(baseImg, 0),
    (1, 1):pygame.transform.rotate(baseAImg, -90),
    (2, -2):pygame.transform.rotate(baseAImg2,0),
    (2, 0):pygame.transform.rotate(baseImg2,0),
    (2, 2):pygame.transform.rotate(baseAImg2,-90),
    (0, 1):pygame.transform.rotate(baseImg, -90),
    (0, -1):pygame.transform.rotate(baseImg, 90),
    (0, 2):pygame.transform.rotate(baseImg2,-90),
    (0, -2):pygame.transform.rotate(baseImg2,90),
    (0,0):pygame.transform.scale(pygame.image.load('Arrow Maze\\EX.png'),(min(RL,RW),min(RL,RW)))
    }

def returnFlower(distance):
    options = []
    for i in range(1,distance+1):
        options += [(0,i),(0,-i)]
    for i in [i-distance+int(i-distance>=0) for i in range(distance*2)]:
        for j in range(3):
            options.append((i,i*[-1,0,1][j]))
    return options

def optionsInRange(options, head):
    o = options[:]
    for i in options:
        if i[0]+head[0] not in range(GRIDSIZE[0]) or i[1]+head[1] not in range(GRIDSIZE[1]):
            o.remove(i)
    return o

def checkOptions(options, head):
    o = options[:]
    for i in options:
        if GRID[i[0]+head[0]][i[1]+head[1]] != [0]:
            o.remove(i)
        else:
            for j in GRID[head[0]][head[1]][1:]:
                if sameDirection(i, j): o.remove(i)
    return o

def sameDirection(V1, V2):
    if V1 == (0)*len(V1) or V2 == (0)*len(V2):
        return True
    for j,i in enumerate(V2):
        if i != 0:
            guess = V1[j]/i
    for i in range(len(V2)):
        if V2[i]*guess != V1[i]: return False
    return True

def makeMaze():
    global GRID
    mazeScreen = pygame.surface.Surface((1920,1080))
    GRID = [[[0] for i in range(GRIDSIZE[1])] for j in range(GRIDSIZE[0])]
    stack = []
    head = [0,0]
    mazeScreen.fill((55,55,55))
    pygame.draw.rect(mazeScreen, (50,250,50), (0,0,RL,RW))
    running = True
    while running:
        options = checkOptions(optionsInRange(returnFlower(2), head), head)
        if len(options) > 0 and (random.randint(0, 5) != 0 or len(stack) <= 4):
            pick = random.choice(options)
            GRID[head[0]][head[1]].append(pick)
            pygame.draw.rect(mazeScreen, (0,0,0), ((head[0])*RL,(head[1])*RW,RL,RW), 5)
            mazeScreen.blit(imgSet[tuple(pick)], ((head[0])*RL,(head[1])*RW))
            head = [head[0]+pick[0],head[1]+pick[1]]
            stack.append(pick)
        else:
            if GRID[head[0]][head[1]] == [0]: 
                GRID[head[0]][head[1]].append((0,0))
                pygame.draw.rect(mazeScreen, (0,0,0), ((head[0])*RL,(head[1])*RW,RL,RW), 5)
                mazeScreen.blit(imgSet[(0,0)], ((head[0])*RL,(head[1])*RW))
            for _ in range(random.randint(2, 4)):
                try: pick = stack.pop()
                except: break
                head = [head[0]-pick[0],head[1]-pick[1]]
        if len(stack) == 0: running = False
    
    if GRID[GRIDSIZE[0]-1][GRIDSIZE[1]-1] == [0,(0,0)]:
        GRID[GRIDSIZE[0]-1][GRIDSIZE[1]-1] = [0]
        pygame.draw.rect(mazeScreen, (55,55,55), ((GRIDSIZE[0]-1)*RL,(GRIDSIZE[1]-1)*RW,RL,RW))
        pygame.draw.rect(mazeScreen, (0,0,0), ((GRIDSIZE[0]-1)*RL,(GRIDSIZE[1]-1)*RW,RL,RW),5)
    GRID[GRIDSIZE[0]-1][GRIDSIZE[1]-1].append((1,0))
    pygame.draw.rect(mazeScreen, (250,100,0), ((GRIDSIZE[0])*RL,(GRIDSIZE[1]-1)*RW,RL,RW))
    pygame.draw.rect(mazeScreen, (0,0,0), ((GRIDSIZE[0])*RL,(GRIDSIZE[1]-1)*RW,RL,RW),5)
    mazeScreen.blit(imgSet[(1,0)], ((GRIDSIZE[0]-1)*RL,(GRIDSIZE[1]-1)*RW))
    empty = []
    for i in range(GRIDSIZE[0]):
        for j in range(GRIDSIZE[1]):
            if GRID[i][j] == [0]:
                empty.append((i,j))
    if len(empty) > 2: 
        S = makeMaze()
        return S
    else: 
        for head in empty:
            direction = random.choice(optionsInRange(returnFlower(2), head))
            GRID[head[0]][head[1]].append(direction)
            pygame.draw.rect(mazeScreen, (0,0,0), ((head[0])*RL,(head[1])*RW,RL,RW), 5)
            mazeScreen.blit(imgSet[direction], ((head[0])*RL,(head[1])*RW))
    return mazeScreen


class playerClass:
    def __init__(self):
        self.gx = 0
        self.gy = 0
        self.x = RL/2
        self.y = RW/2
    def move(self, direction=None, position=None):
        if position:
            pick = position
        else:
            try: options = GRID[self.gx][self.gy][1:]
            except: 
                print('cant')
                return
            if direction == (False,False,False,False):
                pick = random.choice(options)
            else:
                V = (int(direction[0])-int(direction[1]), int(direction[3])-int(direction[2]))
                pick = (0,0)
                for i in options:
                    if sameDirection(i, V): pick = i
        self.gx += pick[0]
        self.gy += pick[1]
        self.x += RL*pick[0]
        self.y += RW*pick[1]

mazeScreen = makeMaze()
player = playerClass()
screenSurface = pygame.surface.Surface((1920,1080))
run=True
l,r,u,d = False,False,False,False
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    mazeScreen = makeMaze()
                    player.move(position=(-player.gx,-player.gy)) 
                if event.key == pygame.K_BACKSPACE:
                    player.move(position=(-player.gx,-player.gy))
                if event.key == pygame.K_RIGHT: r=True
                if event.key == pygame.K_LEFT: l=True
                if event.key == pygame.K_UP: u=True
                if event.key == pygame.K_DOWN: d=True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT: r=False
                if event.key == pygame.K_LEFT: l=False
                if event.key == pygame.K_UP: u=False
                if event.key == pygame.K_DOWN: d=False
                if event.key == pygame.K_SPACE:
                    player.move(direction=(r,l,u,d))
                if event.key == pygame.K_x:
                    player.move(direction=(r,l,u,d))
    screenSurface.blit(mazeScreen, (0,0))
    pygame.draw.circle(screenSurface, (0,100,200), (player.x,player.y), RL/7)
    updateScreen(screenSurface)
