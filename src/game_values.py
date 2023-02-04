"""
Module for the game's constant values.
"""

from math import pi
from src.classes.vector_2d import Vector2D


#Map values
WINDOW_SIZE = (1400,700) #pixles
START_OF_WINDOW = Vector2D(0,0) #pixles # do no touch
END_OF_WINDOW = Vector2D(*WINDOW_SIZE) #pixles # do no touch

MAP_TILE_SIZE = (64, 64) #pixles
START_OF_MAP = Vector2D(*MAP_TILE_SIZE)
END_OF_MAP = Vector2D(END_OF_WINDOW.x - END_OF_WINDOW.x%MAP_TILE_SIZE[0],\
                      END_OF_WINDOW.y - END_OF_WINDOW.y%MAP_TILE_SIZE[1])
RIGHT_UPPER_CORNER = Vector2D(END_OF_MAP.x, START_OF_MAP.y)
LEFT_LOWER_CORNER = Vector2D(START_OF_MAP.x, END_OF_MAP.y)

CENTRE_OF_WINDOW = END_OF_WINDOW/2
CENTRE_OF_MAP = END_OF_MAP/2
    # - WINDOW_SIZE[0]%MAP_TILE_SIZE[0],\
    # - WINDOW_SIZE[1]%MAP_TILE_SIZE[1]) #pixles
#END_OF_MAP.x -= MAP_TILE_SIZE[0]
#END_OF_MAP.y -= MAP_TILE_SIZE[1]


#Constants for the game
#Player values
PLAYER_START = CENTRE_OF_MAP #pixles
PLAYER_SPEED = 400 #pixles per second
PLAYER_SCALE = Vector2D(48, 48) #pixles
PLAYER_BULLET_SPEED = 900 #pixles per second
PLAYER_BULLET_SLOWDOWN_SPEED = 900 #pixles per second
PLAYER_BULLET_SIZE = 4 # pixels
PLAYER_BULLET_COLOR = (0,255,0) #RGB
PLAYER_TELEPORT_SPEED = 2100 #pixles per second
PLAYER_TELEPORT_SIZE_RADIUS = 6
PLAYER_SHOOT_COOLDOWN = 150 #ms
PLAYER_DAMAGE = 1
MAX_HOLD_TIME = 5000 #ms - how long can the player hold the teleportation device.

#Effects
LIFETIME_OF_CIRCLE_EFFECT = 700 #ms

LASER_EFFECT_RADIUS = 10

#Boss values
BOSS_SCALE = Vector2D(48, 48)
BOSS_LASER_WIDTH = 10 #pixels
BOSS_BULLET_SIZE = 7 #pixels
BOSS_ATTACK_COLOR = (255, 0, 0) # RGB
BOSS_HEALTH = 180
BOSS_HARDMODE_HEALTH_THRESHOLD = BOSS_HEALTH/2
LASER_LENGTH = abs(END_OF_WINDOW) #pixels
LASER_ANTICIPATION_TIME = 1000
HEALTH_BAR_POSITION = Vector2D(300, 20)

#Boss attack vars
BOSS_WAVE_SHOOT_COOLDOWN = 1700 #ms
BOSS_WAVE_SHOOT_ANGLE = pi/9 #degrees in pi
BOSS_WAVE_SHOOT_BULLET_STARTING_SPEED = 50 #pixels per second
BOSS_WAVE_SHOOT_BULLET_INCREASING_SPEED = 250 # pixels per second

BOSS_PLUS_LASER_ROTATION_SPEED = pi/4 #pi degrees per second
BOSS_PLUS_LASER_MAXIMUM_SPEED = pi/2 #pi degrees per second
BOSS_PLUS_LASER_MINIMUM_SPEED = pi/9 #pi degrees per second

BOSS_EDGE_LASER_ROTATION_SPEED = pi/2 #pi degrees per second
BOSS_EDGE_LASER_MAXIMUM_SPEED = pi #pi degrees per second
BOSS_EDGE_LASER_MINIMUM_SPEED = pi/9 #pi degrees per second

BOSS_SPIRAL_COOLDOWN = 70 #ms
BOSS_SPIRAL_SHOOT_ROTATION = pi/13.5 #degrees in pi
BOSS_SPIRAL_SHOOT_BULLET_SPEED = 300 #pixels per second

BOSS_CIRCLE_SHOOT_COOLDOWN = 1000 #ms
BOSS_CIRCLE_SHOOT_ROTATION = pi/13 #degrees in pi
BOSS_CIRCLE_SHOOT_BULLET_SPEED = 300

##Boss movement values
#Boss parabolic/elipse movement
BOSS_UPPER_CENTRE_OF_ELIPSE = Vector2D(END_OF_MAP.x/2, -END_OF_MAP.y/20)
BOSS_LOWER_CENTRE_OF_ELIPSE = Vector2D(END_OF_MAP.x/2, END_OF_MAP.y - END_OF_MAP.y/20)
BOSS_ELIPSE_HEIGHT = END_OF_MAP.y*7/16   #should scale with ends of the map
BOSS_ELIPSE_WIDTH = END_OF_MAP.x/2   #should scale with end of the map



#Menu values
BUTTON_PLAY_SIZE = Vector2D(128, 64)
BUTTON_PLAY_POSITION = END_OF_WINDOW/2 - BUTTON_PLAY_SIZE/2
RESET_PLAY_POSITION = BUTTON_PLAY_POSITION + Vector2D(0, 100)

TITLE_POSITION = END_OF_WINDOW/2 + Vector2D(0, -200)

START_ANIMATION_TIME = 2000 #ms



#Cheats
CAN_LOSE =  True