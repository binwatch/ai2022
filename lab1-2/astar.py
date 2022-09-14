# lab1: 8 digits puzzle
# using A* Search algorithm

from queue import PriorityQueue

def input_validation():
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

def get_target_pos():
    for i in range(9):
        target_pos[int(target[i])] = i

def coord(idx):
    x = idx // 3
    y = idx % 3
    return x, y

def posi(x, y):
    return x * 3 + y

def out_of_range(x, y):
    if x < 0 or x > 2 or y < 0 or y > 2:
        return True 
    else:
        return False

def h_to_target(n):
    h_sum = 0
    for i in range(9):
        if n[i] == '0':
            continue
        ri, ci = coord(i)
        rj, cj = coord(target_pos[int(n[i])])
        h_sum += abs(ri - rj) + abs(ci - cj)
    return h_sum

def A_star():
    open = PriorityQueue()
    open.put((h_to_target(origin), origin)) 
    g = dict()
    successor[origin] = None
    g[origin] = 0

    while not open.empty():
        current = open.get()[1]

        if current == target:
            return g[current]
        c0 = 0
        for i in range(9):
            if current[i] == '0':
                c0 = i
                break
        for i in range(4):
            r, c = coord(c0)
            nr = r + dr[i]
            nc = c + dc[i]
            if out_of_range(nr, nc) == True:
                continue
            n0 = posi(nr, nc)
            next = ""
            for j in range(9):
                if j == c0:
                    next += current[n0]
                elif j == n0:
                    next += current[c0]
                else:
                    next += current[j] 
            ng = g[current] + 1
            if next not in g or ng < g[next]:
                g[next] = ng
                f = ng + h_to_target(next)
                open.put((f, next))
                successor[next] = current

    return -1 

def print_path(current):
    if current == None:
        return
    else:
        print_path(successor[current])
        print(current)

if __name__ == "__main__":
    dr = [0, 0, -1, 1]
    dc = [1, -1, 0, 0]
    target_pos = [0, 1, 2, 3, 4, 5, 6, 7, 8]    # query position by number
    successor = dict()
    origin = input()    # origin state
    target = input()    # target state
    if input_validation() == False:
        error_msg = '''Sorry, you need to enter 2 state in 2 lines
        \tand you can only use the characters in 012345678
        \tand each char must be used only once in each state string'''
        raise Exception(error_msg)
    get_target_pos()
    #print(h_to_target(origin))
    steps = A_star()
    print(steps)
    if steps != -1: 
        print_path(target)