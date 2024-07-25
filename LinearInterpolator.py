from MutableSetInterpolator import MutableSetInterpolator
import bisect


class LinearInterpolator(MutableSetInterpolator):
    '''Linear interpolator.

    Given a list of tuples of floats [(x0,y0),...,(xn,yn)]
    with the xi distinct this class can be called on 
    other values x to find the value of the linear
    interpolation of these points at x.  If x is smaller
    than the minimum xi, the corresponding yi is returned
    and similarly if x is larger than the largest xi.  

    Initialization take O(n log(n)) time and O(n) space.
    Evaluation at a point x takes time O(log(n)) and constant 
    space. An error is thrown if the user attempts provides 
    input that would have n < 2, or have two entries with 
    the same x value. 

    Attributes:
        xs (list(float)): x values of the input.
        ys (list(float)): y values of the input.
    '''

    def __init__(self, points):
        zipped = sorted(points, key=lambda z: z[0])
        xs = [float(x) for x, _ in zipped]
        ys = [float(y) for _, y in zipped]
        super().__init__(xs, ys)

    def __call__(self, x):
        N = len(self.xs)
        L = bisect.bisect_left(self.xs, x) - 1
        if L == -1:
            return self.ys[0]
        elif L == N-1:
            return self.ys[-1]

        R = L + 1
        # y = ax + b
        a = (self.ys[L] - self.ys[R]) / (self.xs[L] - self.xs[R])
        b = self.ys[L] - a*self.xs[L]
        return a*x + b

    def discard(self, x):
        x = float(x)
        if x in self.xs:
            N = len(self.xs)
            if N <= 1:
                raise Exception("Need at least one point.")
            index = self.xs.index(x)
            del self.xs[index]
            del self.ys[index]

    def add(self, point):
        if (type(point) != tuple or
                len(point) != 2):
            raise TypeError("Value must be a tuple of three floats.")
        x_new, y_new = float(point[0]), float(point[1])
        if x_new in self.xs:
            raise Exception("Cannot enter two points with the same x value.")

        xnew, ynew = float(point[0]), float(point[1])
        index = bisect.bisect(self.xs, x_new)
        bisect.insort(self.xs, xnew)  # xs maintains order.
        self.ys.insert(index, ynew)
