from collections import Counter

"""
type Coord = (Int, Int)
type Board = [Cell]
type Cell = Coord
"""


class Game(object):
    def __init__(self):
        self.state = {}
        self.step = 0
        self.started = False

    def change(self, state):
        self.state = next_loop(state)
        self.step += 1
        return self.state

    def current(self):
        return self.state

    def time(self):
        return self.step

    def reset_time(self):
        self.step = 0

    def start(self):
        self.started = True

    def stop(self):
        self.started = False


def transform_input(target):
    return set(map(tuple, target))


def neighbours(current):
    """
    neighbours :: Coord -> [Coord]
    
    :param current: Current cell coordinate 
    :return: Neighbour coordinate of current cell 
    """

    x, y = current
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def find_neighbours(board):
    """
    find_neighbours :: Board -> Counter [Cell -> Count]
    
    :param board: Current state of world
    :return: All count of neighbours of current world
    """
    return Counter(nb for cell in board
                   for nb in neighbours(cell))


def next_loop(board):
    """
    change :: Board -> Board
    
    :param board: 
    :return: 
    """
    possible_cells = counts = find_neighbours(board)
    return {cell for cell in possible_cells
            if (counts[cell] == 3)
            or (counts[cell] == 2 and cell in board)}


if __name__ == '__main__':
    game = Game()
    alive = {(0, 0), (1, 0), (2, 0), (5, 6), (5, 7), (5, 8)}
    game.change(game.change(alive))
    print(str(game.current()))
    pass
