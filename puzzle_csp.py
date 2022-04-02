#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = caged_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the FunPuzz puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. caged_csp_model (worth 25/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with FunPuzz cage constraints.

'''
from cspbase import *
import itertools


def binary_ne_grid(fpuzz_grid):
    N = fpuzz_grid[0][0]

    # Creating Variable
    temp = itertools.count(1)
    domain = list(range(1, N + 1))
    variables = [[Variable('{}'.format(next(temp)), domain) for _ in range(N)] for _ in range(N)]

    vars = [var for row in variables for var in row] # Getting all variables

    constraints = []
    sat_tuples = []
    csp = CSP("binary_ne_grid", vars)
    for t in itertools.permutations(domain, 2):
        sat_tuples.append(t)

    for i in range(N):
        row = variables[i]
        col = [variables[j][i] for j in range(N)]
        for tuple in itertools.combinations(row, 2):
            cons = Constraint('C{}{}'.format(tuple[0].name, tuple[1].name), [tuple[0], tuple[1]])
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)
        for tuple in itertools.combinations(col, 2):
            cons = Constraint('C{}{}'.format(tuple[0].name, tuple[1].name), [tuple[0], tuple[1]])
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)
    for cons in constraints:
        csp.add_constraint(cons)

    return csp, variables

def nary_ad_grid(fpuzz_grid):
    #IMPLEMENT
    N = fpuzz_grid[0][0]

    # Creating Variable
    temp = itertools.count(1)
    domain = list(range(1, N + 1))
    variables = [[Variable('{}'.format(next(temp)), domain) for _ in range(N)] for _ in range(N)]
    vars = [var for row in variables for var in row]  # Getting all variables

    constraints = []
    sat_tuples = []
    csp = CSP("nary_ad_grid", vars)
    for t in itertools.permutations(domain, N):
        sat_tuples.append(t)

    for i in range(N):
        row = variables[i]
        col = [variables[j][i] for j in range(N)]
        for _ in itertools.combinations(row, N):
            cons = Constraint('C{}'.format(tuple(row)), row)
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)

            cons = Constraint('C{}'.format(tuple(col)), col)
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)
    for cons in constraints:
        csp.add_constraint(cons)

    return csp, variables

def multiply(lst, target):
    result = 1
    for x in lst:
        result *= x
    return result == target

def add(lst, target):
    result = 0
    for x in lst:
        result += x
    return result == target

def sub(lst, target):
    size = len(lst)
    for t in itertools.product(tuple(lst), repeat=size):
        for i in range(size):
            if t[i] - sum(t[:i] + t[i + 1:]) == target:
                return True

def divide(lst, target):
    size = len(lst)
    for t in itertools.product(tuple(lst), repeat=size):
        for i in range(size):
            result = float(t[i])
            for value1 in t[:i] + t[i + 1:]:
                result /= value1
            if result == target:
                return True


def caged_csp_model(fpuzz_grid):
    #IMPLEMENT
    N = fpuzz_grid[0][0]

    # Creating Variable
    temp = itertools.count(1)
    temp_cage = itertools.count(1)
    domain = list(range(1, N + 1))
    variables = [[Variable('{}'.format(next(temp)), domain) for _ in range(N)] for _ in range(N)]

    # Creating Constraints
    constraints = []
    # Cage Constraints
    for cage in fpuzz_grid[1:]:
        # While cage only have two elements
        # 1st cell is the value and 2nd cell is the target number
        if (len(cage)) == 2:
            scope = []
            i = (cage[0] // 10) - 1
            j = (cage[0] % 10) - 1
            target = cage[1]
            variables[i][j] = Variable("%d%d" % (i, j), [target])
            scope.append(variables[i][j])
            cons = Constraint("cage{}".format(next(temp_cage)), scope)
            cons.add_satisfying_tuples([(target, )])
            constraints.append(cons)

        else:
            op = cage[-1]
            target = cage[-2]
            varDoms = []
            scope = []
            sat_tuple = []
            for index in range(len(cage) - 2):
                i = (cage[index] // 10) - 1
                j = (cage[index] % 10) - 1
                scope.append(variables[i][j])
                varDoms.append(variables[i][j].domain())

            cons = Constraint("cage{}".format(cage), scope)
            for t in itertools.product(*varDoms):
                match op:
                    case 0:
                        if add(t, target):
                            sat_tuple.append(t)
                    case 1:
                        if sub(t, target):
                            sat_tuple.append(t)
                    case 2:
                        if divide(t, target):
                            sat_tuple.append(t)
                    case 3:
                        if multiply(t, target):
                            sat_tuple.append(t)
                    case _:
                        print("Error: Invalid op num")
                        return
            cons.add_satisfying_tuples(sat_tuple)
            constraints.append(cons)

    # Other constraints (without cage)
    sat_tuple = [t for t in itertools.permutations(domain, 2)]
    # for i in range(N):
    #     row = variables[i]
    #     col = [variables[j][i] for j in range(N)]
    #     for _ in itertools.combinations(row, N):
    #         cons = Constraint('row{}'.format(tuple(row)), row)
    #         cons.add_satisfying_tuples(sat_tuple)
    #         constraints.append(cons)
    #
    #         cons = Constraint('col{}'.format(tuple(col)), col)
    #         cons.add_satisfying_tuples(sat_tuple)
    #         constraints.append(cons)

    # binary_neq_grid
    for i in range(N):
        row = variables[i]
        col = [variables[j][i] for j in range(N)]
        for t in itertools.combinations(row, 2):
            cons = Constraint('row{}{}'.format(t[0].name, t[1].name), [t[0], t[1]])
            cons.add_satisfying_tuples(sat_tuple)
            constraints.append(cons)
        for t in itertools.combinations(col, 2):
            cons = Constraint('col{}{}'.format(t[0].name, t[1].name), [t[0], t[1]])
            cons.add_satisfying_tuples(sat_tuple)
            constraints.append(cons)


    vars = [var for row in variables for var in row]  # Getting all variables

    csp = CSP("caged_csp_model", vars)
    for cons in constraints:
        csp.add_constraint(cons)

    return csp, variables