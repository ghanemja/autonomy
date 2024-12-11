import pygame
import cv2
from djitellopy import tello

drone = tello.Tello()
drone.connect()
drone.streamon()
pygame.init()
screen = pygame.display.set_mode((360, 240))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    img = drone.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pygame_surface = pygame.surfarray.make_surface(img.swapaxes(0,1))
    screen.blit(pygame_surface, (0, 0))
    pygame.display.flip()
