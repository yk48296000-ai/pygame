import pygame
import random
import sys
import cv2
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solarpunk eco runner")
clock = pygame.time.Clock()
bg = pygame.image.load("assets/background.png")
player_img = pygame.image.load("assets/runner.png")
waste_img = pygame.image.load("assets/waste.png")
energy_img = pygame.image.load("assets/energy.png")
tree_img = pygame.image.load("assets/tree.png")
logo_img = pygame.image.load("assets/logo.png")
start_img = pygame.image.load("assets/start_btn.png")
exit_img = pygame.image.load("assets/exit_btn.png")
restart_img = pygame.image.load("assets/restart_btn.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (60, 60))
waste_img = pygame.transform.scale(waste_img, (40, 40))
energy_img = pygame.transform.scale(energy_img, (30, 30))
tree_img = pygame.transform.scale(tree_img, (60, 80))
logo_img = pygame.transform.scale(logo_img, (400, 150))
start_img = pygame.transform.scale(start_img, (160, 70))
exit_img = pygame.transform.scale(exit_img, (160, 70))
restart_img = pygame.transform.scale(restart_img, (160, 70))
pygame.mixer.music.load("assets/audio/bg.mp3")
collect_sound = pygame.mixer.Sound("assets/audio/collect.wav")
waste_sound = pygame.mixer.Sound("assets/audio/waste.wav")
click_sound = pygame.mixer.Sound("assets/audio/click.wav")
gameover_sound = pygame.mixer.Sound("assets/audio/gameover.wav")
pygame.mixer.music.set_volume(0.5)
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 50)
player_x = 150
player_y = HEIGHT - 120
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True
score = 0
pollution = 100
time_limit = 60
wastes = []
energies = []
trees = []
shayari = "If you do this in real world, you are a genius 🌱"
def play_intro_video():
    cap = cv2.VideoCapture("assets/video/intro.mp4")
    if not cap.isOpened():
        print("Video not found")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    delay = int(1000 / fps)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
        pygame.time.delay(delay)
    cap.release()
def start_screen():
    pygame.mixer.music.play(-1)
    while True:
        screen.blit(bg, (0, 0))
        screen.blit(logo_img, (250, 120))
        start_rect = start_img.get_rect(center=(450, 320))
        exit_rect = exit_img.get_rect(center=(450, 420))
        screen.blit(start_img, start_rect)
        screen.blit(exit_img, exit_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    click_sound.play()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
def game_loop():
    global player_y, velocity_y, on_ground, score, pollution
    score = 0
    pollution = 100
    wastes.clear()
    energies.clear()
    trees.clear()
    start_time = pygame.time.get_ticks()
    while True:
        clock.tick(60)
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        remaining = time_limit - elapsed
        if remaining <= 0:
            gameover_sound.play()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = jump_power
            on_ground = False
        velocity_y += gravity
        player_y += velocity_y
        if player_y >= HEIGHT - 120:
            player_y = HEIGHT - 120
            on_ground = True
        if random.randint(1, 40) == 1:
            wastes.append([WIDTH, HEIGHT - 100])

        if random.randint(1, 50) == 1:
            energies.append([WIDTH, HEIGHT - 150])
        for w in wastes:
            w[0] -= 6
        for e in energies:
            e[0] -= 6
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        for w in wastes[:]:
            if player_rect.colliderect(pygame.Rect(w[0], w[1], 40, 40)):
                wastes.remove(w)
                pollution += 5
                waste_sound.play()
        for e in energies[:]:
            if player_rect.colliderect(pygame.Rect(e[0], e[1], 30, 30)):
                energies.remove(e)
                score += 10
                pollution -= 5
                trees.append([random.randint(200, WIDTH), HEIGHT - 120])
                collect_sound.play()
        pollution = max(0, min(100, pollution))
        screen.blit(bg, (0, 0))
        for t in trees:
            screen.blit(tree_img, t)
        screen.blit(player_img, (player_x, player_y))
        for w in wastes:
            screen.blit(waste_img, w)
        for e in energies:
            screen.blit(energy_img, e, special_flags=pygame.BLEND_ADD)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 10))
        screen.blit(font.render(f"Pollution: {pollution}%", True, (255,0,0)), (10, 40))
        screen.blit(font.render(f"Time: {remaining}", True, (255,255,255)), (10, 70))
        txt = font.render(shayari, True, (0, 0, 0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 10))

        pygame.display.update()
def game_over():
    while True:
        screen.blit(bg, (0, 0))

        txt = big_font.render("TIME UP!", True, (255, 0, 0))
        screen.blit(txt, (300, 200))

        restart_rect = restart_img.get_rect(center=(450, 320))
        exit_rect = exit_img.get_rect(center=(450, 420))

        screen.blit(restart_img, restart_rect)
        screen.blit(exit_img, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    click_sound.play()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
while True:
    play_intro_video()
    start_screen()
    game_loop()
    game_over()