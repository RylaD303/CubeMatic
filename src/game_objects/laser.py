from typing import Union
from enum import Enum
import pygame
from math import isclose
from src.game_values import *
from src.classes.vector_2d import Vector2D, number_types
from src.classes.game_object import GameObject

WHITE = (255, 255 ,255)
class LaserState(Enum):
    """Enum for laser state"""
    Anticipation = 1
    Attack = 2
    Recovery = 3

class LaserMovement(Enum):
    """Enum to describe the laser movements"""
    Constant = 1
    AcceleratingStart = 2
    DeceleratingEnd = 3



def get_segment_intersection(beginpoint1: "Vector2D",
                        endpoint1: "Vector2D",
                        beginpoint2: "Vector2D",
                        endpoint2: "Vector2D") -> Union["Vector2D", None]:
    """
    Checks if the two line segments intersect and
    returns their intersection.
    Returns none if the line segments do not interset.

    todo! documentation
    """
    vector1 = endpoint1 - beginpoint1
    vector2 = endpoint2 - beginpoint2
    cross_product1 = vector1.cross_product(vector2)
    cross_product2 = vector2.cross_product(beginpoint1 - beginpoint2)
    if isclose(cross_product1, 0) or isclose(cross_product2, 0):
        return None

    scalar = cross_product2/cross_product1

    return (beginpoint1 + scalar*vector1, scalar)



def distance_to_line_segment(point: "Vector2D",
                            begin_point: "Vector2D",
                            end_point: "Vector2D"):
    """
    Returns the distance between a point and segment
    defined by two points.

    formula from here:
    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    Under: "Line defined by two points"
    """
    line_vector = end_point - begin_point
    point_to_begin = begin_point - point
    top = abs(line_vector.x*point_to_begin.y - point_to_begin.x*line_vector.y)
    bottom = abs(line_vector)

    return top/bottom


class Laser(GameObject):
    """
    Laser object for the boss attacks.

    Handles own movement and chagne of states.
    """

    def __init__(self,
        begin_point: "Vector2D",
        direction: "Vector2D",
        time: number_types, #ms
        width: number_types = 10,
        color: tuple = (255, 0, 0))-> None:
        """
        Initialises the Laser object.

        Parameters:
            begin_point -
                Starting point of the laser.
            direction -
                Direction of the laser.
            time -
                time for the laser to live.
            width -
                width of the laser.
            color -
                color with which the laser will be rendered.
        """
        super().__init__(begin_point)
        self.direction = (direction/abs(direction))*LASER_LENGTH
        self.width = width
        self.starting_width = width
        self.color = color
        self.state = LaserState.Anticipation
        self.movement_types = [LaserMovement.Constant]
        self.rotation_speed = 0
        self.cooldown = LASER_ANTICIPATION_TIME
        self.time_to_execute = time


    def main(self,
            clock: "pygame.time.Clock",
            new_position: "Vector2D" = None):
        """
        Handles main part of the laser - movement, state evaluation,
        time left to execute.

        Parameters:
            clock -
                to evaluate time left to live.
            new_position -
                the new position at frame of which the laser should be
                comnig from. If not given one, the laser stays in one
                place.
        """
        self.cooldown -= clock.get_time()
        self.time_to_execute -= clock.get_time()
        self.direction.angle_rotate(self.rotation_speed*clock.get_time()/1000)
        if new_position:
            self.position = new_position

        self.__evaluate_state()
        self.__evaluate_movement(clock)

        if self.state == LaserState.Recovery:
            self.width = (self.starting_width\
                        * (self.time_to_execute/LASER_ANTICIPATION_TIME))

    def render(self, display: "pygame.Surface"):
        """
        Renders the laser on a display.
        The function renders the laser in a different ways depending
        on its current state. If the state is anticipation then the
        laser renders as slightly faded self. If the state is attack,
        then the laser pritns as it should be, and if it is in recovery,
        the laser contracts.
        Parameters:
            display - pygame.Surface
                to print the player on the surface.
        """
        if self.state == LaserState.Anticipation:
            new_color = (self.color[0]/2, self.color[1]/2, self.color[2]/2)
            pygame.draw.line(display,
                            new_color,
                            tuple(self.position),
                            tuple(self.position+self.direction),
                            round(self.width))

        elif self.state == LaserState.Attack:
            pygame.draw.line(display,
                            self.color,
                            tuple(self.position),
                            tuple(self.position+self.direction),
                            self.width)
            # pygame.draw.line(display,
            #                 WHITE,
            #                 tuple(self.position),
            #                 tuple(self.direction),
            #                 round(self.width/3))
        else:
            pygame.draw.line(display,
                            WHITE,
                            tuple(self.position),
                            tuple(self.position+self.direction),
                            round(self.width))

    def switch_state(self, state: "LaserState"):
        """
        Changes the state of the laser to the given state.
        """
        if state == LaserState.Attack:
            self.state = LaserState.Attack
            self.cooldown = self.time_to_execute-LASER_ANTICIPATION_TIME
        elif state == LaserState.Recovery:
            self.state = LaserState.Recovery
            self.time_to_execute = LASER_ANTICIPATION_TIME
            self.cooldown = LASER_ANTICIPATION_TIME

    def __evaluate_state(self):
        """
        Evaluates the current statec of the laser.
        States are in the order:
        Anticipation,
        Attack,
        Recovery.
        """
        if self.cooldown<=0:
            if self.state == LaserState.Anticipation:
                self.switch_state(LaserState.Attack)
            elif self.state == LaserState.Attack:
                self.switch_state(LaserState.Recovery)
            else:
                self.invalidate()


    def __evaluate_movement(self, clock: "pygame.time.Clock"):
        """
        Evaluates the movement of the laser, given the movement_types
        it was given.

        Parameters:
            clock -
                to scale movement with.
        """
        if self.movement_types[0] == LaserMovement.Constant:
            pass #nothing to do here

        elif self.movement_types[0] == LaserMovement.AcceleratingStart\
             and self.state == LaserState.Attack:

            if self.rotation_speed < self.max_rotation_speed:
                self.rotation_speed +=\
                    (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)

        elif self.movement_types[0] == LaserMovement.DeceleratingEnd\
            and self.state == LaserState.Attack\
            and self.time_to_execute < LASER_ANTICIPATION_TIME*2:

            if self.rotation_speed > self.min_rotation_speed:
                self.rotation_speed -=\
                    (clock.get_time()/1000)*self.control_rotation_speed
            else:
                self.movement_types.pop(0)


    def set_type(self,
        move_types: list["LaserMovement"] = [LaserMovement.Constant],
        control_rotation_speed: number_types = 0, #pi/s
        max_rotation_speed: number_types = 0, #pi/s
        min_rotation_speed: number_types = 0, #pi/s
        )->None:
        """
        Sets the type of movement for the laser.
        All speeds calculated with pi/s.
        Parameters:
            move_types -
                list of laser type movements.
            control_rotation_speed -
                at what speed should the laser accelerate/decelerate
            max_rotation_speed -
                the max speed the laser can reach.
            min_rotation_speed -
                the minimum speed at which the laser is rotating.
        """
        if not isinstance(move_types, list):
            move_types = [move_types]
        if move_types[-1] != LaserMovement.Constant:
            move_types.append(LaserMovement.Constant)
        self.movement_types = move_types
        self.control_rotation_speed = control_rotation_speed
        self.max_rotation_speed = max_rotation_speed
        self.min_rotation_speed = min_rotation_speed


    def get_end_point_in_map(self) -> Union["Vector2D", None]:
        """
        Returns the point at which the laser ends on the map
        Possible misscalculations may result in No point at all.
        (I blame the float for that)

        todo! documantation
        """

        def choose_intersection_point1(point: "Vector2D") -> "Vector2D":
            if point.x-50 < START_OF_MAP.x:
                return Vector2D(START_OF_MAP.x, point.y)
            return Vector2D(END_OF_MAP.x, point.y)

        def choose_intersection_point2(point: "Vector2D") -> "Vector2D":
            if point.y-50 < START_OF_MAP.y:
                return Vector2D(point.x, START_OF_MAP.y)
            return Vector2D(point.x, END_OF_MAP.y)


        if self.direction.x>0:
            intersection_point1 =\
                get_segment_intersection(
                    self.position,
                    self.position + self.direction,
                    RIGHT_UPPER_CORNER,
                    END_OF_MAP)
        else:
            intersection_point1 =\
                get_segment_intersection(
                    self.position,
                    self.position + self.direction,
                    START_OF_MAP,
                    LEFT_LOWER_CORNER)
        if self.direction.y>0:
            intersection_point2 =\
                get_segment_intersection(
                    self.position,
                    self.position + self.direction,
                    LEFT_LOWER_CORNER,
                    END_OF_MAP)
        else:
            intersection_point2 =\
                get_segment_intersection(
                    self.position,
                    self.position + self.direction,
                    START_OF_MAP,
                    RIGHT_UPPER_CORNER)

        if not intersection_point1:
            return choose_intersection_point2(intersection_point2[0])

        if not intersection_point2:
            return choose_intersection_point1(intersection_point1[0])

        if 1 > intersection_point1[1] > 0 and 1 > intersection_point2[1] > 0:
            if self.position.distance_to(intersection_point1[0])\
                > self.position.distance_to(intersection_point2[0]):
                return choose_intersection_point2(intersection_point2[0])
            else:
                return choose_intersection_point1(intersection_point1[0])

        if 1> intersection_point1[1] > 0:
            return choose_intersection_point1(intersection_point1[0])

        return choose_intersection_point2(intersection_point2[0])


    def is_colliding_with(self, other: "GameObject") -> bool:
        """
        Since this is a Laser object. This has a different collision
        type than the other objects.

        Definition: a game object colliding with the laser, when its
        radius of collision + the widhth of the laser is smaller
        than the distance between the centre of the object and the
        line segment. This also makes sure the object is are not behind
        the laser with.
        """

        # getting the Euclidic result from the vector -
        # object to the start of laser, and from the laser start.
        vector = self.position - other.centre_position()
        result = vector*self.direction

        # Checking if the object is not behind the laser
        if result > 0:
            return False

        # in any other case there might be actual collision
        # so we check for the distance between the line and
        # the object
        distance = distance_to_line_segment(other.centre_position(),
                                            self.position,
                                            self.position + self.direction)
        if distance <= other.radius + self.width*0.5:
            print(distance)
            print(other.radius + self.width*0.5)
            return True
        return False
