class LevelManager:
    def __init__(self):
        self.level = 0
        self.level_maps = {0: {"maze_name": "first_maze.txt", "pellet_name": "pellets_first_maze.txt", "row": 0,
                               "fruit": "cherry"}}

    def next_level(self):
        self.level += 1

    def reset_game(self):
        self.level = 0

    def get_level_map(self):
        return self.level_maps[self.level % len(self.level_maps)]