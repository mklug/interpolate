# interpolate

This repository contains implementations of the following interpolators:
- Linear 
- Piecewise Hermite cubic
- Lagrange
- Newton

Details can be found in the relevant files.

The evaluation time of both the linear and piecewise Hermite cubic could be sped up considerably (with a cost of a slightly more expensive intialization that would not dominate the initialization time complexity) by computing and caching the coefficients of the polynomials for the different intervals.  I did not worry about that and instead optimized for readability in that respect.  
