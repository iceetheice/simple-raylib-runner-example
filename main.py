from pyray import *
import random

init_window(300, 600, "raylib python")
init_audio_device()

scene = "game"

score = 0
add_score_timer = 0

spawn_timer = 0
time = 3 # 3

die_sound = load_sound("sounds/explosion.wav")
score_up_sound = load_sound("sounds/score-up.wav")

class Player:
    speed = 5
    x = 150
    y = 550

player = Player()

class Enemy:
    speed = 7 # 7
    x = 0
    y = -10
enemys = []

def spawn_enemys():
    enemy = Enemy()
    enemy.x = random.randrange(0, 290)
    enemys.append(enemy)

def update_enemys():
    global scene
    for i in enemys:
        i.y += i.speed
        if check_collision_recs(Rectangle(player.x, player.y, 10, 10), Rectangle(i.x, i.y, 10, 10)):
            play_sound(die_sound)
            scene = "menu"
        if i.y > 610:
            enemys.remove(i)

def draw_enemys():
    for i in enemys:
        draw_rectangle(i.x, i.y, 10, 10, WHITE)
    

def update():
    global add_score_timer
    global score
    global spawn_timer
    global scene
    if scene == "game":
        if is_key_down(KEY_RIGHT) and player.x < 290:
            player.x += player.speed
        if is_key_down(KEY_LEFT) and player.x > 0:
            player.x -= player.speed

        update_enemys()

        spawn_timer += get_frame_time()
        if spawn_timer >= random.randrange(0, 5): # 0, 5
            spawn_enemys()
            spawn_timer = 0
    else:
        for i in enemys:
            enemys.remove(i)  
        player.x = 150

    add_score_timer += 1
    if add_score_timer >= time and scene == "game":
        if score % 100 == 0 and score > 10:
            play_sound(score_up_sound)
        score += 1
        add_score_timer = 0

    if is_key_down(KEY_ENTER):
        scene = "game"
        score = 0

def draw():
    global scene
    global score
    clear_background(BLACK)
    if scene == "menu":
        draw_text("score: " + str(score), 100, 200, 20, WHITE)
        draw_text("press enter to play", 50, 400, 20, WHITE)
    else:
        draw_rectangle(player.x, player.y, 10, 10, RED)
        draw_text(str(score), 10, 10, 20, WHITE)
        draw_enemys()


while not window_should_close():
    set_target_fps(60)
    update()
    begin_drawing()
    draw()
    end_drawing()
close_audio_device()
close_window()
