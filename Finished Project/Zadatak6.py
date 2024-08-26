import pygame
import time
import math
import sys

pygame.init()

sirina_ekrana, visina_ekrana = 800, 600
screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
pygame.display.set_caption("Rotacija strelice")

icon = pygame.image.load('strelica.png')
pygame.display.set_icon(icon)

arrow_original = pygame.image.load('arrow_64x64.png')
arrow = arrow_original
strelica_rect = arrow.get_rect(center=(400, 300))

x, y = 400, 300
rotation = 0
brzina = 5
moveX, moveY = 0, 0

clock = pygame.time.Clock()
previous_time = time.time()
average_time_per_frame = 0
FPS = 60

running = True
forward = False
backward = False
mouse_control = False

counter = 0
counter_for_counter = 0
broj_pritisaka = 0

rotation = 0

pomakXos = 0
pomakYos = 0

font_main = pygame.font.Font("Silkscreen.ttf", 22)
font_secondary = pygame.font.Font('verdana.ttf', 18)

fullscreen_gumb = pygame.Rect((sirina_ekrana - 220) // 2, visina_ekrana - 50 - 10, 200, 40)
fullscreen_tekst = font_main.render("Fullscreen", True, (255, 255, 255))
fullscreen_tekst_sirina = fullscreen_tekst.get_width()

gumb_kontrola = pygame.Rect(30, 10, 230, 50)
kontrola_misem_text = font_main.render("Kontrola misem", True, pygame.Color('white'))
fullscreen_text = font_main.render("Fullscreen", 1, (255, 255, 255))
upaljeno_text = font_secondary.render("(Upaljeno)", 1, (255, 255, 255))
ugaseno_text = font_secondary.render("(Ugaseno)", 1, (255, 255, 255))
 
text_rect = kontrola_misem_text.get_rect(center=gumb_kontrola.center)

clock = pygame.time.Clock()

moving_forward = False
moving_backward = False
fullscreen = False

kontrola_misem = False
kontrola_tipkama = True
pocetna_pozicija = (0, 0)

while True:
    screen.fill((64,64,64))

    trenutna_rotacija = font_secondary.render("Kut rotacije: " + str(rotation % 360) + "°", 1, (255, 255, 255))
    kutevi = font_secondary.render("(0° - 360°)", 1, (255, 255, 255))
    mis = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gumb_kontrola.collidepoint(pygame.mouse.get_pos()):
                broj_pritisaka += 1
                if broj_pritisaka % 2 != 0: 
                    pygame.time.delay(200)
                    kontrola_misem = True
                    kontrola_tipkama = False
                else:
                    pygame.time.delay(200)
                    kontrola_misem = False
                    kontrola_tipkama = True
                    
            elif fullscreen_gumb.collidepoint(pygame.mouse.get_pos()):
                if fullscreen == False:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
                    fullscreen = False
            
    keys = pygame.key.get_pressed()

    if gumb_kontrola.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (204, 204, 255), gumb_kontrola)
    else:
        pygame.draw.rect(screen, (102, 102, 255), gumb_kontrola)

    if fullscreen_gumb.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (204, 204, 255), fullscreen_gumb)
    else:
        pygame.draw.rect(screen, (102, 102, 255), fullscreen_gumb)
        
    if kontrola_tipkama == True:
        screen.blit(ugaseno_text, (100, 65))
        
        
        if keys[pygame.K_UP]:
                moving_forward = True
        else:
            moving_forward = False

        if keys[pygame.K_DOWN]:
                moving_backward = True
        else:
            moving_backward = False

        if keys[pygame.K_LEFT]:
                rotation += 2
        elif keys[pygame.K_RIGHT]:
                rotation -= 2
            
            
    if kontrola_misem == True:
        screen.blit(upaljeno_text, (100, 65))
        if pygame.mouse.get_pressed()[2]:
            moving_forward = True
        else:
            moving_forward = False

        if pygame.mouse.get_pressed()[0]:
            moving_backward = True
        else:
            moving_backward = False
        
        rotation = int((180 * (math.atan2((mis[1] - y), (x - mis[0]))) / math.pi) + 180)
       
            
    if moving_forward:
        pomakXos = math.sin((((rotation + 90) / 180) * math.pi) % (2 * math.pi)) * brzina
        pomakYos = math.cos((((rotation + 90) / 180) * math.pi) % (2 * math.pi)) * brzina
    elif moving_backward:
        pomakXos = math.sin((((rotation + 90) / 180) * math.pi) % (2 * math.pi)) * (-brzina)
        pomakYos = math.cos((((rotation + 90) / 180) * math.pi) % (2 * math.pi)) * (-brzina)
    else:
        pomakXos = 0
        pomakYos = 0

    strelica_rect.x += pomakXos
    strelica_rect.y += pomakYos

    if strelica_rect.x > 800:
        strelica_rect.x = 800
    if strelica_rect.x < 0:
         strelica_rect.x = 0
    if strelica_rect.y > 600:
         strelica_rect.y = 600
    if strelica_rect.y < 0:
         strelica_rect.y = 0
    
    rotated_arrow = pygame.transform.rotozoom(arrow, rotation, 1)
    rotated_rect = rotated_arrow.get_rect(center=(strelica_rect.x, strelica_rect.y))

    screen.blit(trenutna_rotacija, (620, 10))
    screen.blit(kutevi, (630, 40))
    screen.blit(rotated_arrow, rotated_rect.topleft)
    
    screen.blit(kontrola_misem_text, text_rect.topleft)
    screen.blit(fullscreen_tekst, (fullscreen_gumb.x + (200 - fullscreen_tekst_sirina) // 2, fullscreen_gumb.y + 5))
    pygame.display.flip()
    clock.tick(60)