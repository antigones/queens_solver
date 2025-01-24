from optlang import Model, Variable, Constraint, Objective

class CPlexSolver:

    def __init__(self, color_areas: list[list[int]], nr_of_queens: int, area_version: bool = False):
        self.board = color_areas
        self.nr_of_queens = nr_of_queens
        self.area_version = area_version

    def __generate_model(self):
        variables = {}
        for i in range(1, self.nr_of_queens + 1):
            for j in range(1, self.nr_of_queens + 1):
                variables[f"x{i}{j}"] = Variable(f"x{i}{j}", type="binary")

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

        status = model.optimize()

        print("status:", model.status)
        print("objective value:", model.objective.value)
        print("----------")
        for var_name, var in model.variables.iteritems():
            print(var_name, "=", var.primal)
