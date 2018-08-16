class Term:
    def __init__(self, term="0x^0"):
        self.coef = float(term[:term.index('x')])
        self.power = int(term[term.index('^') + 1:])

    def derivative(self):
        d = Term()
        d.coef = self.coef*self.power
        d.power = self.power - 1
        return d


class Polynomial:
    def __init__(self, polynomial="", terms=None):
        if terms is not None:  # is not None as opposed to just "if terms:" because terms could be an empty list
            self.terms = terms
        else:
            self.terms = [Term(term) for term in polynomial.split(' ')]

        self.f = lambda x: sum([term.coef*pow(x, term.power) for term in self.terms])

    def derivative(self):
        return Polynomial(terms=[term.derivative() for term in self.terms if term.coef != 0 and term.power != 0])


def find_roots(poly: Polynomial):
    # stop recursion if the polynomial is degree 0
    if not poly.terms: return []

    # by Mean value theorem the roots of a polynomial are in-between the roots of its derivative
    # To find the roots of a function, find the roots of it's derivative and search in-between them
    derivative_roots = find_roots(poly.derivative())

    # construct intervals from roots
    if len(derivative_roots) != 0:
        intervals = [[-100000, derivative_roots[0]]]
        for i in range(len(derivative_roots) - 1):
            intervals.append([derivative_roots[i], derivative_roots[i + 1]])
        intervals.append([derivative_roots[-1], 100000])

    else:
        intervals = [[-100000, 100000]]

    # Search for roots in each of the intervals
    roots = []
    for interval in intervals:
        root = bisection_estimate(poly, interval)
        if root is not None: roots.append(root)
    return roots


def bisection_estimate(poly: Polynomial, interval, depth=0):
    midpoint = (interval[0] + interval[1])/2
    if abs(poly.f(midpoint)) <= 0.000000000001:  # once estimate is good enough return it
        return midpoint

    # Since we are searching in intervals between the stationary points the function is constantly increasing
    # or decreasing, hence if the sign of the function evaluated at the endpoints doesn't change
    # there is no root in the interval
    if (poly.f(interval[0]) > 0) == (poly.f(interval[1]) > 0):
        return None
    if depth == 900:  # avoid hitting recursion limit
        return midpoint

    # if the root is not in the first half of the interval it must be in the second
    first_half = bisection_estimate(poly, [interval[0], midpoint], depth+1)
    if first_half is not None:
        return first_half
    else:
        return bisection_estimate(poly, [midpoint, interval[1]], depth+1)


def main():
    print('All polynomials must be entered in the form (+/-)ax^n for the program to work')
    print('For example: "+1x^2 -4x^1 +1x^0" is valid whereas "x^2 -4x + 1" is not')

    while True:
        poly = Polynomial(input('Enter a polynomial: '))
        print('The roots are: ')
        for root in find_roots(poly):
            print('x = {}'.format(root))


if __name__ == '__main__':
    main()
