import pgzrun
from pygame import Rect

WIDTH = 900
HEIGHT = 720
TITLE = "JOGUITO"

game_state = "menu"

player = Actor('idle-1')

player.animations = {
    'idle': ['idle-1', 'idle-2', 'idle-3', 'idle-4', 'idle-5', 'idle-6'],
    'idleflip': ['idleflip-1', 'idleflip-2', 'idleflip-3', 'idleflip-4', 'idleflip-5', 'idleflip-6'],
    'run': ['run-1', 'run-2', 'run-3', 'run-4', 'run-5', 'run-6', 'run-7', 'run-8'],
    'runflip': ['runflip-1', 'runflip-2', 'runflip-3', 'runflip-4', 'runflip-5', 'runflip-6', 'runflip-7', 'runflip-8'],
    'jump': ['jump1', 'jump2', 'jump3', 'jump4', 'jump5', 'jump6', 'jump7', 'jump8', 'jump9', 'jump10', 'jump11', 'jump12'],
    'jumpflip': ['jumpflip-1', 'jumpflip-2', 'jumpflip-3', 'jumpflip-4', 'jumpflip-5', 'jumpflip-6', 'jumpflip-7', 'jumpflip-8', 'jumpflip-9', 'jumpflip-10', 'jumpflip-11', 'jumpflip-12']
}

player.animation_index = 0
player.animation_timer = 0
player.animation_speed = 10
player.state = 'idle'

background = Actor('map')
background.x = WIDTH // 2
background.y = HEIGHT // 2

explosoes = []

finish_line = Rect(55, 230, 18, 18)
start_button = Rect((175, 260), (490, 180))
menu_button = Rect((350, 470), (200, 50))
retry_button = Rect((350, 400), (200, 50))
sound_button = Rect((400, 380), (200, 60))
exit_button = Rect((175, 500), (490, 180))

bullets = []
tiro_delay = 0 

colisores = [
    Rect((0, 648), (900, 50)),
    Rect((270, 575), (54, 18)),
    Rect((380, 540), (108, 18)),
    Rect((522, 504), (54, 18)),
    Rect((648, 468), (90, 18)),
    Rect((774, 440), (90, 18)),
    Rect((630, 360), (126, 18)),
    Rect((558, 360), (54, 18)),
    Rect((432, 324), (90, 18)),
    Rect((324, 290), (54, 18)),
    Rect((144, 270), (144, 18)),
    Rect((36, 268), (54, 18)),
]
spikes = [
    Rect((576, 630), (70, 20))
]

RED = 200, 0, 0


def animate_player():
    player.animation_timer += 1
    if player.animation_timer >= player.animation_speed:
        player.animation_timer = 0
        frames = player.animations[player.state]
        player.animation_index = (player.animation_index + 1) % len(frames)
        player.image = frames[player.animation_index]

class Enemies:
    def __init__(self, x, y, min_x, max_x):
        self.frames = ['enemy1', 'enemy2']  
        self.index = 0
        self.timer = 0
        self.frame_duration = 15

        self.actor = Actor(self.frames[0])
        self.actor.x = x
        self.actor.y = y

        self.speed = 1.5  
        self.direction = 1  
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.index = (self.index + 1) % len(self.frames)
            self.actor.image = self.frames[self.index]
            self.timer = 0

        self.actor.x += self.speed * self.direction
        if self.actor.x < self.min_x or self.actor.x > self.max_x:
            self.direction *= -1

    def draw(self):
        self.actor.draw()

enemies = [
    Enemies(480, 314, 435, 520),  
    Enemies(850, 428, 775, 860),
    Enemies(200, 258, 150, 280),
]

class Explosion:
    def __init__(self, x, y):
        self.frames = [f"explosion_{i}" for i in range(1, 16)]  
        self.index = 0
        self.timer = 0
        self.frame_duration = 2
        self.x = x
        self.y = y

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.index += 1
            self.timer = 0

    def draw(self):
        if self.index < len(self.frames):
            screen.blit(self.frames[self.index], (self.x, self.y))

    def is_finished(self):
        return self.index >= len(self.frames)  

def on_mouse_down(pos):
    global game_state
    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
            sounds.menu.stop()
            sounds.level1.play(-1)
            player.x = 100
            player.y = 632
            player.vy = 0
            player.on_ground = False
            player.facing_left = False
            player.jumping = False
            player.animation_index = 0
            player.animation_timer = 0
            player.state = 'idle'
            enemies[:] = [
            Enemies(480, 314, 435, 520),  
            Enemies(850, 428, 775, 860),
            Enemies(200, 258, 150, 280),
        ]
            bullets.clear()
        if exit_button.collidepoint(pos):
            exit()
    elif game_state == "dead":
        if retry_button.collidepoint(pos):
            game_state = "playing"
            player.x = 100
            player.y = 632
            player.vy = 0
            player.on_ground = False
            player.facing_left = False
            player.jumping = False
            player.animation_index = 0
            player.animation_timer = 0
            player.state = 'idle'
            enemies[:] = [
            Enemies(480, 314, 435, 520),  
            Enemies(850, 428, 775, 860),
            Enemies(200, 258, 150, 280),
        ]
            bullets.clear()
        elif menu_button.collidepoint(pos):
            game_state = "menu"
            sounds.level1.stop()
            sounds.menu.play(-1)

def on_key_down(key):
    global tiro_delay
    if key == keys.SPACE and tiro_delay <= 0:
        bullet = Actor('tiro')
        bullet.x = player.x 
        bullet.y = player.y 
        bullet.angle = 0 if not player.facing_left else 180
        bullet.speed = 10
        bullets.append(bullet)
        tiro_delay = 5
    if keyboard.space:
        sounds.sfx_wpn_punch3.play()
  
def update():
    global tiro_delay, game_state

    if game_state == "menu" or game_state == "dead":
        return   
    
    elif game_state == "playing":
        player_speed = 3
        move_x = 0
        player.vy += 0.5  
    if player.vy > 10:
        player.vy = 10

    if player.colliderect(finish_line):
        game_state = "win"
        return

    if keyboard.d:
        move_x = 1
        player.facing_left = False
    elif keyboard.a:
        move_x = -1
        player.facing_left = True
    else:
        move_x = 0

    if keyboard.w and player.on_ground:
        player.vy = -10
        player.on_ground = False
        player.jumping = True

    player.x += move_x * player_speed
    player.y += player.vy

    player_rect = Rect(player.x - player.width // 2, player.y - player.height // 2, player.width, player.height)

    player.on_ground = False
    for colisor in colisores:
        if player_rect.colliderect(colisor) and player.vy >= 0:
            if player_rect.bottom - player.vy <= colisor.top + 5:
                player.y = colisor.top - player.height // 2
                player.vy = 0
                player.on_ground = True

    if not player.on_ground:
        if player.facing_left:
            player.state = "jumpflip"
        else:
            player.state = "jump"
    elif move_x != 0:
        if player.facing_left:
            player.state = "runflip"
        else:
            player.state = "run"
    else:
        if player.facing_left:
            player.state = "idleflip"
        else:
            player.state = "idle"

    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += bullet.speed  # direita
        else:
            bullet.x -= bullet.speed 

        if bullet.y < 0:
            bullets.remove(bullet)

    if tiro_delay > 0:
        tiro_delay -= 1

    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy.actor):
                bullets.remove(bullet)
                explosao = Explosion(enemy.actor.x, enemy.actor.y)
                explosoes.append(explosao)
                enemies.remove(enemy)
                break

    for explosao in explosoes:
        explosao.update()
        if explosao.is_finished():
            explosoes.remove(explosao)

    for spike in spikes:
        if player.colliderect(spike):
            game_state = "dead"

    for enemy in enemies:
        enemy.update()  

    for enemy in enemies:
        if player.colliderect(enemy.actor):
            game_state = "dead"


def draw():
    screen.clear()
    if game_state == "menu":
        if not sounds.menu.get_num_channels():
            sounds.menu.play(-1)
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "dead":
        screen.fill((30, 0, 0)) 
        screen.draw.text("VOCE MORREU", center=(WIDTH//2, HEIGHT//3), fontsize=80, color="red")
        screen.draw.filled_rect(retry_button, "black")
        screen.draw.text("Tentar de novo", center=retry_button.center, fontsize=40, color="white")
        screen.draw.filled_rect(menu_button, "black")
        screen.draw.text("Menu", center=menu_button.center, fontsize=40, color="white")
    elif game_state == "win":
        screen.draw.text("VOCÊ CONSEGUIU!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="gold", owidth=2, ocolor="black")

def draw_menu():
    screen.blit('menu', (0, 0))

def draw_game():
    screen.clear()
    screen.fill((135, 206, 235))
    background.draw()
    animate_player()
    for enemy in enemies:
        enemy.draw()
    for explosao in explosoes:
        explosao.draw()
    player.draw()
    for bullet in bullets:
        bullet.draw()        

pgzrun.go()
