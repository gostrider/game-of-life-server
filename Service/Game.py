from collections import Counter


class Game(object):
    def __init__(self):
        self.state = {}
        self.step = 0
        self.started = False

    def change(self, state):
        self.state = next_loop(state)
        self.step += 1

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

    def addOne(self, number=1):
        return number + 1

    def getTwo(self):
        return 2

    def do(self, payload):
        return {
            "a": self.addOne(payload['number']),
            "b": self.getTwo()
        }[payload['action']]


def transform_input(target):
    def tuple_each(pair):
        return pair['x'], pair['y']

    return set(map(tuple_each, target))


def transform_output(color, target):
    return map(lambda p: {
        'x': p[0],
        'y': p[1],
        'alive': ['O', 'X'],
        'color': [color, 'rgb(255,255,255)']
        }, target)


"""
    type Coord = (Int, Int)
    type Board = [Cell]
    type Cell = Coord
"""


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
    alive = {(1, 0), (3, 0), (2, 0), (5, 6), (5, 7), (5, 8)}
    game = Game()
    game.change(alive)
    print(str(game.current()))
    pass
