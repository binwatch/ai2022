# Lab1 8 digits puzzle
# Using A* algorithm

from astar import Astar

class EightDigits(Astar):
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

    def h(self, current) -> int:
        hsum = 0
        for i in range(9):
            if current[i] == '0':
                continue
            if current[i] != self.target[i]:
                hsum += 1
            #ri, ci = self.coord(i)
            #rj, cj = self.coord(self.target_pos[int(current[i])])
            #hsum += abs(ri - rj) + abs(ci - cj)
        return hsum 
    
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

def input_validation(origin, target):
    if origin.__len__() != 9:
        return False
    if target.__len__() != 9:
        return False
    cnt_origin = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    cnt_target = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        if origin[i] < '0' or origin[i] > '9':
            return False
        elif cnt_origin[int(origin[i])] >= 1:
            return False
        else:
            cnt_origin[int(origin[i])] += 1
        if target[i] < '0' or target[i] > '9':
            return False
        elif cnt_target[int(target[i])] >= 1:
            return False
        else:
            cnt_target[int(target[i])] += 1
    return True

if __name__ == "__main__":
    origin = input()
    target = input()
    if input_validation() == False:
        error_msg = '''Sorry, you need to enter 2 state in 2 lines
        \tand you can only use the characters in 012345678
        \tand each char must be used only once in each state string'''
        raise Exception(error_msg)
    solver = EightDigits(origin, target)
    steps = solver.search()
    print(steps)
    if steps != -1:
        solver.print_path_to_target()