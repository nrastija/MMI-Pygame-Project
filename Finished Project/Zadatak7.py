import pygame
import sys
import time
import random

pygame.init()

# Postavke ekrana
sirina_ekrana, visina_ekrana = 800, 600
screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
pygame.display.set_caption("Igra s Kuglicom")

icon = pygame.image.load('breakout.png')
pygame.display.set_icon(icon)

font_main = pygame.font.Font("verdana.ttf", 22)
font_gumb = pygame.font.Font('Silkscreen.ttf', 22)
font_game_over = pygame.font.Font("RubikDoodleShadow.ttf", 80)
font_broj_bodova = pygame.font.Font("RubikDoodleShadow.ttf", 30)

fullscreen_gumb = pygame.Rect((308, 25, 180, 40))
fullscreen_tekst = font_gumb.render("Fullscreen", True, (255, 255, 255))
fullscreen_tekst_sirina = fullscreen_tekst.get_width()
fullscreen_tekst_visina = fullscreen_tekst.get_height()

game_over_text = font_game_over.render("GAME OVER", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(150, 200))

restart_gumb = pygame.Rect((270, 300, 250, 40))
restart_tekst = font_gumb.render("Ponovno pokreni", True, (255, 255, 255))
restart_tekst_rect = restart_tekst.get_rect(center= restart_gumb.center)

exit_gumb = pygame.Rect((270, 350, 250, 40))
exit_tekst = font_gumb.render("Izađi", True, (255, 255, 255))
exit_tekst_rect = exit_tekst.get_rect(center= exit_gumb.center)

teza_igra_gumb = pygame.Rect((500, 500, 250, 40))
teza_igra_tekst = font_gumb.render("Teza igra?", True, (255, 255, 255))
teza_igra_tekst_rect = teza_igra_tekst.get_rect(center= teza_igra_gumb.center)


# Postavke kuglice
kuglica_radius = 10
kuglica_x = random.randint(kuglica_radius, sirina_ekrana - kuglica_radius)
kuglica_y = kuglica_radius
kuglica_brzina = 5
kuglica_smjer_x = random.choice([-1, 1])
kuglica_smjer_y = 1

# Postavke pločice
plocica_sirina = 120
plocica_visina = 15
plocica_x = (sirina_ekrana - plocica_sirina) // 2
plocica_y = visina_ekrana - 2 * plocica_visina
plocica_brzina = 300

plocica_pomak_Xos = 0
bodovi = 0
broj_zivota = 3

micanje_lijevo = False
micanje_desno = False
fullscreen = False
kraj_igre = False
teza_igra = False

clock = pygame.time.Clock()
prethodno_vrijeme = time.time()
prosjecno_vrijeme = 0
FPS = 60

# Glavna petlja igre
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
             
        elif event.type == pygame.KEYDOWN and not kraj_igre:
            if event.key == pygame.K_LEFT:
                micanje_lijevo = True
            if event.key == pygame.K_RIGHT:
                micanje_desno = True         
                   
        elif event.type == pygame.KEYUP and not kraj_igre:
            if event.key == pygame.K_LEFT:
                if plocica_pomak_Xos == plocica_brzina:
                    micanje_desno = True
                else:
                    micanje_lijevo = False
            if event.key == pygame.K_RIGHT:
                if plocica_pomak_Xos == -plocica_brzina:
                    micanje_lijevo = True
                else:
                    micanje_desno = False
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:           
            if fullscreen_gumb.collidepoint(pygame.mouse.get_pos()):
                if fullscreen == False:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
                    fullscreen = False
            elif teza_igra_gumb.collidepoint(pygame.mouse.get_pos()):
                teza_igra = not teza_igra
    
    screen.fill((0,0,0))
    
    bodovi_text = font_main.render(f"BODOVI: {bodovi}", True, (102,178,255))
    zivoti_text = font_main.render(f"BROJ ZIVOTA: {broj_zivota}", True, (102,178,255))
    osvojeni_bodovi_tekst = font_broj_bodova.render(f"Osvojen broj bodova: {bodovi}", True, (255, 255, 255))
    teza_igra_glavni_tekst = font_main.render(f"TEZA IGRA: {teza_igra}", True, (102,178,255))
    
    trenutno = time.time()
    prosjecno_vrijeme = trenutno - prethodno_vrijeme
    prethodno_vrijeme = trenutno
    
    if (teza_igra == True):
        kuglica_brzina = 10
    else:
        kuglica_brzina = 5
    
    if (kraj_igre == False):
        kuglica_x += kuglica_smjer_x * kuglica_brzina 
        kuglica_y += kuglica_smjer_y * kuglica_brzina 

        if (micanje_desno and not micanje_lijevo):
            plocica_pomak_Xos = plocica_brzina
        elif (micanje_lijevo and not micanje_desno):
            plocica_pomak_Xos = -plocica_brzina
        elif (not micanje_lijevo and not micanje_desno):
            plocica_pomak_Xos = 0
            
        plocica_x += plocica_pomak_Xos * prosjecno_vrijeme
            
            # Odbijanje od zidova
        if kuglica_x - kuglica_radius <= 0 or kuglica_x + kuglica_radius >= sirina_ekrana:
            kuglica_smjer_x *= -1

            # Odbijanje od pločice
        if (
            plocica_x <= kuglica_x <= plocica_x + plocica_sirina and
            plocica_y <= kuglica_y + kuglica_radius <= plocica_y + plocica_visina
        ):
            kuglica_smjer_y *= -1
            bodovi += 1

            
        # Provjera gubitka igre
        if kuglica_y - kuglica_radius >= visina_ekrana:
            broj_zivota -= 1
            
            if (broj_zivota > 0):
                kuglica_x = random.randint(kuglica_radius, sirina_ekrana - kuglica_radius)
                kuglica_y = kuglica_radius
                kuglica_smjer_x = random.choice([-1, 1])
                kuglica_smjer_y = 1 
            else:
                pygame.time.delay(200)
                kraj_igre = True  
        
        if plocica_x > 700:
            plocica_x = 700
        if plocica_x < 0:
            plocica_x = 0
                
        if kuglica_y - kuglica_radius < 0:
            kuglica_smjer_y *= -1
        

    if (kraj_igre == True):
        screen.blit(game_over_text, game_over_rect.center)
        
        if restart_gumb.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 0, 102), restart_gumb)
        else:
            pygame.draw.rect(screen, (51, 51, 255), restart_gumb)
            
        screen.blit(restart_tekst, restart_tekst_rect.topleft)
        
        if exit_gumb.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (64, 64, 64), exit_gumb)
        else:
            pygame.draw.rect(screen, (255, 51, 51), exit_gumb)
        
        screen.blit(exit_tekst, exit_tekst_rect.topleft)
        
        if teza_igra_gumb.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (64, 64, 64), teza_igra_gumb)
        else:
            pygame.draw.rect(screen, (255, 51, 51), teza_igra_gumb)
            
        screen.blit(teza_igra_tekst, teza_igra_tekst_rect .topleft)
        screen.blit(osvojeni_bodovi_tekst, (220, 420))
        
        # Provjera klika na gumbima
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Provjeri klik na gumb "Ponovno pokreni"
            if restart_gumb.collidepoint(pygame.mouse.get_pos()):
                # Postavi sve varijable na početne vrijednosti
                kraj_igre = False
                broj_zivota = 3
                bodovi = 0
                pygame.time.delay(200)
                # Dodatne postavke za ponovno postavljanje elemenata igre
           
            # Provjeri klik na gumb "Izađi"
            elif exit_gumb.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()
    
    
    if fullscreen_gumb.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, (0, 153, 153), fullscreen_gumb)
    else:
        pygame.draw.rect(screen, (64, 64, 64), fullscreen_gumb)
        
    pygame.draw.circle(screen, (160,160,160), (kuglica_x, int(kuglica_y)), kuglica_radius)
    pygame.draw.rect(screen, (160,160,160), (plocica_x, plocica_y, plocica_sirina, plocica_visina))
        
    screen.blit(bodovi_text, (10, 30))
    screen.blit(zivoti_text, (600, 30))
    screen.blit(teza_igra_glavni_tekst, (10, 60))
    
    tekst_rect = fullscreen_tekst.get_rect(center=fullscreen_gumb.center)
    screen.blit(fullscreen_tekst, tekst_rect.topleft)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)