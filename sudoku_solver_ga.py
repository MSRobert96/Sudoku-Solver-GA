import numpy as np
from numpy.random import choice
import time

GENES = {1,2,3,4,5,6,7,8,9}
MAX_SCORE = 162
POP_SIZE = 2000
MUT_RATE = 0.1
ELITE_NUM = 50

TEST_CASE = (
    '37. 5.. ..6'
    '... 36. .12'
    '... .91 75.'
    '... 154 .7.'
    '..3 .7. 6..'
    '.5. 638 ...'
    '.64 98. ...'
    '59. .26 ...'
    '2.. ..5 .64'
).replace('.', '0').replace(' ', '')

class Individual:
    '''
    Represents an individual of the population.
    Each individual contains its own `genes` and `fixed_genes`.
    Individuals can `crossover` and `mutate`.
    Individuals have a `fitness` score between 0 and 1
    '''

    def __init__(self, genes, fixed_genes, init = False):
        self.fixed_genes = fixed_genes
        self.genes = genes
        if init: self.fill()
        self.calc_fitness()

    def calc_fitness(self):
        '''Updates the fitness score of the individual'''
        score = 0
        # rows scores
        score += sum([np.unique(col).size for col in self.genes.T])
        # boxes scores
        for r,c in [(0,0),(0,3),(0,6),
                    (3,0),(3,3),(3,6),
                    (6,0),(6,3),(6,6)]:
            score += np.unique(self.genes[r:r+3,c:c+3]).size
        self.fitness = (score / MAX_SCORE) ** 10
    
    def crossover(self, partner):
        '''Create a child with a `partner`, with a random crossover point'''
        new_genes = self.genes.copy()
        from_partner = np.random.randint(1,9)
        new_genes[-from_partner:] = partner.genes[-from_partner:].copy()
        return Individual(new_genes, self.fixed_genes)

    def mutate(self):
        '''Swap values in a row, according to a mutation rate'''
        if np.random.random() < MUT_RATE:
            row = np.random.randint(0,9)
            cells = np.random.permutation(np.argwhere(~self.fixed_genes[row]))
            c1, c2 = cells[0], cells[1]
            self.genes[row,c1], self.genes[row,c2] = self.genes[row,c2], self.genes[row,c1]
            self.calc_fitness()

    def fill(self):
        '''Fills empty cells of each row with a random permutation of genes'''
        for row in range(9):
            assignable = GENES - set(self.genes[row][self.fixed_genes[row]])
            self.genes[row][~self.fixed_genes[row]] = np.random.permutation(list(assignable))

    def __str__(self):
        return '<Individual fit: {:.4f}, content: [{}] />'.format(self.fitness, ''.join(self.genes.flatten().astype(str)))


class Population:
    '''
    Represents the entire population of individuals.
    Population can evolve though selection and reproduction.
    '''

    def __init__(self, base_genes):
        self.base_genes = np.array(list(base_genes), dtype=int).reshape(9,9)
        self.initialize()
        self.generation = 1

    def initialize(self):
        '''Create the starting set of individuals'''
        fixed_genes = self.base_genes > 0
        self.individuals = []
        for _ in range(POP_SIZE):
            self.individuals.append(Individual(self.base_genes.copy(), fixed_genes, init=True))
        self.calc_stats()

    def calc_stats(self):
        '''Calculation of internal stats of the population'''
        self.max_fitness = max([i.fitness for i in self.individuals])
        self.tot_fitness = sum([i.fitness for i in self.individuals])
        self.avg_fitness = self.tot_fitness / POP_SIZE
        self.probs = [i.fitness / self.tot_fitness for i in self.individuals]

    def get_fittest(self):
        '''Get the individual with higher `fitness` score'''
        return sorted(self.individuals, key=lambda c: c.fitness, reverse=True)[0]

    def evolve(self):
        '''Create a new generation of individuals through elitism, crossover and mutation'''
        new_gen = [] + sorted(self.individuals, key=lambda c: c.fitness, reverse=True)[:ELITE_NUM]
        while len(new_gen) < POP_SIZE:
            parent1, parent2 = self.selection()
            child = parent1.crossover(parent2)
            child.mutate()
            new_gen.append(child)

        self.individuals = new_gen
        self.calc_stats()
        self.generation += 1

    def selection(self):
        '''Select 2 individuals through Tournament Selection'''
        candidates = sorted(choice(self.individuals, 20, replace=False).tolist(), key=lambda c: c.fitness, reverse=True)
        return candidates[0], candidates[1]

    def solve(self):
        '''Continuously evolve the population until a solution (`fitness = 1`) is found'''
        max_fitness_age = 0
        current_max = self.max_fitness

        while(self.max_fitness < 1):
            if max_fitness_age == 1000:
                # local maximum safe net: re-initialiaze population if stuck for too many iterations
                self.initialize()
            self.evolve()
            if self.max_fitness > current_max:
                current_max = self.max_fitness
                max_fitness_age = 0
            else:
                max_fitness_age += 1
            print(self)
        
        return ''.join(self.get_fittest().genes.flatten().astype(str).tolist())

    def __str__(self):
        return 'Gen {}: avg {:.4f}, max {:.4f}'.format(self.generation, self.avg_fitness, self.max_fitness)


if __name__ == '__main__':
    # The program defaults to the measurament of the assignment example

    p = Population(TEST_CASE)
    time_start = time.monotonic_ns()
    print(p)
    p.solve()
    time_elapsed = time.monotonic_ns() - time_start
    
    print('Found solution:')
    solution = p.get_fittest().genes
    print(solution)

    print(f'Elapsed time : {time_elapsed/1000000000:.5f} s')
