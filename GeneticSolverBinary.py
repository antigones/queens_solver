from deap import base, creator, tools, algorithms
import random, numpy as np, time

seed = int(str(time.time()).replace(".", "")[8:])
seed = 96085098
random.seed(seed)
np.random.seed(seed)


class GeneticSolver:

    def __init__(self, color_areas: list[list[int]], nr_of_queens: int, pop_size: int = 50, mutate_proba: float = 0.8,
                 gene_mutate_proba: float = 0.3, crossover_proba: float = 0.99, generations: int = 1000, area_version: bool = True,
                 use_elitism: bool = True, hof: int = 5):
        self.board = color_areas
        self.n_queens = nr_of_queens
        self.pop_size = pop_size
        self.gene_mutate_proba = gene_mutate_proba
        self.mutate_proba = mutate_proba
        self.generations = generations
        self.crossover_proba = crossover_proba
        self.use_elitism = use_elitism
        self.area_version = area_version
        self.hof = hof
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.__create_individual)
        self.toolbox.register("evaluate", self.__eval)
        self.toolbox.register("mate", self.__cxTwoPointCustom)
        self.toolbox.register("mutate", self.__flipBitCustom, indpb=1/self.n_queens)
        self.toolbox.register("select", tools.selTournament, tournsize=3)


    def __find_ones(self, board):
        return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == 1]

    def __find_diagonals(self, board):
        n = len(board)
        m = len(board[0])
        one_pos = self.__find_ones(board)
        diags, anti_diags = [], []
        for pos in one_pos:
            diag = []
            anti_diag = []
            i, j = pos[0], pos[1]
            while i > 0 and j > 0:
                i -= 1
                j -= 1
            while i < n and j < m:
                diag.append((i, j))
                i += 1
                j += 1
            i, j = pos[0], pos[1]
            while i > 0 and j < m - 1:
                i -= 1
                j += 1
            while i < n and j >= 0:
                anti_diag.append((i, j))
                i += 1
                j -= 1
            if len(diag) > 1:
                diags.append(diag)
            if len(anti_diag) > 1:
                anti_diags.append(anti_diag)
        return diags, anti_diags, one_pos

    def __cxTwoPointCustom(self, ind1, ind2):
        size = min(len(ind1), len(ind2))
        i1 = self.__convert_to_matrix(individual=ind1)
        i2 = self.__convert_to_matrix(individual=ind2)
        cxpoint1, cxpoint2 = None, None
        while cxpoint1 == cxpoint2:
            cxpoint1 = random.randint(0, size - 1)
            cxpoint2 = random.randint(0, size - 1)
        i1 = i1[:cxpoint1] + i2[cxpoint1:cxpoint2] + i1[cxpoint2:]
        i2 = i2[:cxpoint1] + i1[cxpoint1:cxpoint2] + i2[cxpoint2:]
        i1 = self.__convert_to_list(individual=i1)
        i2 = self.__convert_to_list(individual=i2)
        ind1[:] = i1
        ind2[:] = i2
        return ind1, ind2

    def __cxOnePointCustom(self, ind1, ind2):
        size = min(len(ind1), len(ind2))
        i1 = self.__convert_to_matrix(individual=ind1)
        i2 = self.__convert_to_matrix(individual=ind2)
        cxpoint = random.randint(0, size - 1)
        i1 = i1[:cxpoint] + i2[cxpoint:]
        i2 = i2[:cxpoint] + i1[cxpoint:]
        i1 = self.__convert_to_list(individual=i1)
        i2 = self.__convert_to_list(individual=i2)
        ind1[:] = i1
        ind2[:] = i2
        return ind1, ind2

    def __flipRowCustom(self, individual, indpb):
        ind = self.__convert_to_matrix(individual=individual)
        for i in range(len(ind)):
            idx1, idx2 = None, None
            while idx1 == idx2:
                idx1 = random.randint(0, len(ind) - 1)
                idx2 = random.randint(0, len(ind) - 1)
            if random.random() < indpb:
                ind[idx1], ind[idx2] = ind[idx2], ind[idx1]
        ind = self.__convert_to_list(individual=ind)
        individual[:] = ind
        return individual,

    def __transponseMutation(self, individual, indpb):
        if random.random() < indpb:
            ind = self.__convert_to_matrix(individual=individual)
            ind = [[ind[j][i] for j in range(len(ind))] for i in range(len(ind))]
            ind = self.__convert_to_list(individual=ind)
            individual[:] = ind
        return individual,

    def __flipBitCustom(self, individual, indpb):
        ind = self.__convert_to_matrix(individual=individual)
        for row in ind:
            if random.random() < indpb:
                rnd_idx = random.randint(0, len(row) - 1)
                for i in range(len(row)):
                    row[i] = 1 if i == rnd_idx else 0
        ind = self.__convert_to_list(individual=ind)
        individual[:] = ind
        return individual,


    def __eval(self, individual):
        nb_of_1s = individual.count(1)
        if nb_of_1s != self.n_queens:
            fitness = 10**5
        else:
            assigned_area = []
            board = self.__convert_to_matrix(individual=individual)
            fitness = 1
            diags, anti_diags, ones_pos = self.__find_diagonals(board)
            diag_to_check = []
            if len(diags) > 0:
                for d in diags:
                    diag_to_check.append([board[pos[0]][pos[1]] for pos in d])
            if len(anti_diags) > 0:
                for d in anti_diags:
                    diag_to_check.append([board[pos[0]][pos[1]] for pos in d])
            cols = [sum(col) for col in zip(*board)]
            rows = [sum(row) for row in board]
            diags = [sum(d) for d in diag_to_check]
            # Check col queens
            for c in cols:
                if c > 1:
                    fitness = fitness * c
            # Check row queens
            for r in rows:
                if r > 1:
                    fitness = fitness * r
            # Check diag queens
            for d in diags:
                if d > 1:
                    fitness = fitness * d
            # Check Area
            if self.area_version:
                same_area = 2
                for pos in ones_pos:
                    color = self.board[pos[0]][pos[1]]
                    if color in assigned_area:
                        same_area += 1
                    else:
                        assigned_area.append(color)
                same_area -= 1
                fitness = fitness * same_area
            fitness -= 1
        return -fitness,

    def __convert_to_matrix(self, individual: list) -> list:
        return [individual[i:i + self.n_queens] for i in range(0, len(individual), self.n_queens)]

    def __convert_to_list(self, individual: list) -> list:
        return [num for row in individual for num in row]

    def __create_individual(self) -> list:
        individual = []
        for _ in range(self.n_queens):
            partial_ind = [0] * self.n_queens
            rnd_idx = random.randint(0, self.n_queens - 1)
            partial_ind[rnd_idx] = 1
            individual += partial_ind
        individual = creator.Individual(individual)
        return individual


    # Due to neat does not implement elitistm, i used the custom function from this repo:
    # https://github.com/PacktPublishing/Hands-On-Genetic-Algorithms-with-Python/blob/master/Chapter05/elitism.py
    def __eaSimpleWithElitism(self, population, toolbox, cxpb, mutpb, ngen, stats=None,
                              halloffame=None, verbose=__debug__):
        """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
        halloffame is used to implement an elitism mechanism. The individuals contained in the
        halloffame are directly injected into the next generation and are not subject to the
        genetic operators of selection, crossover and mutation.
        """
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if halloffame is None:
            raise ValueError("halloffame parameter must not be empty!")

        halloffame.update(population)
        hof_size = len(halloffame.items) if halloffame.items else 0

        record = stats.compile(population) if stats else {}
        logbook.record(gen=0, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        # Begin the generational process
        for gen in range(1, ngen + 1):

            # Select the next generation individuals
            offspring = toolbox.select(population, len(population) - hof_size)

            # Vary the pool of individuals
            offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # add the best back to population:
            offspring.extend(halloffame.items)

            # Update the hall of fame with the generated individuals
            halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            if verbose:
                print(logbook.stream)

        return population, logbook



    def solve(self) -> (bool, list[list[int]]):
        hof = tools.HallOfFame(self.hof)
        population = self.toolbox.populationCreator(n=self.pop_size)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", np.max)
        stats.register("avg", np.mean)
        if self.use_elitism:
            self.__eaSimpleWithElitism(population=population, toolbox=self.toolbox,
                                       cxpb=self.crossover_proba, mutpb=self.mutate_proba,
                                       ngen=self.generations, stats=stats, halloffame=hof, verbose=True)
        else:
            algorithms.eaSimple(population, self.toolbox, cxpb=self.crossover_proba,
                                mutpb=self.mutate_proba, ngen=self.generations, stats=stats,
                                halloffame=hof, verbose=True)
        best = hof.items[0]
        fitness = best.fitness.values[0]
        could_solve = False
        if fitness == 0:
            could_solve = True
        print("Seed = ", seed)
        print("Best individual ever ", best)
        print("Best fitness ever ", fitness)
        best = self.__convert_to_matrix(individual=best)
        print("-- Board = ", best)
        return could_solve, best


