import pygame, sys, time, json, os.path, time
from random import choice
from enum import Enum
from pygame.locals import *
from src.game_objects.player import Player
from src.game_objects.boss import Boss
from src.game_objects.bullet import Bullet
from src.game_objects.laser import Laser, LaserState
from src.game_objects.teleport import Teleport
from src.game_objects.tiles import MapTile
from src.game_objects.effects import CircleEffect
from src.game_objects.button import Button
from src.game_objects.health_bar import HealthBar
from src.classes.vector_2d import Vector2D
from src.game_values import *

pygame.mixer.init()
lose_sound = pygame.mixer.Sound("src/sounds/lose_sound.wav")
lose_sound.set_volume(0.4)

GREEN = (0, 255, 0)
def draw_text(text: str, text_color: tuple, position: "Vector2D", screen: "pygame.Surface") -> None:
    img = font.render(text, True, text_color)
    offset = Vector2D(img.get_width(),img.get_height())/2
    screen.blit(img, tuple(position - offset))

play_button_image = pygame.image.load('src/sprites/Play_button.png')
play_button = Button(play_button_image, BUTTON_PLAY_POSITION, BUTTON_PLAY_SIZE)
reset_button_image = pygame.image.load('src/sprites/Reset_button.png')
reset_button = Button(reset_button_image, RESET_PLAY_POSITION, BUTTON_PLAY_SIZE)
starting_offset = Vector2D(0,700)

def time_to_str(time_in_seconds):
    """
    turns seconds into a string 'MM:SS'
    """
    time_in_seconds = round(time_in_seconds)
    seconds = time_in_seconds%60
    minutes = str(time_in_seconds//60)
    seconds = "0" + str(seconds) if seconds<10 else str(seconds)
    return minutes + ":" + seconds

user_values = {}
def reset_user_values():
    """
    Resets the user values to default
    """
    user_values["lost_playthroughs"] = 0
    user_values["won_playthroughs"] = 0
    user_values["best_time"] = None
    user_values["won_last_game"] = False
    user_values["lost_last_game"] = False
    user_values["won_last_game_good_time"] = False
    user_values["lost_game_less_than_30_seconds"] = False

def rewrite_player_values(user_values: dict):
    """
    Saves the user values to the file.
    """
    with open("player_values.json", 'w', encoding = "UTF-16") as outfile:
        outfile.write(json.dumps(user_values, indent = 4))


if os.path.exists("player_values.json"):
    # GeTs the user values at the start of the program
    # or creates the file if it doesnt't exist.
    with open('player_values.json', 'r', encoding = "UTF-16") as openfile:
        user_values = json.load(openfile)

else:
    user_values = {}
    reset_user_values()
    rewrite_player_values(user_values)

text_quotes = None
with open('src/text_lines.json', 'r', encoding = "UTF-16") as openfile:
    text_quotes = json.load(openfile)

def choose_quote():
    if text_quotes == None:
        return ""

    if user_values["lost_playthroughs"] == 0\
        and user_values["won_playthroughs"] == 0:
        return choice(text_quotes["first_game"])

    if user_values["won_playthroughs"] == 1\
        and user_values["won_last_game"]:
        return choice(text_quotes["won_first_game"])

    if user_values["won_last_game"]\
        and user_values["won_last_game_good_time"]:
        return choice(text_quotes["won_last_game_good_time"])

    if user_values["won_last_game"]:
        return choice(text_quotes["won_last_game"])

    if user_values["lost_game_less_than_30_seconds"]:
        return choice(text_quotes["lost_game_less_than_30_seconds"])

    return choice(text_quotes["lost_last_game"])



class GameState(Enum):
    Menu = 0
    Loading = 1
    Running = 2
    Won = 3
    Lost = 4
    Paused = 5
    Animation = 6
    AfterBoss = 7
    ShowText = 8
class Game:
    """
    class to handle the game's responsibilites like:
        user button pushing;
        rendering game objects on the screen;
        creation and deletion of game objects;
        collsion handling;
    """
    resizable_screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)
    time_left_for_animation = START_ANIMATION_TIME
    time_for_text_main = 0
    time_for_text_after_start = 0
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
        self.screen_scaling: float= 1
        self.game_state: "GameState" = None
        self.keys_pressed: dict = {}
        self.boss_health_bar: "HealthBar" = None
        self.start_time: float = None
        self.quote = None

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

        #Teleport creation

        self.teleportation_device: "Teleport" =\
            Teleport(PLAYER_TELEPORT_SPEED,
                     pygame.image.load('src/sprites/Teleport.png'),
                     PLAYER_SCALE)

        #Boss creation
        self.boss = Boss(pygame.image.load('src/sprites/Boss.png'),\
                    *tuple(BOSS_SCALE))
        self.boss_bullets = set()
        self.boss_lasers = set()
        self.boss_health_bar = HealthBar(HEALTH_BAR_POSITION)

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

        #Bullet movement
        for bullet in self.boss_bullets:
            bullet.main(clock)

        #Laser movement and cooldowns
        for laser in self.boss_lasers:
            if self.boss.active:
                laser.main(clock, self.boss.centre_position())
            else:
                laser.main(clock)

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

        self.boss_health_bar.render(self.screen)

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
                self.boss.take_damage(PLAYER_DAMAGE)
                self.boss_health_bar.set_health(self.boss.health)
                if self.boss.health <= 0:
                    self.game_state = GameState.Won
            bullet.check_boundaries()
            if not bullet.is_valid():
                players_bullets_to_remove.add(bullet)
                self.circle_effects.add(\
                    CircleEffect(bullet.position, bullet.radius*2))


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
                    CircleEffect(bullet.position, bullet.radius*2))
            elif bullet.is_colliding_with(self.player):
                    self.game_state = GameState.Lost

        #Removes the boss' bullets who are not valid.
        for bullet in boss_bullets_to_remove:
            self.boss_bullets.remove(bullet)

        #Handles laser collision
        lasers_to_remove: set["Laser"] = set()
        for laser in self.boss_lasers:
            if not laser.is_valid():
                lasers_to_remove.add(laser)
            elif laser.state == LaserState.Attack:
                point = laser.get_end_point_in_map()
                if point:
                    self.circle_effects.add(\
                        CircleEffect(point, LASER_EFFECT_RADIUS))
                if laser.is_colliding_with(self.player):
                    self.game_state = GameState.Lost


        #Handles laser removal
        for laser in lasers_to_remove:
            self.boss_lasers.remove(laser)

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

    def get_key_presses(self):
        """
        Gets the key presses from the user and evaluates the events.
        """
        for event in pygame.event.get():
            #Existing game
            if event.type == QUIT:
                if self.game_state in [GameState.Running,
                                       GameState.Paused,
                                       GameState.ShowText]:
                    self.game_state = GameState.Lost
                    self.time_survived = round(time.time() - self.start_time)
                    self.update_user_values()
                rewrite_player_values(user_values)
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

                #Teleporting
                if event.button == 3:              #right mouse click
                    self.keys_pressed["teleport"] = True

            #Player stop firing
            elif event.type == pygame.MOUSEBUTTONUP :
                if event.button == 1:
                    self.keys_pressed["fire"] = False

    def evaluate_key_presses_ingame(self):
        """
        Evaluates events based on pressed keys from user.
        """
        if self.game_state != GameState.Paused:
            if self.keys_pressed["teleport"]:
                if not self.teleportation_device.active:
                    self.teleportation_device.activate(
                        self.player.position,
                        (Vector2D(*pygame.mouse.get_pos())\
                        - Vector2D(self.player.sprite.get_width()/2,
                                    self.player.sprite.get_height()/2))\
                        / self.screen_scaling)
                else:
                    self.teleportation_device.teleport_player(
                        self.player,
                        self.circle_effects)

            #Check if mouse button is held down
            if self.keys_pressed["fire"]:
                self.player.fire(self.player_bullets,
                                Vector2D(*pygame.mouse.get_pos())\
                                            / self.screen_scaling)

        #Pauses game:
        if self.keys_pressed["pause"]:
            if self.game_state == GameState.Running:
                self.game_state = GameState.Paused
            elif self.game_state == GameState.AfterBoss:
                self.game_state = GameState.Menu
            else:
                self.game_state = GameState.Running

        self.keys_pressed["pause"] = False
        self.keys_pressed["teleport"] = False

    def run(self):
        """
        Starts the game.
        """
        self.game_state = GameState.Menu
        while True:
            self._update()
            clock.tick(120)

    def render_surface(self, offset: "Vector2D" = Vector2D(0,0)):
        """
        Renders everything on the screen of the user, scaling with
        the user's resized window.
        """
        Game.resizable_screen.blit(
                pygame.transform.scale(self.screen,
                                       Game.resizable_screen.get_rect().size),
                                       tuple(offset))
        pygame.display.flip()

    def clear_surface(self):
        """
        Clears the game's surface (screen)
        """
        #Black background
        self.screen.fill((0,0,0))

    def run_level_enter_animation(self):
        """
        Runs the animation for the start of the game.
        """
        if Game.time_left_for_animation>0:
            Game.time_left_for_animation -= clock.get_time()
            offset = Game.time_left_for_animation\
                     / START_ANIMATION_TIME*starting_offset
            self.handle_objects_rendering()
            self.render_surface(offset)
            self.clear_surface()
        else:
            self.game_state = GameState.ShowText
            Game.time_for_text_after_start = 3000
            self.quote = choose_quote()

    def run_level(self):
        """
        Runs everything connected with the level.
        Movement, collision, rendering on the user's screen.
        """
        if self.game_state != GameState.Paused:
            self.handle_objects_main()
        self.evaluate_key_presses_ingame()
        self.handle_objects_collisions()
        self.handle_objects_rendering()

    def run_menu(self):
        """
        Runs the menu of the game.
        Prints the buttons and checks for clicks on them.
        Also shows best Time to beat the game and total wins.
        """
        draw_text("CubeMatic",
                GREEN,
                TITLE_POSITION,
                self.screen)
        clicked_play = play_button.main(self.screen, self.screen_scaling)
        clicked_reset = reset_button.main(self.screen, self.screen_scaling)

        if Game.time_for_text_main > 0:
            Game.time_for_text_main -= clock.get_time()
            draw_text("Reset game values",
                    GREEN,
                    BUTTON_PLAY_POSITION + Vector2D(70, 200),
                    self.screen)
        if user_values["best_time"]:
            draw_text("Best time:  " + time_to_str(user_values["best_time"]),
                    GREEN,
                    BUTTON_PLAY_POSITION + Vector2D(70, 250),
                    self.screen)

        draw_text("Total wins:  " + str(user_values["won_playthroughs"]),
                    GREEN,
                    BUTTON_PLAY_POSITION + Vector2D(70, 300),
                    self.screen)
        if clicked_play == True:
            self.clear_surface()
            self.render_surface()
            self.game_state = GameState.Loading
            Game.time_for_text_after_start = 3000

        if clicked_reset:
            reset_user_values()
            Game.time_for_text_main = 2000

    def reset_user_last_game(self):
        """
        Clears the last game's values.
        """
        user_values["won_last_game"] = False
        user_values["lost_last_game"] = False
        user_values["won_last_game_good_time"] = False
        user_values["lost_game_less_than_30_seconds"] = False

    def update_user_values(self):
        """
        Updates the user's values according to the games end.
        """
        self.reset_user_last_game()
        if self.game_state == GameState.Lost:
            user_values["lost_playthroughs"] += 1

            if self.time_survived < 30:
                user_values["lost_game_less_than_30_seconds"] = True
            else:
                user_values["lost_last_game"] = True

        if self.game_state == GameState.Won\
            or self.game_state == GameState.AfterBoss:
            user_values["won_playthroughs"] += 1

            if not user_values["best_time"]\
               or user_values["best_time"] > self.time_survived:
                user_values["best_time"] = self.time_survived
            if self.time_survived < 60:
                user_values["won_last_game_good_time"] == True
            else:
                user_values["won_last_game"] = True

    def _update(self):
        """
        Checks the game's state and acts accordingly.
        """
        self.get_key_presses()
        if self.game_state == GameState.Menu:
            self.run_menu()

        elif self.game_state == GameState.Loading:
            draw_text("Loading...", GREEN, CENTRE_OF_WINDOW, self.screen)
            self.clear_surface()
            self.render_surface()
            self.load_level()
            Game.time_left_for_animation = START_ANIMATION_TIME
            self.game_state = GameState.Animation
            self.start_time = time.time()
            clock.tick(120)

        elif self.game_state == GameState.Animation:
            self.run_level_enter_animation()
            return

        elif self.game_state == GameState.ShowText:
            if Game.time_for_text_after_start > 0:
                draw_text(self.quote,
                            GREEN,
                            CENTRE_OF_MAP + Vector2D(0, 200),
                            self.screen)
                self.run_level()
                Game.time_for_text_after_start -= clock.get_time()
            else:
                self.game_state = GameState.Running
                self.boss.activate()

        elif self.game_state in [GameState.Running, GameState.Paused]:
            self.run_level()

        elif self.game_state == GameState.Lost:
            if not CAN_LOSE:
                self.game_state = GameState.Running
                self._update()
                return
            self.time_survived = round(time.time() - self.start_time)
            self.update_user_values()
            self.handle_objects_rendering()
            pygame.mixer.Sound.play(lose_sound)
            draw_text("Game Over", GREEN, CENTRE_OF_MAP, self.screen)
            time_survived = round(time.time() - self.start_time)
            draw_text("Time survived: " + time_to_str(time_survived),
                      GREEN,
                      CENTRE_OF_MAP + Vector2D(0, 100),
                      self.screen)
            self.render_surface()
            time.sleep(4)
            self.clear_surface()
            self.game_state = GameState.Menu

        elif self.game_state == GameState.Won:
            self.time_survived = round(time.time() - self.start_time)
            self.update_user_values()
            self.boss.deactivate()
            self.circle_effects.add(CircleEffect(self.boss.centre_position(),\
                                                self.boss.radius*3))
            self.boss_bullets = set()
            for laser in self.boss_lasers:
                laser.switch_state(LaserState.Recovery)
            self.boss.position = Vector2D(-100,-100)
            self.game_state = GameState.AfterBoss

        elif self.game_state == GameState.AfterBoss:
            draw_text("press Esc to get back to menu",
                        GREEN,
                        Vector2D(END_OF_MAP.x/2, 100),
                        self.screen)
            draw_text("Won!", GREEN, CENTRE_OF_MAP, self.screen)
            draw_text("Total time: " + time_to_str(self.time_survived),
                        GREEN,
                        CENTRE_OF_MAP + Vector2D(0, 100),
                        self.screen)

            if user_values["best_time"] == self.time_survived:
                draw_text("New best Time!",
                        GREEN,
                        CENTRE_OF_MAP + Vector2D(0, 150),
                        self.screen)

            self.run_level()

        self.render_surface()
        self.clear_surface()

pygame.init()
font = pygame.font.SysFont("arialblack", 40)
#Clock
clock = pygame.time.Clock()
clock.tick()

pygame_icon = pygame.image.load('src/sprites/Player1.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption('CubeMatic')


game = Game()
game.run()
