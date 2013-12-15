#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch
#
#
# Question 1.
#
# Implement a binary Genetic Algorithm that uses fitness proportional selection,
# 1-point crossover, and bit-flip mutation to solve the problem in which the
# fitness is the number of 1s in the chromosome, i.e. the optimal solution is
# the chromosome where all genes are set to 1.
#
# A. (40 points) Run the algorithm 10 times for each of the four following
# versions of the problem:
# l = 5, 10, 20, 50, where l is the length of the chromosomes. Vary the
# population size and mutation rate to obtain good results (fast solution).
#
# B. (10 points) Plot the best fitness in each generation (averaged over the 10
# runs), for each of the four problems. There should be one graph with four
# curves, the x-axis being the generations, and the y-axis the average (best)
# fitness.


import random # randrange()


import sys # sys.exit()

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )


class Person(object):
    def __init__(self, chromosome=[], fitness=0, probability=0.0):
        self._chromosome=chromosome
        self._fitness=fitness
        self._probability=probability
    def chromosome(self): return self._chromosome
    def set_chromosome(self,chromosome): self._chromosome=chromosome
    def fitness(self): return self._fitness
    def set_fitness(self,fitness): self._fitness=fitness
    def probability(self): return self._probability
    def set_probability(self, probability): self._probability=probability
    def set_chromatide(self, idx, chromatide): self._chromosome[idx] = chromatide


class Genetic(object):
    def __init__(self,population_size, chromosome_size, mutation_rate):
        self.population_size=population_size
        self.chromosome_size=chromosome_size
        self.mutation_rate=mutation_rate
        self.population=[]
        self.new_population=[]
        self._run=0
        self.optimal=0

    def run(self):
        # 1. initialize random popolation of candidate solutions
        # create random chromosome
        self.population = [Person(chromosome=self.generate_chromosome()) for p in range(self.population_size)]

        while self.optimal==0:
#            print "generation: %d"%(self._run)    
            self.DB_population()     
            print "self.population_siz %d"%len(self.population)  

            # 2. evaluate solutions on problem and assign a fitnes score
            self.evaluate()
            print "self.population_siz %d"%len(self.population)  

            # 3. select some solutions for mating
            self.selection()
            print "self.population_siz %d"%len(self.population)  

            # 4. recombine: create new solutions from selected ones by exchanging structure
            self.recombination()

            # 5. IF good solution not found: GOTO 2
            self.optimal = self.is_done()
            self._run += 1


            if self._run == 1000: die("I give up") ## avoid infinite loops due to bugs
            
        ## only print the number of runs, it took to compute the result
#        self.DB_population()     

        ## // while
        return self._run

    def evaluate(self):
        for idx in range(self.population_size):
            self.population[idx].set_fitness(self.get_fitness(self.population[idx].chromosome()))

    def selection(self):
        ## calculate a genotypes probability of being selected in proportion to its fitness
        for idx in range(self.population_size):
            self.population[idx].set_probability(self.compute_probability(self.population, self.population[idx].fitness()))
        ## prepare new_population by pre-selecting genotypes with highest probability, based on random value
        idx=0; cnt=0 # safety counter
        while idx < self.population_size and cnt < 100: # or, after 100 tries, give up, and take old one...
            # for each position in new_population choose a "likely" individual
            probability = 0.0
            for jdx in range(self.population_size):
                ## get random criteria
                rnd_probability = (1.0*random.randrange(1, self.population_size)) / 10
                ## go through all population items and see by probability if one gots selected,
                ## only increment the counter if we have an item for new_population
                ## if not, go through all again
                probability = self.population[jdx].probability()
                if rnd_probability < probability:
                    ## we found an item
                    self.new_population += [Person(chromosome=self.population[jdx].chromosome())]
                    idx+=1
                    cnt=0
                    break
            cnt+=1

    def recombination(self):
        ## mating
        self.new_population = self.crossover(self.new_population)

        ## mutation
        for idx_p in range(self.population_size):
            rate = random.randrange(0,10) / 10.0
            if rate < self.mutation_rate:
                ## flip a bit on mutation rate
                bit = random.randrange(0,self.chromosome_size)
                self.new_population[idx_p].set_chromatide(bit,(self.new_population[idx_p].chromosome()[bit] + 1) % 2)
            ## // if
        ## // for

    def is_done(self):
        ## doing next generation
        self.population = [Person( chromosome=elem.chromosome()) for elem in self.new_population]
        self.new_population = []
        if 0 != self.is_optimal(self.population):
            return 1
        return 0

    def generate_chromosome(self): # elements of [0;2[
        return [random.randrange(0,2) for i in range(self.chromosome_size)]

    def get_best_fitness(self, population):
        return max([population[i].fitness() for i in range(self.population_size)])/self.chromosome_size

    def get_fitness(self, chromosome):
        return sum(chromosome)

    def compute_probability(self, population, fitness):
        return (1.0 * fitness) / sum([i.fitness() for i in population])

    def get_parents(self):
# TODO this picks just any kind of parents - do we need to keep certain criteria for selection?
        idx_parent_a=None
        idx_parent_b=idx_parent_a
        while idx_parent_a == idx_parent_b:
            idx_parent_a = random.randrange(0, self.population_size)
            idx_parent_b = random.randrange(0, self.population_size)
        return idx_parent_a, idx_parent_b

    def crossover(self, population):
        for idx_p in range(1,self.population_size,2):
            chromosome_a=[]; chromosome_b=[]
            ## 1 point chrossover
            xo_pt=random.randrange(0,self.chromosome_size)
            for idx_c in range(self.chromosome_size):
                print "XXX idx_p %d, population_siz %d, idx_c %d"%(idx_p, len(population), idx_c)   
                print "XXX [idx-1]chromosome_siz %d"%(len(population[idx_p].chromosome()))   
                print "XXX [idx]chromosome_siz %d"%(len(population[idx_p].chromosome()))   
                print "" 
                chromosome_a += [population[idx_p-1 if idx_c < xo_pt else idx_p].chromosome()[idx_c]]
                chromosome_b += [population[idx_p if idx_c < xo_pt else idx_p-1].chromosome()[idx_c]]
            ## init by generated chromosome
            population[idx_p-1].set_chromosome(chromosome_a)
            population[idx_p].set_chromosome(chromosome_b)
        return population

    def is_optimal(self, population):
        total = 0
        for p in population:
            total += sum(p.chromosome())
        if total == self.chromosome_size * self.population_size:
            return 1
        return 0
    
    ## debug, print the chromosomes of all population
    def DB_population(self):
        print "self.population"
        for idx in range(self.population_size):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.population[idx].fitness(), self.population[idx].probability()),
            print '%s'%' '.join(map(str,self.population[idx].chromosome()))
        print "self.new_population"
        for idx in range(len(self.new_population)):
            print "%d. individuum, fitness: '%d', probability: '%f', chromosome: "%(idx, self.new_population[idx].fitness(), self.new_population[idx].probability()),
            print '%s'%' '.join(map(str,self.new_population[idx].chromosome()))

    def print_new_chromosome(self):
        print "Population : Chromosome"
        for idx_pop in self.population_size:
            for idx_chr in self.chromosome_size:
                print "%d\t%d"%(idx_pop, self._new_population[idx_pop].chromosome[idx_chr])
    
    def __str__(self):
        return str(self.run())


                                                                               
## MAIN
if __name__ == '__main__':
    population_size = 10
    chromosome_sizes = [5,10,20,50]
    mutation_rate = 0.2

    for chromosome_size in chromosome_sizes:
#        print chromosome_size
        genetic = Genetic(population_size, 5, mutation_rate)
#        genetic = Genetic(population_size, chromosome_size, mutation_rate)
#        x=genetic.run()
#        print x
#        break
        print genetic,
    print ""

    die("STOP")    

#    print "optimal solution"
#    print "generations: ",genetic.run()
#    print "genes: "


    genetic.print_new_chromosome()


#    population_size = 10
#    chromosome_size = 10
#    mutation_rate = 0.02
# TODO


#    population_size = 10
#    chromosome_size = 20
#    mutation_rate = 0.02
# TODO


#    population_size = 10
#    chromosome_size = 50
#    mutation_rate = 0.02
# TODO


    print "READY."
