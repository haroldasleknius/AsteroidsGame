from Vector import Vector
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

NUM_ASTEROIDS = 8
MAX_SPEED = 1.6
HEIGHT = 800
WIDTH = 1000
PROJECTILE = []
DEL_PROJECTILE = []
DEL_ASTEROID = []
DEL_BALL = []
explosions = []
DEL_EXPLOSIONS = []
asteroid_spawn_time = 500
score = 0
lives = 3

def reduceLives():
    global lives 
    lives -= 1
def increaseScore():
    global score
    score += 1
def speedup():
    global asteroid_spawn_time 
    if asteroid_spawn_time > 250:
        asteroid_spawn_time -= 50
    
def vector_to_angle(vector):
    return math.atan2(vector.x, -(vector.y))

SHEET_URL = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/explosion-spritesheet.png"
SHEET_WIDTH = 900
SHEET_HEIGHT = 900
SHEET_COLUMNS = 9
SHEET_ROWS = 9

class Background:
    def __init__(self):
        self.image = simplegui.load_image('https://docs.google.com/uc?export=download&id=1tQeo9iJgQCEHzSyHdpzVprorkLqbBMU2')
        self.centreImage = (640,400)
        self.imageDims = (1280,800)
        self.centre = (WIDTH / 2, HEIGHT / 2)
        self.size = (WIDTH,HEIGHT)

    def draw(self,canvas):
        canvas.draw_image(self.image, self.centreImage, self.imageDims, self.centre,
                              self.size)        
   

class Explosions:
    def __init__(self, 
                 imgurl, 
                 width, height, 
                 columns, rows, pos):

        self.img = simplegui.load_image(imgurl)
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.num_frames = 74
        
        self.frame_width = width / columns
        self.frame_height = height / rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.pos = pos

        self.frame_index = [9, 0]

        
    def done(self):
        if not self.transition(self.num_frames):
            return True
        else:
            return False
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows

    def draw(self, canvas):
        clock.time += 1
        self.next_frame()

        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )

        source_size = (self.frame_width, self.frame_height)

        dest_size = (100, 100)

        canvas.draw_image(self.img,
                          source_centre,
                          source_size,
                          self.pos.get_p(),
                          dest_size)
        
class Clock:
    
    def __init__(self):
    
        self.time = 0
        
    def tick(self):
        self.time += 1
        
    def transition(self, num_frames):
        if self.time < num_frames:
            return True
        else:
            return False
            
class Rocket:
    def __init__(self, pos, radius):
        self.pos = pos
        self.vel = Vector()
        self.radius = radius
        self.IMG = simplegui.load_image(
            'https://docs.google.com/uc?export=download&id=1rZ0LwsjV8rCCkF4FNzZXRcSQzyQi5aMl')
        self.IMG2 = simplegui.load_image(
            'https://docs.google.com/uc?export=download&id=1z5_y8BrMbTlJjw_EV-GK2sKjoQ6yyn2K')
        self.IMG_CENTRE = (72, 128)
        self.IMG_DIMS = (143,256)
        self.rotation = None
        self.angle = Vector(0,-1)
        self.moving = False

    def draw(self, canvas):
        self.rotation = vector_to_angle(self.angle)
        if self.moving:
            canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, (self.pos.x % WIDTH, self.pos.y % HEIGHT),
                              self.radius, self.rotation)
        else:
            canvas.draw_image(self.IMG2, self.IMG_CENTRE, self.IMG_DIMS, (self.pos.x % WIDTH, self.pos.y % HEIGHT),
                              self.radius, self.rotation)            
            
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.8)
        
    

        
class StartingPosition:
    def __init__(self, pos, radius):
        self.pos = pos
        self.vel = Vector()
        self.radius = radius
        self.colour = 'White'
        self.rotation = None
        self.angle = Vector(0,-1)
        self.dx = None
        self.dy = None

    def draw(self, canvas):
        self.rotation = vector_to_angle(self.angle)
        projectile_offset = Vector(0, -60)
        self.dx = projectile_offset.x * math.cos(self.rotation) - projectile_offset.y * math.sin(self.rotation)
        self.dy = projectile_offset.x * math.sin(self.rotation) + projectile_offset.y * math.cos(self.rotation)

        top_offset = Vector(0, -30)
        middle_offset = Vector(0, -15)
        bottom_offset = Vector(0, 15)

        self.topX = top_offset.x * math.cos(self.rotation) - top_offset.y * math.sin(self.rotation)
        self.topY = top_offset.x * math.sin(self.rotation) + top_offset.y * math.cos(self.rotation)
        self.middleX = middle_offset.x * math.cos(self.rotation) - middle_offset.y * math.sin(self.rotation)
        self.middleY = middle_offset.x * math.sin(self.rotation) + middle_offset.y * math.cos(self.rotation)
        self.bottomX = bottom_offset.x * math.cos(self.rotation) - bottom_offset.y * math.sin(self.rotation)
        self.bottomY = bottom_offset.x * math.sin(self.rotation) + bottom_offset.y * math.cos(self.rotation)
        #canvas.draw_circle((self.pos.x % WIDTH + self.topX, self.pos.y % HEIGHT + self.topY), 15, 1, self.colour,self.colour)
        #canvas.draw_circle((self.pos.x % WIDTH + self.middleX, self.pos.y % HEIGHT + self.middleY), 15, 1, self.colour,self.colour)
        #canvas.draw_circle((self.pos.x % WIDTH + self.bottomX, self.pos.y % HEIGHT + self.bottomY), 20, 1, self.colour,self.colour)
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.8)
        
    def collisionTop(self,position):
        temp = Vector(self.pos.x % WIDTH + self.topX,self.pos.y % HEIGHT + self.topY)
        distance = (position - (temp)).length()
        return distance <= 40
    
    def collisionMiddle(self,position):
        temp = Vector(self.pos.x % WIDTH + self.middleX,self.pos.y % HEIGHT + self.middleY)
        distance = (position - (temp)).length()
        return distance <= 40
    
    def collisionBottom(self,position):
        temp = Vector(self.pos.x % WIDTH + self.bottomX,self.pos.y % HEIGHT + self.bottomY)
        distance = (position - (temp)).length()
        return distance <= 40
    

class Projectile:
    def __init__(self,dx,dy,pos,angle):
        self.dx = dx
        self.dy = dy
        self.pos = pos
        self.vel = angle
        self.radius = 5
        self.colour = 'Yellow'
    
    def draw(self,canvas):
        canvas.draw_circle((self.pos.x % WIDTH + self.dx, self.pos.y % HEIGHT + self.dy), 
                           self.radius, 1, self.colour,self.colour)
        self.update()
        
    def update(self):
        self.pos.add(self.vel * 1.5)
        
    def collision(self,position):
        temp = Vector(self.pos.x % WIDTH, self.pos.y % HEIGHT)
        distance = (temp - position).length()
        return distance < 40

    
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
            rocket.moving = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
            rocket.moving = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False

class Asteroid:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.img = simplegui.load_image('https://docs.google.com/uc?export=download&id=1yv-SQL4dKv4Zuj8R6ZtrYvRDbpe46RzT')
        self.img_centre = (250, 250)
        self.img_dims = (500, 500)
        self.dest_dim = (64, 64)
        self.img_rot = 0
        self.step = 0.05
        
    def draw(self, canvas):
        canvas.draw_image(self.img,
                          self.img_centre,
                          self.img_dims,
                          self.pos.get_p(),
                          self.dest_dim,
                          self.img_rot)
    
    def update(self):
        self.img_rot += self.step
        
class Ball:
    def __init__(self, pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        
    def offset_left(self):
        return self.pos.x - self.radius
    
    def offset_right(self):
        return self.pos.x + self.radius
    
    def offset_top(self):
        return self.pos.y - self.radius
    
    def offset_bottom(self):
        return self.pos.y + self.radius   
    
    def update(self):
        self.pos.add(self.vel)
        
    def bounce(self, normal):
        self.vel.reflect(normal)
        
class Wall:
    def __init__(self, x, y, border, color):
        self.x = x
        self.y = y
        self.border = border
        self.color = color
        self.normal_vertical = Vector(1,0)
        self.normal_horizontal = Vector(0, 1)
        self.edge_right = x + self.border
        self.edge_bottom = y + self.border
    
    def hit_left(self, ball):
        h = (ball.offset_left() <= self.edge_right)
        return h

    def hit_right(self, ball):
        h = (ball.offset_right() >= WIDTH - self.edge_right)
        return h
    
    def hit_top(self, ball):
        h = (ball.offset_top() <= self.edge_bottom)
        return h

    def hit_bottom(self, ball):
        h = (ball.offset_bottom() >= HEIGHT - self.edge_bottom)
        return h

class Interaction:
    def __init__(self, wall, balls, rocket, keyboard, startingPos):
        self.wall = wall
        self.balls = balls
        self.rocket = rocket
        self.keyboard = keyboard
        self.startingPos = startingPos
        self.in_collision = set()
        self.wall_collision = False
    
    def hit(self, b1, b2):
        sep_vec = b1.pos.copy().subtract(b2.pos)
        return sep_vec.length() < b1.radius + b2.radius
    
    def do_bounce(self, b1, b2):
        sep_vec = b1.pos.copy().subtract(b2.pos)
       
        unit = sep_vec.copy().normalize()
        v1_par = b1.vel.get_proj(unit)
        v1_perp = b1.vel.copy().subtract(v1_par)
        v2_par = b2.vel.get_proj(unit)
        v2_perp = b2.vel.copy().subtract(v2_par)
        
        b1.vel = v2_par + v1_perp
        b2.vel = v1_par + v2_perp
        
    def collide(self, b1, b2):
        if self.hit(b1, b2):
            b1vb2 = (b1, b2) in self.in_collision
            b2vb1 = (b2, b1) in self.in_collision
            if not b1vb2 and not b2vb1:
                self.do_bounce(b1, b2)
                self.in_collision.add((b1, b2))
        else:
            self.in_collision.discard((b1, b2))
            self.in_collision.discard((b2, b1))
     
    def update(self):
        if self.keyboard.right:
            self.rocket.angle.rotate(4)
            self.startingPos.angle.rotate(4)
        if self.keyboard.left:
            self.rocket.angle.rotate(-4)
            self.startingPos.angle.rotate(-4)
        if self.keyboard.up:
            self.rocket.vel.add(self.rocket.angle)
            self.startingPos.vel.add(self.rocket.angle)
        if self.keyboard.space:
            if len(PROJECTILE) < 1:
                projectile = Projectile(self.startingPos.dx,self.startingPos.dy,
                                        self.rocket.pos.copy(),self.rocket.angle.copy().multiply(6))
                PROJECTILE.append(projectile)
                
        for ball in self.balls:
            ball.update()
            if self.wall.hit_left(ball) or self.wall.hit_right(ball):
                # Fix the sticky problem with the wall
                if not self.wall_collision:
                    ball.bounce(self.wall.normal_vertical)
                    self.wall_collision = True
                else:
                    self.wall_collision = False
            if self.wall.hit_top(ball) or self.wall.hit_bottom(ball):
                if not self.wall_collision:
                    ball.bounce(self.wall.normal_horizontal)
                    self.wall_collision = True
                else:
                    self.wall_collision = False
        
        for ball1 in self.balls:
            for ball2 in self.balls:
                if ball1 != ball2:
                    self.collide(ball1, ball2)

                    
    def draw(self, canvas):
        if lives > 0:
            self.update()
            background.draw(canvas)
            rocket.update()
            startingPos.update()
            rocket.draw(canvas)
            startingPos.draw(canvas)
            canvas.draw_text('SCORE:', [WIDTH - 225, 50], 40, 'White')
            canvas.draw_text(str(score), [WIDTH - 75, 50], 40, 'White')
            canvas.draw_text('LIVES:', [WIDTH - 975, 50], 40, 'White')
            canvas.draw_text(str(lives),[WIDTH - 840, 50], 40, 'White')
            if len(asteroids) < 7:
                number = random.randint(1,4)
                new_asteroid = Asteroid(rand_pos_vec(number),
                                        rand_vel_vec())
                new_ball = Ball(new_asteroid.pos,
                                new_asteroid.vel,
                                24)
                asteroids.append(new_asteroid)
                balls.append(new_ball)
            if len(PROJECTILE) == 1:
                PROJECTILE[0].draw(canvas)
            for asteroid in asteroids:
                asteroid.draw(canvas)
                asteroid.update()
                if(startingPos.collisionTop(asteroid.pos)) or (startingPos.collisionMiddle(asteroid.pos)) or (startingPos.collisionBottom(asteroid.pos)):
                    for ball in balls:
                        if(startingPos.collisionTop(ball.pos)) or (startingPos.collisionMiddle(ball.pos)) or (startingPos.collisionBottom(ball.pos)):
                            DEL_BALL.append(ball)
                            break
                    DEL_ASTEROID.append(asteroid)
                    reduceLives()
                if((asteroid.pos.x % WIDTH < 0 - 10 or asteroid.pos.x % WIDTH > WIDTH + 10) or (asteroid.pos.y % HEIGHT < 0 - 10 or asteroid.pos.y % HEIGHT > HEIGHT + 10)):
                    for ball in balls:
                        if((ball.pos.x % WIDTH < 0 - 10 or ball.pos.x % WIDTH > WIDTH + 10) or (ball.pos.y % HEIGHT < 0 - 10 or ball.pos.y % HEIGHT > HEIGHT + 10)):
                            DEL_BALL.append(ball)
                            break
                    DEL_ASTEROID.append(asteroid)
                
                if len(PROJECTILE) == 1:
                    if((PROJECTILE[0].pos.x % WIDTH < 0 or PROJECTILE[0].pos.x % WIDTH > WIDTH - 10) or (PROJECTILE[0].pos.y % HEIGHT < 0 or PROJECTILE[0].pos.y % HEIGHT > HEIGHT - 10)):
                        DEL_PROJECTILE.append(PROJECTILE[0])
                    if(PROJECTILE[0].collision(asteroid.pos)):
                        for ball in balls:
                            if(PROJECTILE[0].collision(ball.pos)):
                                DEL_BALL.append(ball)
                                break
                        DEL_PROJECTILE.append(PROJECTILE[0])
                        DEL_ASTEROID.append(asteroid)
                        speedup()
                        increaseScore()
                        
            for explosion in explosions:
                if clock.transition(explosion.num_frames):
                    explosion.draw(canvas)
                else:
                    DEL_EXPLOSIONS.append(explosion)
                    clock.time = 0

            for projectile in DEL_PROJECTILE:
                if projectile in PROJECTILE:
                    PROJECTILE.remove(projectile)
            del DEL_PROJECTILE[:]
            for ball in DEL_BALL:
                if ball in balls:
                    balls.remove(ball)
            del DEL_BALL[:]
            for asteroid in DEL_ASTEROID:
                if asteroid in asteroids:
                    explosion = Explosions(SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS,asteroid.pos.copy())
                    explosions.append(explosion)
                    asteroids.remove(asteroid)
            del DEL_ASTEROID[:]
            for explosion in DEL_EXPLOSIONS:
                if explosion in explosions:
                    explosions.remove(explosion)
            del DEL_EXPLOSIONS[:]
            if score >= 25:
                frame.set_draw_handler(end_game)                
                
        else:
            del asteroids[:]
            del balls[:]
            del explosions[:]
            timer.stop()
            frame.set_draw_handler(draw_handler)


def rand_pos_vec(number):
    if number == 1:
        return Vector(random.randint(33, WIDTH // 2 - 100),
                      random.randint(33, HEIGHT // 2 - 100))       
    if number == 2:
        return Vector(random.randint(WIDTH // 2, WIDTH - 33),
                      random.randint(33, HEIGHT // 2 - 50))	
    if number == 3:
        return Vector(random.randint(33, WIDTH // 2),
                      random.randint(HEIGHT // 2 + 50, HEIGHT - 33))
    if number == 4:
        return Vector(random.randint(WIDTH // 2, WIDTH - 33),
                      random.randint(HEIGHT // 2 + 50, HEIGHT - 33))

    
def rand_vel_vec():
    return Vector(random.uniform(-MAX_SPEED, MAX_SPEED),
                  random.uniform(-MAX_SPEED, MAX_SPEED))

def rand_asteroid():
    number = random.randint(1,4)
    return Asteroid(rand_pos_vec(number),
                    rand_vel_vec())

      

kbd = Keyboard()
rocket = Rocket(Vector(WIDTH / 2, HEIGHT / 2),(50,90))
startingPos = StartingPosition(Vector(WIDTH / 2, HEIGHT / 2),5)
asteroids = [ rand_asteroid() for i in range(NUM_ASTEROIDS) ]
background = Background()
wall = Wall(0, 0, 5, 'red')
balls = []
for asteroid in asteroids:
    balls.append(Ball(asteroid.pos,asteroid.vel,24))
clock = Clock()
interaction = Interaction(wall, balls, rocket, kbd, startingPos)

def draw_handler(canvas):
    global lives,score,asteroid_spawn_time
    background.draw(canvas)
    canvas.draw_text("Asteroids", [280, 210], 100, "White", "sans-serif")
    canvas.draw_text("Control your rocket to shoot asteroids.", [160, 300], 30, "White", "sans-serif")
    canvas.draw_text("Use the right, left and up keys to move your rocket.", [160, 370], 30, "White", "sans-serif")
    canvas.draw_text("Press the space key to shoot projectiles.", [160, 440], 30, "White", "sans-serif")
    canvas.draw_text("Get to 25 points to win! Good luck!", [160, 510], 30, "White", "sans-serif")
    canvas.draw_text("Click The Play Button To Play", [330, 600], 23, "White")
    canvas.draw_text("Click The Quit Button To Quit", [330, 650], 23, "White")
    if lives == 0:
        global rocket,startingPos,asteroids,balls
        rocket.pos.y = (HEIGHT / 2)
        rocket.pos.x = (WIDTH / 2)
        startingPos.pos.x = (WIDTH / 2)
        startingPos.pos.y = (HEIGHT / 2)
        asteroids = [ rand_asteroid() for i in range(NUM_ASTEROIDS) ]
        for asteroid in asteroids:
            balls.append(Ball(asteroid.pos,asteroid.vel,24))
        lives = 3
        score = 0
        asteroid_spawn_time = 2000

def end_game(canvas):
    global score
    background.draw(canvas)
    canvas.draw_text("You Win!", [280, 400], 100, "White", "sans-serif")
    canvas.draw_text("Click The Quit Button to Exit the Screen", [270, 600], 23, "White")

def to_play():
    global game
    game = True
    if game:
        timer.start()
        frame.set_draw_handler(interaction.draw)

def to_quit():
    global game
    exit()
    frame.stop()
    timer.stop()
    
def timer_handler():
    global asteroid_spawn_time
    number = random.randint(1,4)
    new_asteroid = Asteroid(rand_pos_vec(number),
                            rand_vel_vec())
    new_ball = Ball(new_asteroid.pos,
                    new_asteroid.vel,
                    24)
    asteroid_spawn_time -= 50
    if(startingPos.collisionTop(new_asteroid.pos)) or (startingPos.collisionMiddle(new_asteroid.pos)) or (startingPos.collisionBottom(new_asteroid.pos)):
        del new_asteroid
        del new_ball
    else:
        asteroids.append(new_asteroid)
        balls.append(new_ball)

                 
timer = simplegui.create_timer(asteroid_spawn_time, timer_handler)
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.add_button("Play", to_play, 60)
frame.add_button("Quit", to_quit, 60)
frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()