from collections import Counter


class Game(object):
    def __init__(self):
        self.state = {}
        self.step = 0
        self.started = False

    def change(self, state):
        """
        Evolve game to next state based on input state,
        and increment the game step
        """
        self.state = next_loop(state)
        self.step += 1

    def current(self):
        """
        Return current living cells 
        """
        return self.state

    def time(self):
        """
        Internal steps of game
        """
        return self.step

    def reset_time(self):
        """
        Reset internal steps of game to 0
        """
        self.step = 0

    def start(self):
        """
        Set game state as started
        """
        self.started = True

    def stop(self):
        """
        Set game state as stopped 
        """
        self.started = False


def transform_input(target):
    def tuple_each(pair):
        return pair['x'], pair['y']
    
    return set(map(tuple_each, target))


def transform_output(target):
    return map(lambda p: {
        'x': p[0], 
        'y': p[1],
        'alive': 'O',
        'color': 'red'
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
    game = Game()
    alive = {(0, 0), (1, 0), (2, 0), (5, 6), (5, 7), (5, 8)}
    print(str(game.current()))
    pass
