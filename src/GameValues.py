from src.classes.Vector2D import Vector2D

#Constants for the game
#Player values
PLAYER_START = Vector2D(20,20) #pixles
PLAYER_SPEED = 7 #pixles
PLAYER_SCALE = Vector2D(48, 48) #pixles
PLAYER_BULLET_SPEED = 20 #pixles
PLAYER_TELEPORT_SPEED = 35 #pixles

PLAYER_SHOOT_COOLDOWN = 100 #ms
MAX_HOLD_TIME = 5000 #ms        how long can the player hold the teleportation device.


#Map values
WINDOW_SIZE = (1400,700) #pixles
START_OF_MAP = Vector2D(0,0) #pixles
END_OF_MAP = Vector2D(*WINDOW_SIZE) #pixles # no touch
MAP_TILE_SIZE = (64, 64) #pixles

#Boss values
BOSS_SCALE = Vector2D(48, 48)
BOSS_BULLET_SPPED = PLAYER_BULLET_SPEED
BOSS_LASER_WIDTH = 10 #pixels
BOSS_LASER_ROTATION_SPEED = 1 #degrees per frame
BOSS_ATTACK_COLOR = (255, 0, 0) # RGB
LASER_LENGTH = abs(END_OF_MAP) #pixels
