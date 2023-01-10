import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.Teleport import Teleport
from src.Tiles import MapTile
from src.classes.Vector2D import Vector2D

pygame.init()


#Clock
clock = pygame.time.Clock()
clock.tick()


#Constants for the game
PLAYER_START = Vector2D(20,20)
PLAYER_SPEED = 7
PLAYER_SCALE = Vector2D(48, 48)

PLAYER_BULLET_SPEED = 20
WINDOW_SIZE = (1400,700)
MAP_TILE_SIZE = (64, 64)


START_OF_MAP = Vector2D(0,0)
END_OF_MAP = Vector2D(*WINDOW_SIZE)
#Tile map creation
map_tile_sprite = pygame.image.load('src\sprites\Tile_map_sprite.png')
map_tiles = []
start_pos_x = (END_OF_MAP.x%MAP_TILE_SIZE[0])/2
start_pos_y = (END_OF_MAP.y%MAP_TILE_SIZE[1])/2

for i in range(END_OF_MAP.x//MAP_TILE_SIZE[0]):
    map_tiles.append(MapTile(Vector2D(start_pos_x + i*MAP_TILE_SIZE[0], 0), map_tile_sprite, 0, *MAP_TILE_SIZE))
    map_tiles.append(MapTile(Vector2D(start_pos_x + i*MAP_TILE_SIZE[0], END_OF_MAP.y - MAP_TILE_SIZE[1]), map_tile_sprite, 180, *MAP_TILE_SIZE))

for i in range(END_OF_MAP.y//MAP_TILE_SIZE[1]):
    map_tiles.append(MapTile(Vector2D(0, start_pos_y + i*MAP_TILE_SIZE[1]), map_tile_sprite, 90, *MAP_TILE_SIZE))
    map_tiles.append(MapTile(Vector2D(END_OF_MAP.x - MAP_TILE_SIZE[0], start_pos_y + i*MAP_TILE_SIZE[1]), map_tile_sprite, 270, *MAP_TILE_SIZE))

#Player creation
player = Player(PLAYER_START, PLAYER_SPEED, pygame.image.load('src/sprites/Player1.png'), *tuple(PLAYER_SCALE))
player_movement = [False,False,False,False]
player_firing = False
teleportation_device: "Teleport" = None


#Other
bullets_fired: set[Bullet] = set()
resizable_screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
screen = resizable_screen.copy()
screen_scaling = 1

game_running = True

while game_running:

    #Black background
    screen.fill((0,0,0))


    #Event handling
    for event in pygame.event.get():

        #Existing game
        if event.type == QUIT:
            game_running = False
            pygame.quit()
            sys.exit()

        #Changing window size
        elif event.type == VIDEORESIZE:
            resizable_screen = pygame.display.set_mode((event.size[0],event.size[0]/2), RESIZABLE)
            screen_scaling = event.size[0]/WINDOW_SIZE[0]


        #Player start movement
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = True


        #Player stop movement
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_movement[0] = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_movement[1] = False
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_movement[2] = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player_movement[3] = False

        #Player firing or useing teleportation device
        elif event.type == pygame.MOUSEBUTTONDOWN :
            #Bullet firing
            if event.button == 1:              #left mouse click
                player_firing = True

            #Teleporting
            if event.button == 3:              #right mouse click
                if not teleportation_device:
                    teleportation_device = Teleport(player.position + PLAYER_SCALE/2, Vector2D(*pygame.mouse.get_pos())/screen_scaling, PLAYER_BULLET_SPEED)
                else:
                    teleportation_device.teleport_player(player)
                    teleportation_device = None

        #Player stop firing
        elif event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1:
                player_firing = False

    #Creating bullets if player is firing
    if player_firing:
        bullets_fired.add(Bullet(player.position + PLAYER_SCALE/2, Vector2D(*pygame.mouse.get_pos())/screen_scaling, PLAYER_BULLET_SPEED))

    #Rendering player on screen
    player.main(screen, player_movement)

    #Rendering bullets and ooking at which ones to remove from set if any
    bullets_to_remove: set[Bullet]= set()
    for bullet in bullets_fired:
        bullet.main(screen)
        if  bullet.position.x <= START_OF_MAP.x or\
            bullet.position.x >= END_OF_MAP.x or\
            bullet.position.y <= START_OF_MAP.y or\
            bullet.position.y >= END_OF_MAP.y:
            bullets_to_remove.add(bullet)

    #Removing here, cuz we cannot change object while being iterated if any
    for bullet in bullets_to_remove:
        bullets_fired.remove(bullet)

    #Rendering teleportation device if any
    if teleportation_device:
        teleportation_device.main(screen, player)
        if teleportation_device.time_remaining == 0:
            teleportation_device.teleport_player(player)
            teleportation_device = None

    #Rendering screen
    resizable_screen.blit(pygame.transform.scale(screen, resizable_screen.get_rect().size), (0,0))
    pygame.display.flip()

    #Setting FPS
    clock.tick(60)
