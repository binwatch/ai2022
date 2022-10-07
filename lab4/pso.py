import random
import numpy as np
import matplotlib.pyplot as plt

class PSO(object):
    def __init__(self, dimension, iterations, population_size, b_low, b_up, v_low, v_high, fitness_function, c1, c2, w) -> None:
        self.__dimension = dimension
        self.__iterations = iterations
        self.__population_size = population_size
        self.__bound = []
        self.__bound.append(b_low)
        self.__bound.append(b_up)
        self.__velocity = []
        self.__velocity.append(v_low)
        self.__velocity.append(v_high)
        self.__fitness_function = fitness_function
        self.__c1 = c1
        self.__c2 = c2
        self.__w = w

        self.__x = np.zeros((self.__population_size, self.__dimension))
        self.__v = np.zeros((self.__population_size, self.__dimension))
        self.__p_best = np.zeros((self.__population_size, self.__dimension))
        self.__g_best = np.zeros((1, self.__dimension))[0]

        best_fitness = -1000000
        for i in range(self.__population_size):
            for j in range(self.__dimension):
                self.__x[i][j] = random.uniform(self.__bound[0][j], self.__bound[1][j])
                self.__v[i][j] = random.uniform(self.__velocity[0], self.__velocity[1])
            self.__p_best[i] = self.__x[i]
            fitness = self.__fitness_function(self.__p_best[i])
            if fitness > best_fitness:
                self.__g_best = self.__p_best[i]
                best_fitness = fitness
    
    def update(self) -> None:
        for i in range(self.__population_size):
            # update velocity
            self.__v[i] = self.__w * self.__v[i] + self.__c1 * random.uniform(0, 1) * (
                self.__p_best[i] - self.__x[i]) + self.__c2 * random.uniform(0, 1) * (
                self.__g_best - self.__x[i])
            for j in range(self.__dimension):
                if self.__v[i][j] < self.__velocity[0]:
                    self.__v[i][j] = self.__velocity[0]
                if self.__v[i][j] > self.__velocity[1]:
                    self.__v[i][j] = self.__velocity[1]
            
            # update position
            self.__x[i] = self.__x[i] + self.__v[i]
            for j in range(self.__dimension):
                if self.__x[i][j] < self.__bound[0][j]:
                    self.__x[i][j] = self.__bound[0][j]
                if self.__x[i][j] > self.__bound[1][j]:
                    self.__x[i][j] = self.__bound[1][j]
            
            # update p_best and g_best
            fitness =  self.__fitness_function(self.__x[i])
            if fitness > self.__fitness_function(self.__p_best[i]):
                self.__p_best[i] = self.__x[i]
            if fitness > self.__fitness_function(self.__g_best):
                self.__g_best = self.__x[i]

    def evolution(self) -> None:
        self.__path = []
        self.__best = self.__g_best
        self.__best_fitness = self.__fitness_function(self.__best)
        for generation in range(self.__iterations):
            self.update()
            g_fitness = self.__fitness_function(self.__g_best)
            if g_fitness > self.__best_fitness:
                self.__best = self.__g_best
                self.__best_fitness = g_fitness
            print('generation: {0:d} best position: {1} best fitness: {2:f}'.format(generation, self.__best, self.__best_fitness))
            self.__path.append(self.__best_fitness)
    
    def draw(self, id, title) -> None:
        t = [i for i in range(self.__iterations)]
        plt.figure()
        plt.plot(t, self.__path, color='blue', marker='.', ms=15)
        plt.margins(0)
        plt.xlabel("generation")
        plt.ylabel("fitness")
        result = ' best result: (' + ', '.join(str(x) for x in self.__best) + ')' 
        plt.title(title + result)
        fig_path = 'figures/' + 'pso_' + str(id) + '.png'
        plt.savefig(fig_path)

if __name__ == '__main__':

    dimension = 2

    def f1(x) -> float:
        return 30*x[0] - x[1]

    def f2(x) -> float:
        return 30*x[1] - x[0]

    def f3(x) -> float:
        return x[0]**2 - x[1]/2

    def f4(x) -> float:
        return 20*x[1]**2 - 500*x[0]
    
    f = [f1, f2, f3, f4]
    title = ["30*x - y", "30*y - x", "x^2 - y/2", "20*y^2 - 500*x"]

    iterations = 50
    population_size = 100

    c1 = 2.0
    c2 = 2.0
    w = 0.8

    b_low = [
        [0, 0],
        [0, 30],
        [30, 0],
        [30, 30]
    ]
    b_up = [
        [30, 30],
        [30, 60],
        [60, 30],
        [60, 60]
    ]
    v_low = -0.5
    v_high = 0.5

    for i in range(4):
        print("-------------------------- " + title[i] + " --------------------------")
        slover = PSO(dimension, iterations, population_size, b_low[i], b_up[i], v_low, v_high, f[i], c1, c2, w)
        slover.evolution()
        slover.draw(i, title[i])
        print("-------------------------------- end --------------------------------")

