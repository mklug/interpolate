from MutableSetInterpolator import MutableSetInterpolator
import bisect


class PiecewiseCubicHermiteInterpolator(MutableSetInterpolator):
    '''Piecewise Cubic Hermite Interpolator.

    Given three equal length lists floats x, f, fprime
    which represent a sequence of points (x,f(x)) together
    with the corresponding values of fprime(x), this 
    class, when called returns the value of the Piecewise
    cubic Hermite spline through these points with the 
    desired derivatives, evaluated at x.  If x is smaller
    than the minimum xi, the corresponding yi is returned
    and similarly if x is larger than the largest xi.  

    Initialization take O(n log(n)) time and O(n) space.
    Evaluation at a point x takes time O(log(n)) and constant 
    space. An error is thrown if the user attempts provides 
    input that would have n < 2, or have two entries with 
    the same x value. 

    Attributes:
        xs (list(float))     : x values of the input.
        ys (list(float))     : f(x) values of the input.
        fprime (list(float)) : fprime(x) values of the input
    '''

    def __init__(self, xs, f, fprime):
        N = len(xs)
        if N < 1:
            raise Exception("Need at least one point.")

        zipped = sorted(zip(xs, f, fprime), key=lambda z: z[0])
        xs = [float(x) for x, _, _ in zipped]
        ys = [float(fx) for _, fx, _ in zipped]
        super().__init__(xs, ys)

        # self.f = [float(fx) for _, fx, _ in zipped]
        self.fprime = [float(fprimex) for _, _, fprimex in zipped]

    def __call__(self, x):
        N = len(self.xs)
        L = bisect.bisect_left(self.xs, x) - 1
        if L == -1:
            return self.ys[0]
        elif L == N-1:
            return self.ys[-1]
        R = L + 1

        # Variables to hopefully make the formula more readable.
        xL = self.xs[L]
        xR = self.xs[R]
        fL = self.ys[L]
        fR = self.ys[R]
        fpL = self.fprime[L]
        fpR = self.fprime[R]

        h = xR - xL
        alpha = (3/(h**2)) * (fpL + fpR) + (6/(h**3)) * (fL - fR)

        return (((-fpL/h) * (((x-xR)**2)/2 - ((h**2)/2))) +
                ((fpR/h) * ((x-xL)**2)/2) +
                (alpha * ((x-xL)**2) * (((x-xL)/3) - (h/2))) +
                fL
                )

    def discard(self, x):
        x = float(x)
        if x in self.xs:
            N = len(self.xs)
            if N <= 1:
                raise Exception("Need at least one point.")
            index = self.xs.index(x)
            del self.xs[index]
            del self.ys[index]
            del self.fprime[index]

    def add(self, point):
        if (type(point) != tuple or
                len(point) != 3):
            raise TypeError("Value must be a tuple of three floats.")
        x_new, y_new, fprime_new = (float(p) for p in point)
        if x_new in self.xs:
            raise Exception("Cannot enter two points with the same x value.")

        xnew, ynew = float(point[0]), float(point[1])
        index = bisect.bisect(self.xs, x_new)
        bisect.insort(self.xs, xnew)
        self.ys.insert(index, ynew)
        self.fprime.insert(index, fprime_new)
