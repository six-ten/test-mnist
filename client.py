#-------------------------------------------------Client Code------------------------------------------------
import socket

host = socket.gethostname()
port = 6789

client_socket = socket.socket()

print('attempting connection')
client_socket.connect((host,port))

print('connection successfull')





#--------------------------------------------------GUI code---------------------------------------------------
import pygame
import pygame.camera
import pygame.surfarray as surfarray
from pygame.locals import *
import cv2
import numpy as np
import time
import imutils

e = np.e
window_dims = (336,336)

display_width, display_height = window_dims
pygame.init()
pygame.display.init()
pygame.font.init()

pygame.display.set_mode(window_dims)


gameDisplay = pygame.display.get_surface()

clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

fill_color = black
draw_color = white

def transform(image):
    '''for _ in range(1):
        image = cv2.medianBlur(image,5)
        image = cv2.medianBlur(image,5)
        image = cv2.GaussianBlur(image,(5,5),0)'''
    return cv2.resize(image,(28,28))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


gameDisplay.fill(fill_color)

def pix_ar_to_np(surface):
    image = surfarray.array3d(surface)
    #cv2.imshow('blurred',cv2.resize(cv2.resize(image,(28,28)),(336,336)))
    return image

def make_prediction(image) :
    
    res = image.T
    
    resized = cv2.resize(res[0],(56,56))
    resized = imutils.skeletonize(resized,size=(3,3))
    resized = transform(resized)
    client_socket.send(resized.tobytes())
    prediction = int(client_socket.recv(1024).decode())
    print(prediction)
counter = 0
mu = 1e4
k = 0.01
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1 :
            counter += 1
            pygame.draw.circle(gameDisplay,draw_color,mouse,11,0)
        
        elif click[1] == 1 :
            gameDisplay.fill(fill_color)

        elif click[2] == 1 :
            make_prediction(pix_ar_to_np(gameDisplay))
            time.sleep(1)
        else :
            counter = 0 
        
        
        #largeText = pygame.font.Font('freesansbold.ttf',20)
        #TextSurf, TextRect = text_objects("A bit Racey", largeText)
        #TextRect.center = ((display_width/2),(display_height/2))
        #gameDisplay.blit(TextSurf, TextRect)

        #pygame.draw.rect(gameDisplay, green,(150,450,100,50))
        #pygame.draw.rect(gameDisplay, red,(550,450,100,50))


        pygame.display.update()
        clock.tick(120)
