import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

genetic_length = 12

class Individual(object):
    def __init__(self) -> None:
        self.__genetic_length = genetic_length
        self.__gene_x = []
        self.__gene_y = []
        self.x = 0.0
        self.y = 0.0
        self.__phenotype = 0
        self.__fitness = 0
 
    def random_create_genetic(self) -> None:
        for i in range(self.__genetic_length):
            self.__gene_x.append(random.randint(0, 1))
            self.__gene_y.append(random.randint(0, 1))
        self.calculate_phenotype()

    def get_genes(self) -> tuple:
        return self.__gene_x, self.__gene_y
    
    def set_genetic(self, genetic_x, genetic_y) -> None:
        self.__gene_x = genetic_x
        self.__gene_y = genetic_y
        self.calculate_phenotype()
    
    def calculate_xy(self) -> None:
        self.x = 0
        self.y = 0
        for i in range(self.__genetic_length):
            self.x = self.x * 2 + self.__gene_x[i]
            self.y = self.y * 2 + self.__gene_y[i]

        self.x = (self.x - 2048) / 1000
        self.y = (self.y - 2048) / 1000

    def calculate_phenotype(self) -> None:
        self.calculate_xy()
        self.__phenotype = 100 * (self.x**2 - self.y)**2 + (1 - self.x)**2
    
    def get_xy(self) -> tuple:
        return self.x, self.y
    
    def get_phenotype(self) -> float:
        return self.__phenotype
    
    def mutation(self) -> None:
        x_mutation_num = random.randint(0, 2)
        y_mutation_num = random.randint(0, 2)

        for i in range(x_mutation_num):
            position = random.randint(0, self.__genetic_length - 1)
            self.__gene_x[position] = random.randint(0, 1)
        
        for i in range(y_mutation_num):
            position = random.randint(0, self.__genetic_length - 1)
            self.__gene_y[position] = random.randint(0, 1)
        
        self.calculate_phenotype()

    def set_fitness(self, fitness) -> None:
        self.__fitness = fitness
    
    def get_fitness(self):
        return self.__fitness

class GeneticAlgorithm(object):
    def __init__(self, population_size) -> None:
        self.__population_size = population_size
        self.__population = []

        self.init_population()
        self.update_fitness()

        self.__max_x_array=[]
        self.__max_y_array=[]
        self.__max_z_array=[]

        self.__eps = 1e-6
        self.__converged = False
        self.__generation = 0

    def init_population(self) -> None:
        for i in range(self.__population_size):
            individual = Individual()
            individual.random_create_genetic()
            self.__population.append(individual)
 
    def update_fitness(self) -> None:
        total_fitness = 0

        for individual in self.__population:
            total_fitness = total_fitness + individual.get_phenotype()
        
        for individual in self.__population:
            individual_fitness = individual.get_phenotype()
            individual.set_fitness(individual_fitness/total_fitness)
    
    def selection(self, kill_number) -> None:
        self.__population = sorted(self.__population, key= lambda individual:individual.get_fitness(), reverse=True)

        self.__population[0].calculate_phenotype()
        position = self.__population[0].get_xy()
        self.__max_x_array.append(position[0])
        self.__max_y_array.append(position[1])
        self.__max_z_array.append(self.__population[0].get_phenotype())
            
        self.print_info()

        # kill individuals
        self.__population = self.__population[0 : self.__population_size - kill_number]
        self.__population_size -= kill_number
    
    def crossover(self, add_number):
        # choose parents from origin population
        current_pNumber = self.__population_size

        for i in range(add_number):
            pa0idx = random.randint(0, current_pNumber - 1)
            pa1idx = random.randint(0, current_pNumber - 1)
            while pa1idx == pa0idx:
                pa1idx = random.randint(0, current_pNumber - 1)
            pa0_genetic_x, pa0_genetic_y = self.__population[pa0idx].get_genes()
            pa1_genetic_x, pa1_genetic_y = self.__population[pa1idx].get_genes()

            crossover_point = random.randint(4, 9)

            genetic_x = pa0_genetic_x[0 : crossover_point] + pa1_genetic_y[crossover_point : genetic_length]
            genetic_y = pa0_genetic_y[0 : crossover_point] + pa1_genetic_x[crossover_point : genetic_length]

            current_individual = Individual()
            current_individual.set_genetic(genetic_x, genetic_y)
            current_individual.mutation()
            self.__population.append(current_individual)
        
    def evolution(self, times) -> None:

        # while not self.converged:
        for i in range(times):
            num = (int)(self.__population_size * random.uniform(0.2, 0.5))
            self.selection(num)
            self.crossover(num)
            self.update_fitness()
            self.__generation += 1
    
    def get_max(self) -> float:
        self.__population = sorted(self.__population, key= lambda individual:individual.get_fitness(), reverse=True)
        return self.__population[0].get_phenotype()
    
    def draw(self) -> None:
        # 3D figure
        fig = plt.figure()
        ax = Axes3D(fig)

        # range of x and y
        x = np.arange(-2.048, 2.048, 0.05)
        y = np.arange(-2.048, 2.048, 0.05)
        
        # generate mesh
        X, Y = np.meshgrid(x, y)
        
        # draw 3D surface of Rosenbrock function
        Z = np.array(100 * (X**2 - Y)**2 + (1 - X)**2)
        ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap = plt.get_cmap('rainbow'))
        # set dimension of z axis
        ax.set_zlim(-1000, 4000)
        
        # draw search path (generations)
        A = np.array(self.__max_x_array)
        B = np.array(self.__max_y_array)
        C = np.array(self.__max_z_array)
        ax.plot(A, B, C, 'b', label='parametric curve')
        
        plt.show()
    
    def print_info(self) -> None:
        fittest_phenotype = self.__population[0].get_phenotype()
        x, y = self.__population[0].get_xy()
        print("Generation: {0:d} fittest value: {1:f} x1: {2:f} x2: {3:f}".format(self.__generation, fittest_phenotype, x, y))

def main() -> None:
    solver = GeneticAlgorithm(50)
    solver.evolution(100)
    solver.draw()

if __name__ == '__main__':
    main()