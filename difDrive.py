import pygame
import math

class Envir:
    def __init__(self, dimensions):
        self.black = (0, 0, 0)
        self.yel = (255, 255, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

        # dimensions
        self.height = dimensions[0]
        self.width = dimensions[1]

        # Window
        pygame.display.set_caption("Differential Drive")
        self.map = pygame.display.set_mode((self.width, self.height))

        # text labels
        self.text="default"
        self.font=pygame.font.Font('freesansbold.ttf', 50)
        self.text=self.font.render('default', True, self.white, self.black)
        self.textRect = self.text.get_rect()
        self.textRect.center = (dimensions[1]-600, dimensions[0]-100)

        # trail
        self.trail_set=[]

    def write_info(self, Vl, Vr, theta):
        txt=f"Vl = {Vl} Vr = {Vr} theta = {int(math.degrees(theta))}"
        self.text = self.font.render(txt, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)

    def trail(self, pos):
        for i in range(0, len(self.trail_set) - 1):
            pygame.draw.line(self.map, self.yel, (self.trail_set[i][0], self.trail_set[i][1]), (self.trail_set[i+1][0], self.trail_set[i+1][1]))

        if self.trail_set.__sizeof__()>3000: # adjustable length of trail
            self.trail_set.pop(0)
        self.trail_set.append(pos)


class Robot:
    def __init__(self, startpos, robotImg, width):
        self.m2p=3779.52 # meters to pixels
        # robot dimensions
        self.w = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.theta = 0
        # wheel velocity
        self.vl = 0
        self.vr = 0
        # unused - can be implemented to limit movement
        self.maxspeed=0.02*self.m2p
        self.minspeed=-0.02*self.m2p

        # graphics
        self.img = pygame.image.load(robotImg)
        self.rotated=self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def draw(self, map):
        map.blit(self.rotated, self.rect)

    def move(self, event=None): # move using arrow keys to control individual wheel speed
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.vr += 0.001*self.m2p
                elif event.key == pygame.K_UP:
                    if self.vl == self.vr: # increase speed
                        self.vl += 0.001*self.m2p
                        self.vr += 0.001*self.m2p
                    else:
                        vel = max(self.vl, self.vr)
                        self.vr = vel
                        self.vl = vel
                elif event.key == pygame.K_RIGHT:
                    self.vl += 0.001*self.m2p
                elif event.key == pygame.K_DOWN:
                    if self.vl == self.vr: # decrease speed
                        self.vl -= 0.001*self.m2p
                        self.vr -= 0.001*self.m2p
                    else:
                        vel = min(self.vl, self.vr)
                        self.vr = vel
                        self.vl = vel
        self.x += ((self.vl + self.vr)/2)*math.cos(self.theta)*dt
        self.y -= ((self.vl + self.vr)/2)*math.sin(self.theta)*dt
        self.theta += (self.vr - self.vl)/self.w*dt

        if self.theta > 2*math.pi or self.theta < -2*math.pi:
            self.theta = 0

        self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

# init
pygame.init()

# start pos
start=(200,200)
# window
dims=(600,1200)

running=True
environment=Envir(dims)
robot=Robot(start,"./robot.png", 80)

dt = 0
last_time=pygame.time.get_ticks()

# simulation
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        robot.move(event) # move constantly at same speed
    dt = (pygame.time.get_ticks() - last_time)/1000
    last_time=pygame.time.get_ticks()
    pygame.display.update()
    environment.map.fill(environment.black)
    robot.move()
    environment.write_info(int(robot.vl), int(robot.vr), robot.theta)
    robot.draw(environment.map)
    environment.trail((robot.x, robot.y))