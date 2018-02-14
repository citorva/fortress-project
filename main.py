import pygame
import gradient

pygame.init()

size = (pygame.display.Info().current_w//2,pygame.display.Info().current_h//2)

window = pygame.display.set_mode(size,pygame.HWSURFACE | pygame.DOUBLEBUF)
run = True
gradient = gradient.GradientAnimation(window, (0,0), size,pygame.Color(126,163,208), pygame.Color(173,248,253),
                            pygame.Color(127,0,0), pygame.Color(255,0,0), 5, Direction.TTB, 32, 60)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]: run = False
    gradient.update_color()


pygame.quit()
