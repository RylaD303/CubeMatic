import pygame, sys
from enum import Enum
from pygame.locals import *
from src.game_objects.player import Player
from src.game_objects.boss import Boss
from src.game_objects.bullet import Bullet
from src.game_objects.laser import Laser, LaserState
from src.game_objects.teleport import Teleport
from src.game_objects.tiles import MapTile
from src.game_objects.effects import CircleEffect
from src.classes.vector_2d import Vector2D
from src.game_values import *

#def collision_test(sprite: "pygame.Rect", objects: list["MapTile"]):
#    hit_list =  [object for object in objects if sprite.colliderect(object.sprite.get_rect())]
#    return hit_list

pygame.init()

#Clock
clock = pygame.time.Clock()
clock.tick()


class GameState(Enum):
    Menu = 0
    Loading = 1
    Running = 2
    Won = 3
    Lost = 4
    Paused = 5


font = pygame.font.SysFont("arialblack", 40)
def draw_text(text: str, text_color: tuple, position:"Vector2D", screen: "pygame.Surface") -> None:
    img = font.render(text, True, text_color)
    screen.blit(img, tuple(position))

class Game:
    """
    class to handle the game's responsibilites like:
        user button pushing;
        rendering game objects on the screen;
        creation and deletion of game objects;
        collsion handling;
    """
    resizable_screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
    def __init__(self):
        """
        Initialises the Game object.
        takes resizable screen on which to print on.
        """
        self.player: "Player" = None
        self.player_bullets: set["Bullet"] = None
        self.teleportation_device: "Teleport" = None
        self.boss: "Boss" = None
        self.boss_bullets: set["Bullet"] = None
        self.boss_lasers: set["Laser"] = None
        self.circle_effects: set["CircleEffect"] = None
        self.map_tiles: set["MapTile"] = None
        self.screen = Game.resizable_screen.copy()
        self.screen_scaling = 1
        self.game_state = None
        self.keys_pressed = {}

    def handle_objects_main(self):
        """
        Handles the main functions of all the objects.
        The main functions activate the main behaviours of the
        non-static GameObjects. They should be called each frame
        the game is running so they can evaluate the objects
        positions, cooldowns and other thing.
        """
        #Player movement
        self.player.main(self.keys_pressed["player_movement"], clock)

        #Bullet movement
        for bullet in self.player_bullets:
            bullet.main(clock)

        #Teleportation device movement and cooldowns
        self.teleportation_device.main(self.player, clock)

        #Check if device is active and cooldown is expired
        if self.teleportation_device.time_remaining == 0\
            and self.teleportation_device.active:
            self.teleportation_device.teleport_player(self.player)

        #Bullet movement
        for bullet in self.boss_bullets:
            bullet.main(clock)

        #Laser movement and cooldowns
        for laser in self.boss_lasers:
            laser.main(clock, self.boss.centre_position())

        #Boss movement, cooldowns and attack patterns
        self.boss.main( self.player,\
                        self.boss_bullets,\
                        self.boss_lasers,\
                        clock)

        #Other effects
        for effect in self.circle_effects:
            effect.main(clock)

    def handle_objects_rendering(self):
        """
        Renders all objects on screen.
        """
        #Rendering player on screen
        self.player.render(self.screen)

        #Rendering bullets
        for bullet in self.player_bullets:
            bullet.render(self.screen)

        #Rendering teleportation device
        self.teleportation_device.render(self.screen)

        for bullet in self.boss_bullets:
            bullet.render(self.screen)

        for laser in self.boss_lasers:
            laser.render(self.screen)

        self.boss.render(self.screen)

        #Rendering tile_map
        for map_tile in self.map_tiles:
            map_tile.render(self.screen)

        #Renderiing effects
        for effect in self.circle_effects:
            effect.render(self.screen)

        #Rendering tex if game paused:
        if self.game_state == GameState.Paused:
            draw_text("Press ESC again to unpause",
                            (0, 128, 0),
                            Vector2D(END_OF_MAP.x/2, 100),
                            self.screen)

    def handle_objects_collisions(self):
        """
        Handles all collisions between objects.
        """
        self.player.check_out_of_bounds()

        #Collects the player's bullets which need to be removed.
        players_bullets_to_remove: set[Bullet]= set()
        for bullet in self.player_bullets:
            if bullet.is_colliding_with(self.boss):
                bullet.invalidate()
                #todo!
            bullet.check_boundaries()
            if not bullet.is_valid():
                players_bullets_to_remove.add(bullet)


        #Removes the player's bullets who are not valid.
        for bullet in players_bullets_to_remove:
            self.player_bullets.remove(bullet)


        #Collects the boss' bullets which need to be removed.
        boss_bullets_to_remove: set[Bullet]= set()
        for bullet in self.boss_bullets:
            bullet.check_boundaries()
            if not bullet.is_valid():
                boss_bullets_to_remove.add(bullet)
                self.circle_effects.add(\
                    CircleEffect(bullet.position,BOSS_BULLET_SIZE*2))
            elif bullet.is_colliding_with(self.player):
                print("Lost")

        #Removes the boss' bullets who are not valid.
        for bullet in boss_bullets_to_remove:
            self.boss_bullets.remove(bullet)

        #Handles deflection of the teleportation device
        if self.teleportation_device.active:
            self.teleportation_device.check_boundaries()

        #Handles effects removal
        effects_to_remove: set[Bullet]= set()
        for effect in self.circle_effects:
            if not effect.is_valid():
                effects_to_remove.add(effect)

        for effect in effects_to_remove:
            self.circle_effects.remove(effect)

        #Handles laser removal
        lasers_to_remove: set["Laser"] = set()
        for laser in self.boss_lasers:
            if not laser.is_valid():
                lasers_to_remove.add(laser)
            elif laser.state == LaserState.Attack:
                point = laser.get_end_point_in_map()
                if point:
                    self.circle_effects.add(\
                        CircleEffect(point,LASER_EFFECT_RADIUS))

        for laser in lasers_to_remove:
            self.boss_lasers.remove(laser)


    def load_level(self):
        """
        Loads the objects into the game class.
        """
        #Tile map creation
        map_tile_sprite =\
            pygame.image.load('src\sprites\Tile_map_wall_sprite.png')
        map_tile_corner_sprite =\
            pygame.image.load('src\sprites\Tile_map_corner_sprite.png')

        self.map_tiles = []
        start_pos_x = START_OF_WINDOW.x  #(END_OF_WINDOW.x%MAP_TILE_SIZE[0])/2
        start_pos_y = START_OF_WINDOW.y  #(END_OF_WINDOW.y%MAP_TILE_SIZE[1])/2
        end_pos_x = END_OF_WINDOW.x//MAP_TILE_SIZE[0]*MAP_TILE_SIZE[0]
        end_pos_y = END_OF_WINDOW.y//MAP_TILE_SIZE[1]*MAP_TILE_SIZE[1]
        top_left_map_corner = Vector2D(start_pos_x, start_pos_y)
        top_right_map_corner = Vector2D(end_pos_x + start_pos_x, start_pos_y)
        bottom_left_map_corner =\
            Vector2D(start_pos_x, end_pos_y + start_pos_y)
        bottom_right_map_corner =\
            Vector2D(end_pos_x + start_pos_x, end_pos_y + start_pos_y)

        self.map_tiles.append(MapTile(top_left_map_corner,
                                    map_tile_corner_sprite,
                                    90,
                                    *MAP_TILE_SIZE))
        self.map_tiles.append(MapTile(top_right_map_corner,
                                    map_tile_corner_sprite,
                                    0,
                                    *MAP_TILE_SIZE))
        self.map_tiles.append(MapTile(bottom_left_map_corner,
                                    map_tile_corner_sprite,
                                    180,
                                    *MAP_TILE_SIZE))
        self.map_tiles.append(MapTile(bottom_right_map_corner,
                                    map_tile_corner_sprite,
                                    270,
                                    *MAP_TILE_SIZE))

        for i in range(1, END_OF_WINDOW.x//MAP_TILE_SIZE[0]):
            position_x = start_pos_x + i*MAP_TILE_SIZE[0]
            self.map_tiles.append(MapTile(Vector2D(position_x, 0),
                                        map_tile_sprite,
                                        0,
                                        *MAP_TILE_SIZE))
            self.map_tiles.append(MapTile(Vector2D(position_x, end_pos_y),
                                        map_tile_sprite,
                                        180,
                                        *MAP_TILE_SIZE))

        for i in range(1, END_OF_WINDOW.y//MAP_TILE_SIZE[1]):
            position_y = start_pos_y + i*MAP_TILE_SIZE[1]
            self.map_tiles.append(MapTile(Vector2D(start_pos_x, position_y),
                                        map_tile_sprite,
                                        90,
                                        *MAP_TILE_SIZE))
            self.map_tiles.append(MapTile(Vector2D(end_pos_x, position_y),
                                        map_tile_sprite,
                                        270,
                                        *MAP_TILE_SIZE))

        #Player creation
        self.player = Player(PLAYER_START,
                        PLAYER_SPEED,
                        pygame.image.load('src/sprites/Player1.png'),
                        *tuple(PLAYER_SCALE))
        self.teleportation_device: "Teleport" = Teleport(PLAYER_TELEPORT_SPEED)

        #Boss creation
        self.boss = Boss(pygame.image.load('src/sprites/Player1.png'),\
                    *tuple(BOSS_SCALE))
        self.boss_bullets = set()
        self.boss_lasers = set()


        #Other
        self.player_bullets: set[Bullet] = set()

        self.circle_effects: set["CircleEffect"] = set()

        self.keys_pressed =\
            {
            "player_movement": [False, False, False, False],
            "fire": False,
            "pause": False,
            "teleport": False
            }

    def get_key_presses(self):
        """
        Gets the key presses from the user and evaluates the events.
        """
        for event in pygame.event.get():
            #Existing game
            if event.type == QUIT:
                self.game_state = GameState.Ended
                pygame.quit()
                sys.exit()


            #Changing window size
            elif event.type == VIDEORESIZE:
                Game.resizable_screen =\
                    pygame.display.set_mode((event.size[0],event.size[0]/2),
                                            RESIZABLE)
                self.screen_scaling = event.size[0]/WINDOW_SIZE[0]


            elif event.type == pygame.KEYDOWN:

                #Player start movement
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.keys_pressed["player_movement"][0] = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.keys_pressed["player_movement"][1] = True
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.keys_pressed["player_movement"][2] = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.keys_pressed["player_movement"][3] = True

                #Pausing and unpausing game
                if event.key == pygame.K_ESCAPE:
                    self.keys_pressed["pause"] = not self.keys_pressed["pause"]


            elif event.type == pygame.KEYUP:

                #Player stop movement
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.keys_pressed["player_movement"][0] = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.keys_pressed["player_movement"][1] = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.keys_pressed["player_movement"][2] = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.keys_pressed["player_movement"][3] = False

            #Player firing or useing teleportation device
            elif event.type == pygame.MOUSEBUTTONDOWN :
                #Bullet firing
                if event.button == 1:              #left mouse click
                    self.keys_pressed["fire"] = True
                    print(self.keys_pressed["fire"])

                #Teleporting
                if event.button == 3:              #right mouse click
                    self.keys_pressed["teleport"] = True

            #Player stop firing
            elif event.type == pygame.MOUSEBUTTONUP :
                if event.button == 1:
                    self.keys_pressed["fire"] = False

    def evaluate_key_presses_ingame(self):
        if self.game_state == GameState.Running:
            if self.keys_pressed["teleport"]:
                if not self.teleportation_device.active:
                    self.teleportation_device.activate(
                        self.player.centre_position(),
                        Vector2D(*pygame.mouse.get_pos())\
                        / self.screen_scaling)
                else:
                    self.teleportation_device.teleport_player(self.player)

            #Check if mouse button is held down
            if self.keys_pressed["fire"]:
                self.player.fire(self.player_bullets,
                                Vector2D(*pygame.mouse.get_pos())\
                                         / self.screen_scaling)

        #Pauses game:
        if self.keys_pressed["pause"]:
            if self.game_state == GameState.Running:
                self.game_state = GameState.Paused
            else:
                self.game_state = GameState.Running

        self.keys_pressed["pause"] = False
        self.keys_pressed["teleport"] = False

    def run(self):
        self.game_state = GameState.Menu
        while True:
            self.get_key_presses()
            self._update()
            self.clear_surface()
            clock.tick(120)
        self.load_level()
        self.game_state = GameState.Running
        self.start()


    def render_surface(self):
        Game.resizable_screen.blit(
                pygame.transform.scale(self.screen,
                                       Game.resizable_screen.get_rect().size),
                                       (0,0))
        pygame.display.flip()

    def clear_surface(self):
        #Black background
        self.screen.fill((0,0,0))

    def start(self):
        clock.tick(120)
        while self.game_state in [GameState.Running, GameState.Paused]:
            if self.game_state == GameState.Running:
                self.handle_objects_main()
            self.evaluate_key_presses_ingame()
            self.handle_objects_collisions()
            self.clear_surface()
            self.handle_objects_rendering()
            self.render_surface()
            clock.tick(120)

        while self.game_state == GameState.Lost:
            self.clear_surface()
            draw_text("Lost", (0, 255, 0), CENTRE_OF_MAP, self.screen)
            self.get_key_presses()
            self.render_surface()
            clock.tick(120)

    def in_menu(self):
        draw_text("CubeMatic",
                (0, 255, 0),
                CENTRE_OF_WINDOW - Vector2D(160,280),
                self.screen)
        self.render_surface()

    def _update(self):
        if self.game_state == GameState.Menu:
            self.in_menu()

game = Game()
game.run()
