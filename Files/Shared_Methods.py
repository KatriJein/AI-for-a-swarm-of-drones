from Shared_constants import FLY_POINTS_IN_SECOND


def get_corresponding_location_in_map(map_, pos):
    cur_pos = (len(map_.map) - 1 - pos[0] // FLY_POINTS_IN_SECOND, pos[1] // FLY_POINTS_IN_SECOND)
    return map_.map[cur_pos[0]][cur_pos[1]]

def round_to_fly_points(value):
    return int(value) - int(value) % FLY_POINTS_IN_SECOND