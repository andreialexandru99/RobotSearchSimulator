import matplotlib.pyplot as plt
import numpy as np
import config

from perlin_numpy import generate_fractal_noise_2d
from robot import Robot


def init_search():
    search_map = generate_fractal_noise_2d(config.MAP_SIZE, config.MAP_RES, config.PERLIN_OCTAVES)
    search_map = (search_map - search_map.min()) / (search_map.max() - search_map.min()) * 255

    robots = [Robot(i) for i in range(config.ROBOTS_COUNT)]
    
    np.random.seed(0)
    fig = plt.figure()
    return (search_map, robots, fig)


# Global variables needed for consecutive calls of the plot_search_state method
# used to clear old scatter plots used to represent robot positions
robots_searching_scatter = None
robots_done_scatter = None

def plot_search_state(robots: list["Robot"], search_map):
    global robots_searching_scatter
    global robots_done_scatter

    # Plot search map
    plt.imshow(search_map, cmap='gray', interpolation='lanczos', origin='lower')
    
    # Clear old robot positions scatter plots
    if robots_searching_scatter:
        robots_searching_scatter.remove()
    if robots_done_scatter:
        robots_done_scatter.remove()

    # Compute and add new robot scatter plots
    robots_searching_x = [robot.get_position_x() for robot in robots if robot.is_searching()]
    robots_searching_y = [robot.get_position_y() for robot in robots if robot.is_searching()]
    robots_done_x = [robot.get_position_x() for robot in robots if not robot.is_searching()]
    robots_done_y = [robot.get_position_y() for robot in robots if not robot.is_searching()]
    robots_searching_scatter = plt.scatter(
        x=robots_searching_x,
        y=robots_searching_y,
        c=config.ROBOTS_COLOR_SEARCHING,
        s=config.ROBOTS_SIZE
    )
    robots_done_scatter = plt.scatter(
        x=robots_done_x,
        y=robots_done_y,
        c=config.ROBOTS_COLOR_DONE,
        s=config.ROBOTS_SIZE
    )

    plt.pause(config.STEP_INTERVAL)


def is_search_over(robots: list["Robot"]) -> bool:
    for robot in robots:
        if robot.is_searching():
            return False
    return True


def perform_search_step(robots: list["Robot"], search_map) -> None:
    for robot in robots:
        robot.scan(search_map)
        robot.broadcast_known_best(robots)
        robot.move()

def print_global_best(robots: list["Robot"]) -> None:
    for robot in robots:
        print(f'Robot {robot.get_id()} found value {robot.get_own_best()} at position {robot.get_own_best_location()}.'
              + f' Best known value is {robot.get_global_best()} at position {robot.get_global_best_location()}.')

def main():
    (search_map, robots, _) = init_search()

    while not is_search_over(robots):
        perform_search_step(robots, search_map)
        plot_search_state(robots, search_map)
    
    print_global_best(robots)
    plt.show()


if __name__ == "__main__":
    main()