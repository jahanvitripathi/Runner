import pygame
from sys import exit 
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect (center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return[]
    
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


pygame.init()
screen = pygame.display. set_mode((800,400))
pygame.display.set_caption ("Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font (None, 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("music.mp3")
bg_music.play(loops = -1)


sky_surface = pygame.image.load ("sky.png").convert()
land_surface = pygame.image.load ("ground.png").convert()

snail_surf = pygame.image.load("snail1.png").convert_alpha()
fly_surf = pygame.image.load ("fly.png").convert_alpha()

obstacle_rect_list = [] 

player_surf = pygame.image.load ("player1.png").convert_alpha()
player_rect = player_surf.get_rect(topleft = (80, 173))

player_gravity = 0
player_stand = pygame.image.load ("player1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect (center = (400,200))

game_name = test_font.render ("Runner", False, (64,64,64)).convert()
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render ("Press space to run", False, (64,64,64))
game_message_rect = game_message.get_rect (center = (400, 320))

obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit ()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 307: 
                    player_gravity = -20
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 307:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True 
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))

            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),190)))
 

    if  game_active:
            screen.blit(sky_surface, (0,0))
            screen.blit(land_surface, (0, 300))
            score = display_score()

            player_gravity += 1     
            player_rect.y += player_gravity
            if player_rect.bottom >= 307: player_rect.bottom= 307
            screen.blit(player_surf, player_rect) 

            obtacle_rect_list = obstacle_movement(obstacle_rect_list)

            game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill ((94, 129, 162))
        screen.blit (player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0 
        

        score_message = test_font.render(f"Your score: {score}", False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,320))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit (game_message, game_message_rect)

        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)