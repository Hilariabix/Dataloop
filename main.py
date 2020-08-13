import os
import argparse
import enum
import numpy as np

STEPS = ((-1, 0), (0, -1), (0, 1), (1, 0))


class BoardComponents(enum.Enum):
    FREE_PATH = 0
    WALL = 1
    GHOST = 2
    PACMAN = 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, point: Point, dist):
        self.point = point
        self.dist = dist


def get_ghost_and_pacman_locations(board):
    pacman = tuple(zip(*np.where(board == BoardComponents.PACMAN.value)))
    ghosts = list(zip(*np.where(board == BoardComponents.GHOST.value)))
    return pacman, ghosts


def valid_point(row, col, board):
    valid = (row >= 0) and (row < len(board)) and (col >= 0) and (col < len(board[0])) and \
            board[row][col] == BoardComponents.FREE_PATH.value
    return valid


def bfs(board, pacman, ghost):
    if board[pacman.x][pacman.y] == BoardComponents.WALL.value or board[ghost.x][ghost.y] == BoardComponents.WALL.value:
        return -1

    visited = np.zeros((len(board), len(board[0])), dtype=bool)
    visited[pacman.x][pacman.y] = True

    q = []
    s = Node(pacman, 0)
    q.append(s)

    while q:
        curr = q.pop(0)
        curr_point = curr.point
        if curr_point.x == ghost.x and curr_point.y == ghost.y:
            return curr.dist

        for step in STEPS:
            row = curr_point.x + step[0]
            col = curr_point.y + step[1]
            dist = curr.dist+1
            if valid_point(row, col, board) and not visited[row][col]:
                visited[row][col] = True
                new_node = Node(Point(row, col), dist)
                q.append(new_node)
            elif row == ghost.x and col == ghost.y:
                return dist

    return -1


def main():
    res = []
    parser = argparse.ArgumentParser("")
    parser.add_argument("--board", action="store", required=True, type=os.path.abspath,
                        help="The board - numpy nd-array file path")
    args = parser.parse_args()

    board = np.load(args.board)
    pacman, ghosts = get_ghost_and_pacman_locations(board)
    pacman = Point(*pacman[0])
    for ghost in ghosts:
        dist = bfs(board, pacman, Point(*ghost))
        if dist != -1:
            res.append([ghost, dist])
    print(res)


if __name__ == "__main__":
    main()
