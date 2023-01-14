import pygame, sys
from pygame.locals import *
from src.Player import Player
from src.Bullet import Bullet
from src.Teleport import Teleport
from src.Tiles import MapTile
from src.CollisionHandler import CollisionHandler
from src.classes.Vector2D import Vector2D
from src.GameValues import *

#def collision_test(sprite: "pygame.Rect", objects: list["MapTile"]):
#    hit_list =  [object for object in objects if sprite.colliderect(object.sprite.get_rect())]
#    return hit_list


handle_collisions = CollisionHandler()

def handle_main(player: "Player", player_bullets: list["Bullet"], teleportation_device: "Teleport" ):
    player.main(player_movement)
    for bullet in player_bullets:
        bullet.main()
    if teleportation_device:
        teleportation_device.main(player)
        if teleportation_device.time_remaining == 0 and teleportation_device.active:
            teleportation_device.teleport_player(player)

def handle_rendering(screen: "pygame.Surface", map_tiles: list["MapTile"], player: "Player", player_bullets: list["Bullet"], teleportation_device: "Teleport"):
    #Rendering tile_map
    for map_tile in map_tiles:
        map_tile.main(screen)

    #Rendering player on screen
    player.render(screen)

    #Rendering bullets
    for bullet in player_bullets:
        bullet.render(screen)

    #Rendering teleportation device
    teleportation_device.render(screen)

    #Rendering screen
    resizable_screen.blit(pygame.transform.scale(screen, resizable_screen.get_rect().size), (0,0))
    pygame.display.flip()

pygame.init()


#Clock
clock = pygame.time.Clock()
clock.tick()

#Tile map creation
map_tile_sprite = pygame.image.load('src\sprites\Tile_map_sprite.png')
map_tile_sprite.set_colorkey(map_tile_sprite.get_at((0,0)))
map_tiles = []
start_pos_x = 0 #(END_OF_MAP.x%MAP_TILE_SIZE[0])/2
start_pos_y = 0 #(END_OF_MAP.y%MAP_TILE_SIZE[1])/2

for i in range(1, END_OF_MAP.y//MAP_TILE_SIZE[1]):
    map_tiles.append(MapTile(Vector2D(0, start_pos_y + i*MAP_TILE_SIZE[1]), map_tile_sprite, 90, *MAP_TILE_SIZE))
    map_tiles.append(MapTile(Vector2D(END_OF_MAP.x - MAP_TILE_SIZE[0] + (MAP_TILE_SIZE[0] - END_OF_MAP.x%MAP_TILE_SIZE[0]), start_pos_y + i*MAP_TILE_SIZE[1]), map_tile_sprite, 270, *MAP_TILE_SIZE))

for i in range(1, END_OF_MAP.x//MAP_TILE_SIZE[0]):
    map_tiles.append(MapTile(Vector2D(start_pos_x + i*MAP_TILE_SIZE[0], 0), map_tile_sprite, 0, *MAP_TILE_SIZE))
    map_tiles.append(MapTile(Vector2D(start_pos_x + i*MAP_TILE_SIZE[0], END_OF_MAP.y - MAP_TILE_SIZE[1] + (MAP_TILE_SIZE[1] - END_OF_MAP.y%MAP_TILE_SIZE[1])), map_tile_sprite, 180, *MAP_TILE_SIZE))

#Player creation
player = Player(PLAYER_START, PLAYER_SPEED, pygame.image.load('src/sprites/Player1.png'), *tuple(PLAYER_SCALE))
player_movement = [False,False,False,False]
player_firing = False
teleportation_device: "Teleport" = Teleport(PLAYER_TELEPORT_SPEED)


#Other
player_bullets: set[Bullet] = set()
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
                if not teleportation_device.active:
                    teleportation_device.activate(player.position + PLAYER_SCALE/2, Vector2D(*pygame.mouse.get_pos())/screen_scaling)
                else:
                    teleportation_device.teleport_player(player)

        #Player stop firing
        elif event.type == pygame.MOUSEBUTTONUP :
            if event.button == 1:
                player_firing = False

    #Creating bullets if player is firing
    if player_firing:
        player_bullets.add(Bullet(player.position + PLAYER_SCALE/2, Vector2D(*pygame.mouse.get_pos())/screen_scaling, PLAYER_BULLET_SPEED))

     #Rendering on the display
    handle_rendering(screen, map_tiles, player, player_bullets, teleportation_device)


    #Handle moving and frame by frame stuff
    handle_main(player, player_bullets, teleportation_device)

    #Collision handling
    handle_collisions(player, player_bullets, teleportation_device)

    #Setting FPS
    clock.tick(60)
