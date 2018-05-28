def find_roots(poly):
    # stop recursion if the polynomial is degree 0
    if parse_term(poly[0])[2] == '0': return []

    # by Mean value theorem the roots of a polynomial are in-between the roots of its derivative
    # To find the roots of a function, find the roots of it's derivative and search in-between them
    derivative_roots = find_roots(differentiate(poly))

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


def bisection_estimate(poly, interval, depth=0):
    midpoint = (interval[0] + interval[1])/2

    if abs(evaluate_poly(poly, midpoint)) <= 0.0000000001:  # once estimate is good enough return it
        return midpoint

    # Since we are searching in intervals between the stationary points the function is constantly increasing
    # or decreasing, hence if the sign of the function evaluated at the endpoints doesn't change
    # it is certain there is no root in the interval
    if (evaluate_poly(poly, interval[0]) > 0) == (evaluate_poly(poly, interval[1]) > 0):
        return None
    if depth == 900:  # avoid hitting recursion limit
        return midpoint

    first_half = bisection_estimate(poly, [interval[0], midpoint], depth=depth+1)
    if first_half is not None: return first_half
    else:
        return bisection_estimate(poly, [midpoint, interval[1]], depth=depth+1)


def differentiate(poly):
    result = []
    for term in poly:
        sign, coefficient, power = parse_term(term)
        if power == '0': break

        differentiated_term = sign + str(int(coefficient) * int(power)) + 'x^' + str(int(power) - 1)
        result.append(differentiated_term)

    return result


def evaluate_poly(poly, x):
    result = 0
    for term in poly:
        sign, coefficient, power = parse_term(term)
        result += int(sign+'1')*int(coefficient)*pow(x, int(power))

    return result


def parse_term(term):
    sign = term[0]
    coefficient = term[1:term.index('^')-1]
    power = term[term.index('^')+1:]

    return sign, coefficient, power


def main():
    print('All polynomials must be entered in the form (+/-)ax^n for the program to work')
    print('For example: "+1x^2 -4x^1 +1x^0" is valid whereas "x^2 -4x + 1" is not')
    while True:
        poly = input('Enter a polynomial: ').split(' ')  # polynomial is represented as a list of terms

        print('The roots are: ')
        for root in find_roots(poly):
            print('x = {}'.format(root))


if __name__ == '__main__':
    main()
