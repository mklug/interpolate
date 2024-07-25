from collections.abc import MutableSequence


def prod(nums):
    res = 1.0
    for x in nums:
        res *= x
    return res


class LagrangeInterpolator(MutableSequence):
    '''Lagrange polynomial interpolator (barycentric form).

    Given a list of tuples of floats [(x0,y0),...,(xn,yn)]
    with the xi distinct this class can be called on 
    other values x to find the value p(x) where p is the 
    unique polynomial of degree at most n with p(xi) = yi
    for all 0 <= i <= n.

    Initialization take O(n^2) time and O(n) space.
    Evaluation at a point x takes time O(n) and constant space
    as do the other updating operations.  An error is thrown
    if the user attempts provides input that would have n < 2,
    or have two entries with the same x value. 

    Attributes:
        xs (list(float)): x values of the input.
        ys (list(float)): y values of the input.
        ws (list(float)): Barycentric weights computed from 
                          the x-values.
    '''

    def __init__(self, points):
        if len(points) < 2:
            raise Exception("Need at least two points.")

        self.xs = [float(x) for x, _ in points]
        if len(self.xs) != len(set(self.xs)):
            raise ValueError("x values must all be distinct.")

        self.ys = [float(y) for _, y in points]
        self.ws = [prod([xi - xj for j, xj in enumerate(self.xs)
                         if j != i])**-1
                   for i, xi, in enumerate(self.xs)]

    def __call__(self, x):
        # try/catch needed to avoid division by zero.
        try:
            index = self.xs.index(x)
            return self.ys[index]
        except ValueError:
            phi_x = prod([x - xi for xi in self.xs])
            return phi_x * sum((wi / (x-xi)) * yi
                               for wi, xi, yi in zip(self.ws,
                                                     self.xs,
                                                     self.ys))

    def append(self, point):
        if (type(point) != tuple or
                len(point) != 2):
            raise TypeError("Value must be a tuple of two floats.")
        x_new, y_new = float(point[0]), float(point[1])
        if x_new in self.xs:
            raise Exception("Cannot enter two points with the same x value.")

        N = len(self.ws)
        for i in range(N):
            self.ws[i] /= self.xs[i] - x_new

        self.ws.append(prod([x_new - xj
                             for xj in self.xs])**-1)
        self.xs.append(x_new)
        self.ys.append(y_new)

    def __delitem__(self, index):
        N = len(self.xs)
        if N <= 2:
            raise Exception("Need at least two points.")

        x_remove = self.xs[index]

        del self.xs[index]
        del self.ys[index]
        del self.ws[index]

        for i in range(N-1):
            self.ws[i] *= self.xs[i] - x_remove

    def __getitem__(self, index):
        N = len(self.xs)
        if index < 0 or index >= N:
            raise IndexError("Index not in range.")
        return (self.xs[index], self.ys[index])

    def __setitem__(self, index, point):
        N = len(self.xs)
        if index < 0 or index >= N:
            raise IndexError("Index not in range.")
        if not (type(point) == tuple and
                len(point) == 2):
            raise TypeError("Value must be a tuple of two floats.")

        x_new, y_new = float(point[0]), float(point[1])

        if x_new in [xi for i, xi in enumerate(self.xs)
                     if i != index]:
            raise Exception("Cannot enter two points with the same x value.")

        for i in range(N):
            if i == index:
                continue
            self.ws[i] *= self.xs[i] - self.xs[index]
            self.ws[i] /= self.xs[i] - x_new

        self.ws[index] = prod([x_new - xj
                               for j, xj in enumerate(self.xs)
                               if j != index])**-1
        self.xs[index] = x_new
        self.ys[index] = y_new

    def insert(self, index, point):
        N = len(self.xs)
        if index < 0 or index >= N:
            raise IndexError("Index not in range.")

        x_new, y_new = float(point[0]), float(point[1])
        if x_new in self.xs:
            raise Exception("Cannot enter two points with the same x value.")

        for i in range(N):
            self.ws[i] /= self.xs[i] - x_new

        self.ws.insert(index, prod([x_new - xj
                                    for xj in self.xs])**-1)

        self.xs.insert(index, x_new)
        self.ys.insert(index, y_new)

    def __len__(self):
        return len(self.xs)
