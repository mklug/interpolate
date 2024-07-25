from collections.abc import Sequence


class NewtonInterpolator(Sequence):
    '''Newton interpolator.

    Given a list of tuples of floats [(x0,y0),...,(xn,yn)]
    with the xi distinct this class can be called on 
    other values x to find the value of the unique degree n
    polynomial through these points at x.    

    Initialization take O(n^2) time and O(n) space as the divided
    differences are computed row by row in order to facilitate 
    stable computation of the coefficients of the Newton form of 
    the interpolating polynomial.

    Evaluation at a point x takes time O(n).  Appending a new 
    point takes time O(n) as the new final row of divided differences 
    must be updated.  

    Attributes:
        xs (list(float))            : x values of the input.
        ys (list(float))            : y values of the input.
        _coef (list(float))         : Coeficients of polynomial
                                      in Newton form.
        _divided_diff (list(float)) : Last row of divided differences.
    '''

    def __init__(self, points):
        N = len(points)
        if N < 2:
            raise Exception("Need at least two points.")
        self.xs = [float(x) for x, _ in points]
        if len(self.xs) != len(set(self.xs)):
            raise ValueError("x values must all be distinct.")
        self.ys = [float(y) for _, y in points]

        # Divided differences - build up row by row.
        self._coef = []
        prev_row = []

        # Want both the bottom row and the ends of each row.
        for i in range(N):
            new_row = [self.ys[i]]
            for j, prev in enumerate(prev_row):
                new_row.append(
                    (prev-new_row[-1]) / (self.xs[i-1-j]-self.xs[i]))
            self._coef.append(new_row[-1])
            prev_row = new_row

        # Keep the last row of the divided differences
        # for fast addition of new points.
        self._divided_diff = new_row

    def append(self, point):
        if (type(point) != tuple or
                len(point) != 2):
            raise TypeError("Value must be a tuple of two floats.")
        x_new, y_new = float(point[0]), float(point[1])
        if x_new in self.xs:
            raise Exception("Cannot enter two points with the same x value.")

        # ``i`` in the initialization divided difference code.
        index = len(self.xs)

        self.xs.append(x_new)
        self.ys.append(y_new)

        prev_row = self._divided_diff
        self._divided_diff = [self.ys[index]]
        for j, prev in enumerate(prev_row):
            self._divided_diff.append(
                (prev-self._divided_diff[-1]) / (self.xs[index-1-j]-self.xs[index]))
        self._coef.append(self._divided_diff[-1])

    def __call__(self, x):
        y = self._coef[-1]
        N = len(self.xs)
        for i in range(N-2, -1, -1):
            y = y * (x - self.xs[i]) + self._coef[i]
        return y

    def __getitem__(self, index):
        N = len(self.xs)
        if index < 0 or index >= N:
            raise IndexError("Index not in range.")
        return (self.xs[index], self.ys[index])

    def __len__(self):
        return len(self.xs)
