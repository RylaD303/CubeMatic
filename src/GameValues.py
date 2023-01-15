from src.classes.Vector2D import Vector2D

#Constants for the game
PLAYER_START = Vector2D(20,20) #pixles
PLAYER_SPEED = 7 #pixles
PLAYER_SCALE = Vector2D(48, 48) #pixles
PLAYER_BULLET_SPEED = 20 #pixles
PLAYER_TELEPORT_SPEED = 35 #pixles

PLAYER_SHOOT_COOLDOWN = 100 #ms

WINDOW_SIZE = (1400,700) #pixles
START_OF_MAP = Vector2D(0,0) #pixles
END_OF_MAP = Vector2D(*WINDOW_SIZE) #pixles
MAP_TILE_SIZE = (64, 64) #pixles

MAX_HOLD_TIME = 5000 #ms
