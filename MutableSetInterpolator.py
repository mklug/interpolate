from collections.abc import MutableSet
import bisect


class MutableSetInterpolator(MutableSet):

    def __init__(self, xs, ys):
        # Must do any sorting of xs before they are passed here.
        N = len(xs)
        if N < 1:
            raise Exception("Need at least one point.")
        self.xs = xs
        self.ys = ys

    def __contains__(self, x):
        return x in self.xs

    def __iter__(self):
        return zip(self.xs, self.ys)

    def __getitem__(self, index):
        N = len(self.xs)
        if index < 0 or index >= N:
            raise IndexError("Index not in range.")
        return (self.xs[index], self.ys[index])

    def __len__(self):
        return len(self.xs)
