from math import pi
from src.classes.vector_2d import Vector2D

#Constants for the game
#Player values
PLAYER_START = Vector2D(20,20) #pixles
PLAYER_SPEED = 6 #pixles
PLAYER_SCALE = Vector2D(48, 48) #pixles
PLAYER_BULLET_SPEED = 20 #pixles
PLAYER_BULLET_SIZE = 3 # pixels
PLAYER_BULLET_COLOR = (0,255,0) #RGB
PLAYER_TELEPORT_SPEED = 35 #pixles
PLAYER_SHOOT_COOLDOWN = 100 #ms
MAX_HOLD_TIME = 5000 #ms        how long can the player hold the teleportation device.


#Map values
WINDOW_SIZE = (1400,700) #pixles
START_OF_WINDOW = Vector2D(0,0) #pixles # do no touch
END_OF_WINDOW = Vector2D(*WINDOW_SIZE) #pixles # do no touch

MAP_TILE_SIZE = (64, 64) #pixles
START_OF_MAP = Vector2D(*MAP_TILE_SIZE)
END_OF_MAP = Vector2D(END_OF_WINDOW.x - END_OF_WINDOW.x%MAP_TILE_SIZE[0],\
                      END_OF_WINDOW.y - END_OF_WINDOW.y%MAP_TILE_SIZE[1])

CENTRE_OF_MAP = Vector2D(\
    END_OF_MAP.x/2,\
    END_OF_MAP.y/2)
    # - WINDOW_SIZE[0]%MAP_TILE_SIZE[0],\
    # - WINDOW_SIZE[1]%MAP_TILE_SIZE[1]) #pixles
#END_OF_MAP.x -= MAP_TILE_SIZE[0]
#END_OF_MAP.y -= MAP_TILE_SIZE[1]

#Boss values
BOSS_SCALE = Vector2D(48, 48)
BOSS_BULLET_SPPED = PLAYER_BULLET_SPEED
BOSS_LASER_WIDTH = 10 #pixels
BOSS_BULLET_SIZE = 7 #pixels
BOSS_ATTACK_COLOR = (255, 0, 0) # RGB

LASER_LENGTH = abs(END_OF_MAP) #pixels
LASER_ANTICIPATION_TIME = 1000



#Boss attack vars
BOSS_WAVE_SHOOT_COOLDOWN = 1700 #ms
BOSS_WAVE_SHOOT_ANGLE = pi/9 #degrees in pi

BOSS_PLUS_LASER_ROTATION_SPEED = 1 #degrees per frame

BOSS_SPIRAL_SHOOT_ATTACK_ROTATION = pi/12 #degrees in pi
BOSS_SPIRAL_ATTACK_COOLDOWN = 70 #ms



##Boss movement values
#Boss parabolic/elipse movement
BOSS_UPPER_CENTRE_OF_ELIPSE = Vector2D(END_OF_MAP.x/2, -END_OF_MAP.y/20)
BOSS_LOWER_CENTRE_OF_ELIPSE = Vector2D(END_OF_MAP.x/2, END_OF_MAP.y - END_OF_MAP.y/20)
BOSS_ELIPSE_HEIGHT = END_OF_MAP.y*7/16   #should scale with ends of the map
BOSS_ELIPSE_WIDTH = END_OF_MAP.x/2   #should scale with end of the map