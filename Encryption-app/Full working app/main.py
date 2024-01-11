from time import sleep
import screens
import pygame
import client

HOST = "127.0.0.1"
PORT = 9090

user = client.Client(HOST,PORT)

pygame.init()
screen_height = 600
screen_width = 1200

screen = pygame.display.set_mode((screen_width,screen_height))

window = screens.SCREENS(screen,user)
window.Login_page()