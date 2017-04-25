from collections import Counter
from itertools import tee, filterfalse, chain
from re import sub


class Game(object):
    def __init__(self):
        self.state = {}

    def change(self, state):
        self.state = next_loop(state)

    def current(self):
        return self.state


def transform_input(target):
    """
    Transform client input to game input format.
    
    :param target: [Dict] Client protocol payload 
    :return: [Set] Cell position only for game input
    """
    def tuple_each(pair):
        return pair['x'], pair['y']

    return set(map(tuple_each, target))


def transform_output(color, target):
    """
    Update reproduction cell color
    
    :param color: [String] RGB color in string format
    :param target: [Set] Next state of input cell
    :return: [Set] [Set] Next state of input cell with different color
    """
    neighbour, reproduction = partition(lambda p: p[1] == 3, target)
    avg_color = average_color(color)
    return chain(map(lambda p: template(color, p[0]), neighbour),
                 map(lambda p: template(avg_color, p[0]), reproduction))


def average_color(color):
    """
    Calculate average color of input color.
    
    :param color: [String] RGB color in string format 
    :return: [String] Average RGB color in string format
    """
    rgb = color.split(',')
    remove_sym = map(lambda s: sub(r'[a-zA-Z()]+', '', s), rgb)
    str_to_int = map(lambda n: str(int(int(n) / 3)), remove_sym)
    to_rgb = 'rgb(' + ','.join(str_to_int) + ')'
    return to_rgb


def neighbours(current):
    """
    Find neighbours of current cell.
    
    :param current: [Tuple] X Y Position of cell 
    :return: [List] List of neighbours
    """
    x, y = current
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def find_neighbours(board):
    """
    Find all neighbour cell.
    
    :param board: [Set] Current state of cells 
    :return: [Object] Neighbour count of each cell
    """
    return Counter(nb for cell in board
                   for nb in neighbours(cell))


def next_loop(board):
    """
    Return count of reproduction cell & neighbour cell.
     
    :param board: [Set] Current state of cell
    :return: [Set] Next state of input cell
    """
    possible_cells = counts = find_neighbours(board)
    return {(cell, counts[cell]) for cell in possible_cells
            if (counts[cell] == 3)
            or (counts[cell] == 2 and cell in board)}


def template(color, position):
    """
    Template json for client.
    
    :param color: [String] RGB in string format 
    :param position: [Tuple] X Y Position of cell
    :return: [Dict] Information of cell
    """
    return {
        'x': position[0],
        'y': position[1],
        'alive': ['O', 'X'],
        'color': [color, 'rgb(255,255,255)']
    }


def partition(condition, elements):
    t1, t2 = tee(elements)
    return filterfalse(condition, t1), filter(condition, t2)


if __name__ == '__main__':
    alive = {(1, 0), (3, 0), (2, 0), (10, 1), (10, 2), (10, 3)}
    game = Game()
    game.change(alive)
    print(str(game.current()))
    pass
