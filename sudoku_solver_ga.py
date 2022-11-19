import numpy as np
from numpy.random import random, choice, permutation

GENES = {1,2,3,4,5,6,7,8,9}
MAX_SCORE = 162
POP_SIZE = 200
MUT_RATE = 0.8
ELITE_NUM = 10
SEL_NUM = 50

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
    def __init__(self, genes, fixed_genes, init = False):
        self.fixed_genes = fixed_genes
        self.genes = genes
        if init: self.fill()
        self.calc_fitness()

    def calc_fitness(self):
        score = 0
        score += sum([np.unique(col).size for col in self.genes.T])
        for r,c in [(0,0),(0,3),(0,6),
                    (3,0),(3,3),(3,6),
                    (6,0),(6,3),(6,6)]:
            score += np.unique(self.genes[r:r+3,c:c+3]).size
        self.fitness = (score / MAX_SCORE) ** 10
    
    def crossover(self, partner):
        new_genes = self.genes.copy()
        from_partner = np.random.randint(1,9)
        new_genes[-from_partner:] = partner.genes[-from_partner:].copy()
        return Individual(new_genes, self.fixed_genes)

    def mutate(self):
        if np.random.random() < MUT_RATE:
            row = np.random.randint(0,9)
            cells = np.random.permutation(np.argwhere(~self.fixed_genes[row]))
            c1, c2 = cells[0], cells[1]
            self.genes[row,c1], self.genes[row,c2] = self.genes[row,c2], self.genes[row,c1]
            self.calc_fitness()

    def fill(self):
        for row in range(9):
            assignable = GENES - set(self.genes[row][self.fixed_genes[row]])
            self.genes[row][~self.fixed_genes[row]] = np.random.permutation(list(assignable))

    def __str__(self):
        return '<Individual fit: {:.4f}, content: [{}] />'.format(self.fitness, ''.join(self.genes.flatten().astype(str)))


class Population:
    def __init__(self, base_genes):
        self.individuals = []
        self.initialize(base_genes)
        self.generation = 1

    def initialize(self, base_genes):
        genes = np.array(list(base_genes), dtype=int).reshape(9,9)
        fixed_genes = genes > 0
        for _ in range(POP_SIZE):
            self.individuals.append(Individual(genes.copy(), fixed_genes, init=True))
        self.calc_stats()

    def calc_stats(self):
        self.max_fitness = max([i.fitness for i in self.individuals])
        self.tot_fitness = sum([i.fitness for i in self.individuals])
        self.avg_fitness = self.tot_fitness / POP_SIZE
        self.probs = [i.fitness / self.tot_fitness for i in self.individuals]

    def evolve(self):
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
        '''Tournament Selection'''
        # candidates = sorted(choice(self.individuals, SEL_NUM, replace=False).tolist(), key=lambda c: c.fitness, reverse=True)
        candidates = np.random.choice(self.individuals, size=2, replace=True, p=self.probs)
        return candidates[0], candidates[1]

    def get_fittest(self):
        return sorted(self.individuals, key=lambda c: c.fitness, reverse=True)[0]

    def __str__(self):
        return 'Gen {}: avg {:.4f}, max {:.4f}'.format(self.generation, self.avg_fitness, self.max_fitness)


if __name__ == '__main__':
    print(TEST_CASE)
    p = Population(TEST_CASE)
    print(p)
    while(True):
        p.evolve()
        print(p)
        print(p.get_fittest())