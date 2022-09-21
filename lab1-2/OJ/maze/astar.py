# AcWing 844 Accepted
# Using A* algorithm

from queue import PriorityQueue

class Astar:
    def __init__(self, origin, target) -> None:
        self.origin = origin
        self.target = target
        self.successor = dict()
        self.closed = dict()
    
    def g(self, current, next) -> int:
        return 0

    def h(self, current) -> int:
        return 0
    
    def neighborhood(self, current) -> list:
        return []

    def search(self) -> int:
        open = PriorityQueue();
        forigin = 0 + self.h(self.origin)
        open.put( (forigin, self.origin) )
        self.closed = dict()
        self.successor[self.origin] = None
        self.closed[self.origin] = 0

        while not open.empty():
            cur = open.get()
            fcur = cur[0]
            current = cur[1]
            # find the target
            if current == self.target:
                return fcur
            # have met current with smaller f before, jump
            # if current in self.closed and self.closed[current] < fcur:
            #    continue
            # else
                # tarverse neighborhood of current
            for next in self.neighborhood(current):
                # estimate cost(of next) = 
                #   cost(from current to next) + estimate cost(from next to target) 
                gnext = self.g(current, next)
                if next not in self.closed or gnext < self.closed[next]:
                    # if bigger f exist in closed, remove it
                    #if next in self.closed:
                    #    del self.closed[next]
                    self.closed[next] = gnext
                    fnext = gnext + self.h(next)
                    open.put( (fnext, next) )
                    self.successor[next] = current
        # cannot reach the target
        return -1

    def print_path(self, current):
        if current == None:
            return
        else:
            self.print_path(self.successor[current])
            print(current)

    def print_path_to_target(self):
        self.print_path(self.target)

class Maze(Astar):
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

    def h(self, current) -> int:
        return abs(current[0] - self.target[0]) + abs(current[1] - self.target[1])
    
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