import pygame
import random
import menu_flap

pygame.init()
pygame.display.set_caption('Flappy bird')
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
paused = False
hiscore = 0

class Ground:
    def __init__(self, x):
        self.ground = pygame.image.load('ground.png')
        self.x = x
        self.speed = 3

    def show_ground(self):
        self.x -= self.speed
        ground_rect = self.ground.get_rect(topleft=(self.x, height - 20))
        screen.blit(self.ground, ground_rect)

    def get_x(self):
        return self.x


class Cloud:
    def __init__(self, x):
        cloud_names = ['cloud1.png', 'cloud2.png', 'cloud3.png', 'cloud4.png', 'cloud5.png', 'cloud6.png']
        clouds = []
        for name in cloud_names:
            clouds.append(pygame.image.load(name))
        self.speed = 1
        self.cloud_x = x
        self.cloud_y = random.randint(0, int(height/3))
        self.cloud = clouds[random.randint(0, 5)]
        self.cloud_rect = self.cloud.get_rect(topleft=(self.cloud_x, self.cloud_y))

    def move(self):
        self.cloud_x -= self.speed
        self.cloud_rect = self.cloud.get_rect(topleft=(self.cloud_x, self.cloud_y))

    def show_cloud(self):
        screen.blit(self.cloud, self.cloud_rect)

    def get_x(self):
        return self.cloud_x


class Bird:
    def __init__(self):
        self.speed = -100
        self.gravity = 10
        self.pos = self.width, self.height = width/4, height/2
        self.bird_img = pygame.image.load('bird.png')
        self.bird_img.set_colorkey((0, 0, 255))
        self.bird_rect = self.bird_img.get_rect(topleft=self.pos)

    def flap(self):
        if self.speed <= 200:
            self.speed -= 120

    def fall_down(self):
        self.bird_img = pygame.transform.rotate(self.bird_img, -45)

    def move(self):
        if self.height + self.speed*0.05 + (self.gravity*0.5) <= 20:
            self.speed = 10
            self.bird_rect = self.bird_img.get_rect(topleft=(self.width, self.height))
        else:
            self.height = self.height + self.speed*0.05 + (self.gravity*0.5)
            self.speed += self.gravity*0.5
            self.bird_rect = self.bird_img.get_rect(topleft=(self.width, self.height))

    def get_pos(self):
        pos = int(self.width), int(self.height)
        return pos

    def draw_bird(self):
        screen.blit(self.bird_img, self.bird_rect)


class Pipe:
    def __init__(self, x):
        self.hole_size = 100
        self.hole_height = random.randint(self.hole_size, height-self.hole_size-20)
        self.lower_pipe = pygame.image.load('pipe_lower.png')
        self.upper_pipe = pygame.image.load('pipe_upper.png')
        self.pipes_x = x
        self.lp_y = self.hole_height + self.hole_size
        self.up_y = self.hole_height-834
        self.speed = 3
        self.lower_pipe_rect = self.lower_pipe.get_rect(topleft=(self.pipes_x, self.lp_y))
        self.upper_pipe_rect = self.upper_pipe.get_rect(topleft=(self.pipes_x, self.up_y))
        self.scored = False

    def move(self):
        self.pipes_x -= self.speed
        self.lower_pipe_rect = self.lower_pipe.get_rect(topleft=(self.pipes_x, self.lp_y))
        self.upper_pipe_rect = self.upper_pipe.get_rect(topleft=(self.pipes_x, self.up_y))

    def show_pipes(self):
        screen.blit(self.upper_pipe, self.upper_pipe_rect)
        screen.blit(self.lower_pipe, self.lower_pipe_rect)

    def get_x(self):
        return self.pipes_x
    # if self.pipes_x <= -113:
    #     self.pipes_x = width
    #     self.hole_height = random.randint(50, height - 50)

    def __del__(self):
        pass


def mouse_clicked(birdie):
    birdie.flap()


def check_landing(birdie):
    if birdie.get_pos()[1] >= 680:
        global running
        running = False


def upd():
    screen.fill((0, 0, 255))
    for c in range(len(cloud)):
        cloud[c].move()
        cloud[c].show_cloud()
        if cloud[c].get_x() <= -120:
            cloud[c] = Cloud(1000)
    for p in range(len(pipe)):
        pipe[p].move()
        pipe[p].show_pipes()
        if pipe[p].get_x() <= -113:
            pipe[p] = Pipe(1000)
    score(bird, pipe)
    for g in range(len(ground)):
        if ground[g].get_x() <= -999:
            ground[g] = Ground(999)
        ground[g].show_ground()
    bird.move()
    bird.draw_bird()
    check_landing(bird)
    collision(bird, pipe)
    pygame.display.flip()


def collision(bird, pipes):
    for p in pipes:
        if p.lower_pipe_rect.colliderect(bird.bird_rect) or p.upper_pipe_rect.colliderect(bird.bird_rect):
            bird.bird_img = pygame.image.load('bird_down.png')
            bird.gravity = 25
            bird.fall_down()


def score(bird, pipes):
    global hiscore
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(hiscore), True, (255, 0, 0), (0, 0, 255))
    text.set_colorkey((0, 0, 255))
    text_rect = text.get_rect(topleft=(width - 60, 20))
    for p in pipes:
        # print(bird.width, p.upper_pipe_rect[0])
        if int(bird.width+bird.bird_rect[2]) > p.upper_pipe_rect[0] and not p.scored:
            hiscore += 1
            p.scored = True
            text = font.render(str(hiscore), True, (0, 255, 0), (0, 0, 255))
            text_rect = text.get_rect(topleft=(width - 20, 20))
    screen.blit(text, text_rect)


cloud = [Cloud(i*50) for i in range(1, 20)]
pipe = [Pipe(300+i*350) for i in range(1, 4)]
ground = [Ground(i*1000) for i in range(0, 2)]
bird = Bird()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        if not paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked(bird)
    if paused:
        pass
    else:
        upd()
    clock.tick(60)


