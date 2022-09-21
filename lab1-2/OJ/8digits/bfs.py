# AcWing 845 Accepted
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

class EightDigits(BFS):
    def get_target_pos(self) -> None:
        for i in range(9):
            self.target_pos[int(self.target[i])] = i

    def __init__(self, origin, target) -> None:
        super().__init__(origin, target)
        self.target_pos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.get_target_pos()
        self.dr = [0, 0, -1, 1]
        self.dc = [1, -1, 0, 0]
    
    def coord(self, idx) -> tuple:
        x = idx // 3
        y = idx % 3
        return x, y
    
    def posi(self, x, y) -> int:
        return x * 3 + y
    
    def out_of_range(self, x, y) -> bool:
        if x < 0 or x > 2 or y < 0 or y > 2:
            return True
        else:
            return False

    def g(self, current, next) -> int:
        return self.closed[current] + 1
 
    def neighborhood(self, current) -> list:
        neighbor = []
        cur0_pos = 0
        for i in range(9):
            if current[i] == '0':
                cur0_pos = i
                break
        for i in range(4):
            r, c = self.coord(cur0_pos)
            rn = r + self.dr[i]
            cn = c + self.dc[i]
            if not self.out_of_range(rn, cn):
                next0_pos = self.posi(rn, cn)
                next = ""
                for j in range(9):
                    if j == cur0_pos:
                        next += current[next0_pos]
                    elif j == next0_pos:
                        next += current[cur0_pos]
                    else:
                        next += current[j]
                neighbor.append(next)
        return neighbor

if __name__ == "__main__":
    target = "123456780"
    digits = input().split()
    origin = ""
    for d in digits:
        if d == 'x':
            origin += '0'
        else:
            origin += d
    solver = EightDigits(origin, target)
    steps = solver.search()
    print(steps)