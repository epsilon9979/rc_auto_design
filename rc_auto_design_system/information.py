import sympy

class information:
    def __init__(self):
        pass
    
    def D(self, number):
        diameter = [0, 0, 0, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.128, 1.27]
        return diameter[number]

    def A(self, number):
        area = [0, 0, 0, 0.11, 0.2, 0.31, 0.44, 0.6, 0.79, 1, 1.27]
        return area[number]

    def type(self, number):
        types = {'non': 0, 'edge': 1, 'middle': 2}
        return types[number]

    def get_c(self, left, right):
        c = sympy.symbols('c')
        equ = sympy.Eq(left, right)
        solutions = sympy.solve(equ, c)
        real_solutions = [sol.evalf() for sol in solutions if sol.is_real]
        return max(real_solutions)
