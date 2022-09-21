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
