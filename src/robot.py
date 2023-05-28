import random
import numpy as np
import config

class Robot:
    def __init__(self, id: int) -> None:
        self.id = id
        self.position_x = config.ROBOTS_DEPLOY_POINT_X
        self.position_y = config.ROBOTS_DEPLOY_POINT_Y
        self.searching = True
        self.own_best_reading = -1
        self.own_best_reading_location = (-1, -1)
        self.global_best_reading = -1
        self.global_best_reading_location = (-1 ,-1)

    def get_own_best(self) -> float:
        return self.own_best_reading
    
    def get_own_best_location(self) -> tuple[int ,int]:
        return self.own_best_reading_location
    
    def get_global_best(self) -> float:
        return self.global_best_reading
    
    def get_global_best_location(self) -> tuple[int ,int]:
        return self.global_best_reading_location

    def get_id(self) -> int:
        return self.id

    def get_position_x(self) -> int:
        return self.position_x
    
    def get_position_y(self) -> int:
        return self.position_y
    
    def is_searching(self) -> bool:
        return self.searching

    def move(self) -> None:
        self.position_x = self.position_x + random.choice([-1, 1])
        self.position_y = self.position_y + random.choice([-1, 1])
        self.adjust_move()

    def adjust_move(self) -> None:
        # Adjust x position to map boundaries
        if (self.position_x < 0):
            self.position_x = 0
        if (self.position_x > config.MAP_SIZE[0]):
            self.position_x = config.MAP_SIZE[0]
        # Adjust y position to map boundaries
        if (self.position_y < 0):
            self.position_y = 0
        if (self.position_y > config.MAP_SIZE[1]):
            self.position_y = config.MAP_SIZE[1]

    def scan(self, search_map) -> None:
        # Check if better than global best
        if (search_map[self.position_x, self.position_y] > self.global_best_reading):
            self.global_best_reading = search_map[self.position_x, self.position_y]
            self.global_best_reading_location = (self.position_x, self.position_y)
        # Check if better than own best
        if (search_map[self.position_x, self.position_y] > self.own_best_reading):
            self.own_best_reading = search_map[self.position_x, self.position_y]
            self.own_best_reading_location = (self.position_x, self.position_y)
        # Check if satisfactory reading was found
        if (self.own_best_reading >= config.SATISFACTORY_THRESHOLD):
            self.searching = False

    def broadcast_known_best(self, robots: list["Robot"]) -> None:
        for robot in robots:
            if (robot == self):
                continue
            # Check if other robot is in comms range
            own_pos = np.array((self.position_x, self.position_y))
            robot_pos = np.array((robot.get_position_x(), robot.get_position_y()))
            if (np.linalg.norm(own_pos - robot_pos) <= config.COMMS_RANGE):
                robot.receive(self.global_best_reading, self.global_best_reading_location)

    def receive(self, other_best_reading, other_best_reading_location) -> None:
        # Known global best will always be greater than or equal to personal best
        if (other_best_reading > self.global_best_reading):
            self.global_best_reading = other_best_reading
            self.global_best_reading_location = other_best_reading_location
        if (other_best_reading >= config.SATISFACTORY_THRESHOLD):
            self.searching = False


