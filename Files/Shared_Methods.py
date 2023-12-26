from Shared_constants import FLY_POINTS_IN_SECOND
from Shared_constants import WIDTH, HEIGHT, PADDING
from random import randint
import turtle

def save_obj_to_map(obj, map_):
        pol_bounds = obj.polygon.bounds
        pol_bounds = [int(b) for b in pol_bounds]
        x_values = [i for i in range(pol_bounds[0] - FLY_POINTS_IN_SECOND, pol_bounds[2] + FLY_POINTS_IN_SECOND) if i % FLY_POINTS_IN_SECOND == 0]
        y_values = [i for i in range(pol_bounds[1] - FLY_POINTS_IN_SECOND, pol_bounds[3] + FLY_POINTS_IN_SECOND) if i % FLY_POINTS_IN_SECOND == 0]
        for x in x_values:
            for y in y_values:
                loc = get_corresponding_location_in_map(map_, (x,y))
                loc.z = obj.get_location().z
                loc.obj_at_location = obj


def get_corresponding_location_in_map(map_, pos):
    cur_pos = (len(map_.map) - 1 - pos[0] // FLY_POINTS_IN_SECOND, pos[1] // FLY_POINTS_IN_SECOND)
    return map_.map[cur_pos[0]][cur_pos[1]]

def round_to_fly_points(value):
    return int(value) - int(value) % FLY_POINTS_IN_SECOND

async def create_free_map_coordinates(helper):
     while True:
        x = randint(0 + PADDING, WIDTH - PADDING)
        y = randint(0 + PADDING, HEIGHT - PADDING)
        if helper.is_intersects_any_polygon(helper.barriers, x, y):
             continue
        break
     return x, y

def create_text_turtle(position=None):
    text_turtle = turtle.Turtle()
    text_turtle.hideturtle()
    text_turtle.speed("fastest")
    text_turtle.color("black")
    if position is not None:
        text_turtle.goto(position[0], position[1])
    return text_turtle