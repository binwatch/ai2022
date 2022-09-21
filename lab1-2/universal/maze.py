# Lab2 maze puzzle
# Using A* algorithm

from astar import Astar

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
    if steps != -1:
        solver.print_path_to_target()