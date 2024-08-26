import pygame
import sys
import time

# Inicijalizacija Pygame-a
pygame.init()

# Postavljanje veličine prozora
sirina_ekrana, visina_ekrana = 800, 600
screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))

# Postavljanje naslova prozora
pygame.display.set_caption("Avion animacija")
logo = pygame.image.load('logo_avion.png')
pygame.display.set_icon(logo)

# Postavljanje pravokutnika za brzi  i spori avion
avion_slika = pygame.image.load("avion_desno.png")  # Zamijenite "avion.png" s vašom slikom aviona
avion_brzi = avion_slika.get_rect()


# Postavljanje x i y osi aviona
avion_brzi.x = 0
avion_brzi.y = 300

# Postavljanje brzine aviona
brzina_aviona = 100  # piksela po sekundi

# Postavljanje pozadinske slike
background_image = pygame.image.load("pozadina.jpg")  # Zamijenite "pozadina.jpg" s vašom slikom pozadine

#Postavljanje fonta za tekst
glavni_font = pygame.font.Font("verdana.ttf", 16)
font_gumb = pygame.font.Font("Silkscreen.ttf", 20)


# Postavljanje fullscreen gumba
fullscreen_gumb_sirina = 220
fullscreen_gumb_visina = 40

fullscreen_gumb = pygame.Rect((sirina_ekrana - fullscreen_gumb_sirina) // 2, visina_ekrana - fullscreen_gumb_visina - 20, fullscreen_gumb_sirina, fullscreen_gumb_visina)
fullscreen_tekst = font_gumb.render("Fullscreen", True, (255, 255, 255))
fullscreen_tekst_sirina = fullscreen_tekst.get_width()

# Glavna petlja igre
FPS = 60

clock = pygame.time.Clock()
proslo_vrijeme = time.time()
vremenski_prosjek = 0
vrijeme_FPS = 0

trenutni_smjer = True
pomakX_os = 0
pomakY_os = 0

brojac = 0

fullscreen = False

brzina_promjena = 10

vrijeme_strelica_gore = 0
vrijeme_strelica_dolje = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fullscreen_gumb.collidepoint(event.pos):
                if fullscreen == False:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    screen = pygame.display.set_mode((sirina_ekrana, visina_ekrana))
                    fullscreen = False

    FPS = frames = glavni_font.render("FPS ekrana: " + str(round(clock.get_fps(), 2)), 1, (255, 255, 255))
    Brzina = glavni_font.render("Trenutna brzina: " + str(brzina_aviona) + " piksela po sekundi", 1, (255, 255, 255))
    Moguca_brzina = glavni_font.render("( 100 - 2000 )", 1, (255, 255, 255))
    
    trenutno_vrijeme = time.time()
    vrijeme_FPS = trenutno_vrijeme - proslo_vrijeme
    vremenski_prosjek = trenutno_vrijeme

    # Povecanje brzine strelicama
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        if brzina_aviona < 2000 and (time.time() - vrijeme_strelica_gore) > 0.1:  
            brzina_aviona += brzina_promjena
            vrijeme_strelica_gore = time.time()
    elif keys[pygame.K_DOWN]:
        if brzina_aviona > 100 and (time.time() - vrijeme_strelica_dolje) > 0.1: 
            brzina_aviona -= brzina_promjena
            vrijeme_strelica_dolje = time.time()
    
    # Provjera hover efekta
    if fullscreen_gumb.collidepoint(pygame.mouse.get_pos()):
        fullscreen_hover = True
    else:
        fullscreen_hover = False
    
     # Crtanje pozadine
    screen.blit(background_image, (0, 0))
    
    # Računanje vremena proteklog od zadnjeg frejma
    proteklo_vrijeme = clock.tick(60) / 1000.0  # Vraća vremenski razmak između frejmova u sekundama
    
    if avion_brzi.x >= 735 and trenutni_smjer == True:
        trenutni_smjer = False
        avion_slika = pygame.image.load('avion_lijevo.png')

    if avion_brzi.x <= 1 and trenutni_smjer == False:
        trenutni_smjer = True
        avion_slika = pygame.image.load('avion_desno.png')

    if trenutni_smjer == True:
        pomakX_os = brzina_aviona
    
    if trenutni_smjer == False:
        pomakX_os = -brzina_aviona

    screen.blit(FPS, (620, 10))    
    screen.blit(Brzina, (10, 10))
    screen.blit(Moguca_brzina, (95, 30))
    
    avion_brzi.x += pomakX_os * proteklo_vrijeme
    avion_brzi.y += pomakY_os * proteklo_vrijeme
    
    if(avion_brzi.x >= 735):
        avion_brzi.x = 735
    if(avion_brzi.x < 1):
        avion_brzi.x = 1
    
    # Crtanje fullscreen gumba s hover efektom
    if fullscreen_hover:
        pygame.draw.rect(screen, (204, 204, 255), fullscreen_gumb)  # Zatamni boju gumba
    else:
        pygame.draw.rect(screen, (102, 102, 255), fullscreen_gumb)  # Originalna boja gumba
        

    
    # Crtanje aviona
    screen.blit(avion_slika, (avion_brzi.x, avion_brzi.y))
    
    # Crtanje gumba
    screen.blit(fullscreen_tekst, (fullscreen_gumb.x + (fullscreen_gumb_sirina - fullscreen_tekst_sirina) // 2, fullscreen_gumb.y + 5))  
      
    # Ažuriranje ekrana
    pygame.display.flip()

# Zatvaranje Pygame-a
pygame.quit()