# Genetic Algorithm class
# Find the maximum value of Rosenbrock function

from random import random

class Individual:
    def __init__(self, lower, upper) -> None:
        self.lower = lower
        self.upper = upper
        self.genes = []
        for i in range(2):
            self.genes.append(random(lower, upper))
        self.fitness = 0
        self.calcFitness()

    def calcFitness(self) -> None:
        self.fitness = 100 * pow(pow(self.genes[0], 2) - self.genes[1], 2) + pow(1 - self.genes[0], 2)

    def mutation(self) -> None:
        for i in range(2):
            mut = random(self.genes[i] - self.lower, self.upper - self.genes[i])
            self.genes[i] += mut

class Population:
    def __init__(self, lower, upper, size) -> None:
        if size <= 0:
            print("The size of pupulation should be larger than 1, change it to 2")
            size = 2
        self.individuals = []
        for i in range(size):
            self.individuals.append(Individual(lower, upper))
        self.fittest_index = 0

    def getfittest(self) -> Individual:
        fittest = self.individuals[0]
        max_fitness = self.individuals[0].fitness
        self.fittest_index = 0
        for i in range(self.individuals.__len__()):
            ind = self.individuals[i]
            if ind.fitness > max_fitness:
                fittest = ind
                max_fitness = ind.fitness
                self.fittest_index = i
        return fittest
    
    def getTop2Fittest(self) -> list:
        top2 = []
        fittest = self.getfittest()
        top2.append(fittest)
        second_fittest = self.individuals[0]
        second_fitness = 0
        find_second = False
        for i in range(self.individuals.__len__()):
            ind = self.individuals[i]
            if find_second == False and i != self.fittest_index:
                find_second = True
                second_fittest = ind
                second_fitness = ind.fitness
            elif find_second == True and ind.fitness > second_fitness:
                second_fittest = ind
                second_fitness = ind.fitness
        top2.append(second_fittest)
        return top2
    
    def getLeastFittestIndex(self) -> int:
        min_fitness_sofar = self.individuals[0].fitness
        least_fittest_index_sofar = 0
        for i in range(self.individuals.__len__()):
            ind = self.individuals[i]
            if ind.fitness < min_fitness_sofar:
                min_fitness_sofar = ind.fitness
                least_fittest_index_sofar = i
        return least_fittest_index_sofar

class Genetic:
    def __init__(self, lower, upper, size) -> None:
        self.generation_count = 0
        self.population = Population(lower, upper, size)
        self.eps = 1e-6
        self.converged = False
        self.fitness = 0
    
    def selection(self) -> None:
        self.fittest, self.second_fittest = self.population.getTop2Fittest()
        self.fitness = self.fittest.fitness

    def crossover(self) -> None:
        crossover_point = random(0, 2)
        for i in range(crossover_point):
            tmp = self.fittest.genes[i]
            self.fittest.genes[i] = self.second_fittest.genes[i]
            self.second_fittest.genes[i] = tmp

    def mutation(self) -> None:
        self.fittest.mutation()
        self.second_fittest.mutation() 
    
    def getFittestOffspring(self) -> Individual:
        self.fittest.calcFitness()
        self.second_fittest.calcFitness()

        if self.fittest.fitness > self.second_fittest.fitness:
            return self.fittest
        else:
            return self.second_fittest

    def addFittestOffspring(self) -> None:
        idx = self.population.getLeastFittestIndex()
        self.population.individuals[idx] = self.getFittestOffspring()
        if abs(self.population.individuals[idx].fitness - self.fitness) < self.eps:
            self.converged = True

    def GA(self) -> None:
        print("Start searching...")
        while self.converged == False:
            self.selection()
            self.print_info()
            self.crossover()
            if random(1, 10) < 5:
                self.mutation()
            self.addFittestOffspring()
            self.generation_count += 1
        
        print("Stop.")
            
    def print_info(self) -> None:
        print("Generation: {0:d} fittest value: {1:f}".format(self.generation_count, self.fitness))

if __name__ == "__main__":
    slover = Genetic(-2.048, 2.048, 30)
    slover.GA()