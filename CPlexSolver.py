from optlang.glpk_interface import Model, Variable, Constraint, Objective


class CPlexSolver:

    def __init__(self, color_areas: list[list[int]], nr_of_queens: int, area_version: bool = True):
        self.board = color_areas
        self.nr_of_queens = nr_of_queens
        self.area_version = area_version

    def __generate_model(self):
        variables = {}
        for i in range(1, self.nr_of_queens + 1):
            for j in range(1, self.nr_of_queens + 1):
                variables[f"x{i}{j}"] = Variable(f"x_{i}_{j}", type="binary")

        constraints = []

        # Righe
        for i in range(1, self.nr_of_queens + 1):
            sum_var = []
            for j in range(1, self.nr_of_queens + 1):
                sum_var.append(variables[f"x{i}{j}"])
            c = Constraint(sum(sum_var), lb=1, ub=1)
            constraints.append(c)

        # Colonne
        for j in range(1, self.nr_of_queens + 1):
            sum_var = []
            for i in range(1, self.nr_of_queens + 1):
                sum_var.append(variables[f"x{i}{j}"])
            c = Constraint(sum(sum_var), lb=1, ub=1)
            constraints.append(c)

        # Diagonali
        for d in range(-self.nr_of_queens + 1, self.nr_of_queens):
            diagonal = [variables[f"x{i + 1}{j + 1}"] for i in range(self.nr_of_queens) for j in range(self.nr_of_queens) if i - j == d]
            if diagonal:
                if len(diagonal) == 1:
                    c = Constraint(diagonal[0], lb=0, ub=1)
                else:
                    c = Constraint(sum(diagonal), lb=0, ub=1)
                constraints.append(c)

        # Antidiagonali
        for d in range(1, 2 * self.nr_of_queens):
            diagonal = [variables[f"x{i + 1}{j + 1}"] for i in range(self.nr_of_queens) for j in range(self.nr_of_queens) if i + j + 1 == d]
            if diagonal:
                if len(diagonal) == 1:
                    c = Constraint(diagonal[0], lb=0, ub=1)
                else:
                    c = Constraint(sum(diagonal), lb=0, ub=1)
                constraints.append(c)

        if self.area_version:
            color_dict = {}
            for i, row in enumerate(self.board):
                for j, color in enumerate(row):
                    if color not in color_dict:
                        color_dict[color] = []
                    color_dict[color].append((i + 1, j + 1))

            for color in color_dict:
                position_per_color = color_dict[color]
                col_vars = [variables[f"x{elem[0]}{elem[1]}"] for elem in position_per_color]
                c = Constraint(sum(col_vars), lb=0, ub=1)
                constraints.append(c)

        # objective function
        of_var = []
        for i in range(1, self.nr_of_queens + 1):
            for j in range(1, self.nr_of_queens + 1):
                of_var.append(variables[f"x{i}{j}"])

        obj = Objective(sum(of_var), direction='max')

        model = Model(name=f'{self.nr_of_queens} Queens Model')
        model.objective = obj
        model.add(constraints)

        return model

    def solve(self):
        model = self.__generate_model()

        model.configuration.verbosity = 1
        model.configuration.presolve = False
        model.configuration.timeout = 600

        try:
            model.optimize()
        except Exception as e:
            print("Errore durante l'ottimizzazione:", str(e))

        status = model.status
        could_solve = False
        if status == 'optimal':
            could_solve = True

        solution = []
        row_sol = []
        for var_name, var in model.variables.iteritems():
            row_sol.append(int(var.primal))
            if len(row_sol) % self.nr_of_queens == 0:
                solution.append(row_sol)
                row_sol = []
        print("status:", model.status)
        print("objective value:", model.objective.value)
        print("solution: ")
        for elem in solution:
            print(elem)
        print("----------")
        return could_solve, solution, None
