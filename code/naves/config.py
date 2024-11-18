import pygame
from threading import Thread
import platform
import cv2
import random
import mediapipe as mp
import math

game_speed = 1
ANCHO_VENTANA=300
ALTO_VENTANA=300
ADD_ENEMY = pygame.USEREVENT+1