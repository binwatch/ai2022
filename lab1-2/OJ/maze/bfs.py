# AcWing 844 Accepted
# Using BFS algorithm

from queue import Queue

class BFS:
    def __init__(self, origin, target) -> None:
        self.origin = origin
        self.target = target
        self.successor = dict()
        self.closed = dict()
    
    def g(self, current, next) -> int:
        return 0
    
    def neighborhood(self, current) -> list:
        return []

    def search(self) -> int:
        open = Queue();
        open.put(origin, 0)
        self.closed = dict()
        self.successor[self.origin] = None
        self.closed[self.origin] = 0

        while not open.empty():
            current = open.get()

            if current == self.target:
                return self.closed[current]

            for next in self.neighborhood(current):
                gnext = self.g(current, next)
                if next not in self.closed:
                    self.closed[next] = gnext
                    open.put( next, gnext )
                    self.successor[next] = current
        return -1

    def print_path(self, current):
        if current == None:
            return
        else:
            self.print_path(self.successor[current])
            print(current)

    def print_path_to_target(self):
        self.print_path(self.target)

class Maze(BFS):
    def __init__(self, rows, cols, maze, origin, target) -> None:
        super().__init__(origin, target)
        self.rows = rows
        self.cols = cols
        self.maze = maze
        self.dr = [0, 0, -1, 1]
        self.dc = [1, -1, 0, 0]

    def out_of_range(self, x, y) -> bool:
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return True
        else:
            return False

    def g(self, current, next) -> int:
        return self.closed[current] + 1
    
    def neighborhood(self, current) -> list:
        neighbor = []
        for i in range(4):
            r, c = current
            rn = r + self.dr[i]
            cn = c + self.dc[i]
            if self.out_of_range(rn, cn):
                continue
            elif self.maze[rn][cn] == 0:
                next = (rn, cn)
                neighbor.append(next)
        return neighbor

if __name__ == "__main__":
    sn, sm = input().split()
    n = int(sn)
    m = int(sm)
    origin = (0, 0)
    target = (n-1, m-1)
    # read in the maze matrix
    maze = []
    for i in range(n):
        rowi = []
        rowis = input().split()
        for j in range(m):
            x = int(rowis[j])
            rowi.append(x)
        maze.append(rowi)
    solver = Maze(n, m, maze, origin, target)
    steps = solver.search()
    print(steps)