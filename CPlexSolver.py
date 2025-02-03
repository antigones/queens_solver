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
            # color_dict.pop(3)
            # color_dict.pop(6)
            for color in color_dict:
                position_per_color = color_dict[color]
                col_vars = [variables[f"x{elem[0]}{elem[1]}"] for elem in position_per_color]
                c = Constraint(sum(col_vars), lb=1, ub=1)
                constraints.append(c)

                # 3: 1 <= x_2_8 + x_3_7 + x_3_8 + x_4_7 <= 1
                # 6: 1 <= x_5_3 + x_5_4 + x_6_4 + x_7_4 + x_8_4 + x_8_5 + x_9_5 <= 1

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

        model.configuration.presolve = False
        # model.configuration.timeout = 600
        model.configuration.verbosity = 3

        try:
            model.optimize()
        except Exception as e:
            print("Errore durante l'ottimizzazione:", str(e))

        status = model.status
        could_solve = False
        if status == 'optimal':
            could_solve = True

        solution = []
        row_solution = []
        raw_sol = {}
        for var_name, var in model.variables.iteritems():
            raw_sol[var_name] = int(var.primal)
        sorted_keys = sorted(raw_sol.keys(), key=lambda x: (int(x.split('_')[1]), int(x.split('_')[2])))
        raw_sol = {k: raw_sol[k] for k in sorted_keys}
        for key in raw_sol:
            row_solution.append(raw_sol[key])
            if key.endswith(f'_{self.nr_of_queens}'):
                solution.append(row_solution)
                row_solution = []

        print("status:", model.status)
        print("objective value:", model.objective.value)
        print("solution: ")
        for elem in solution:
            print(elem)
        print("----------")
        return could_solve, solution, None
