from deap import base, creator, tools, algorithms
import random, numpy as np, time

class GeneticSolver:

    def __init__(self, color_areas: list[list[int]], nr_of_queens: int, pop_size: int = 500, mutate_proba: float = 0.4,
                 crossover_proba: float = 0.9, generations: int = 100, area_version: bool = True, use_elitism: bool = True, hof: int = 1):

        self.seed = int(str(time.time()).replace(".", "")[8:])
        # self.seed = 42
        random.seed(self.seed)
        np.random.seed(self.seed)

        self.board = color_areas
        self.n_queens = nr_of_queens
        self.pop_size = pop_size
        self.mutate_proba = mutate_proba
        self.generations = generations
        self.crossover_proba = crossover_proba
        self.use_elitism = use_elitism
        self.area_version = area_version
        self.hof = hof
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()
        self.toolbox.register("randomQueens", random.sample, range(self.n_queens), self.n_queens)
        self.toolbox.register("individualCreator", tools.initIterate, creator.Individual, self.toolbox.randomQueens)
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)
        self.toolbox.register("evaluate", self.__eval)
        self.toolbox.register("select", tools.selTournament, tournsize=2)
        self.toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0 / self.n_queens)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / self.n_queens)

    def __eval(self, individual):
        fitness = 0
        # Controllo diagonali. Un elemento è sulla tessa diagonale se |r1 - r2| == |c1 - c2|
        # Per costruzione non serve controllare le righe e le colonne
        # (r, q) è la posizione di una regina
        for row_q1, col_q1 in enumerate(individual):
            for row_q2, col_q2 in enumerate(individual):
                if row_q1 != row_q2 and col_q1 != col_q2:
                    if abs(row_q1 - row_q2) == abs(col_q1 - col_q2):
                        fitness += 1
        if self.area_version:
            areas = []
            # Controllo aree
            for row, col in enumerate(individual):
                board_color = self.board[row][col]
                if board_color in areas:
                    fitness += 1
                else:
                    areas.append(board_color)
        return fitness,

    def __convert_to_matrix(self, individual):
        n = len(individual)
        matrix = []
        for row in range(n):
            matrix_row = [0] * n
            column = individual[row]
            matrix_row[column] = 1
            matrix.append(matrix_row)
        return matrix

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
        stats.register("min", np.min)
        stats.register("avg", np.mean)
        stats.register("max", np.max)
        if self.use_elitism:
            self.__eaSimpleWithElitism(population=population, toolbox=self.toolbox,
                                       cxpb=self.crossover_proba, mutpb=self.mutate_proba,
                                       ngen=self.generations, stats=stats, halloffame=hof, verbose=True)
        else:
            algorithms.eaSimple(population=population, toolbox=self.toolbox, cxpb=self.crossover_proba,
                                mutpb=self.mutate_proba, ngen=self.generations, stats=stats,
                                halloffame=hof, verbose=True)
        best = hof.items[0]
        fitness = best.fitness.values[0]
        could_solve = False
        if fitness == 0:
            could_solve = True
        print("Seed = ", self.seed)
        print("Best individual ", best)
        print("Best fitness ", fitness)
        best = self.__convert_to_matrix(individual=list(best))
        print("-- Board --")
        for row in best:
            print(row)
        return could_solve, best