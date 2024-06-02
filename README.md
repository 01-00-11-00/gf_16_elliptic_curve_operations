# GF 16 Elliptic Curve Operations

This is a Python project that implements operations on elliptic curves over the Galois Field GF(2⁴).

## Getting Started

### Dependencies

- Python 3.x

### Installing

Clone the repository using the following command:

```bash
git clone https://github.com/01-00-11-00/gf_16_elliptic_curve_operations.git
```

## Function Overview

This project contains a class `GF16EllipticCurveOperations` with the following methods:

- `__init__(self, a: int)`: This is the constructor of the class. It initializes the instance with a coefficient `a` for the elliptic curve.

- `add(self, p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]`: This method performs the addition of two points `p` and `q` on the elliptic curve and returns the result.

- `multiply(self, p: tuple[int, int], c: int) -> tuple[int, int]`: This method multiplies a point `p` on the elliptic curve by a scalar `c` and returns the result.

- `invert(self, p: tuple) -> tuple`: This method gets the inverse of a point `p` on the elliptic curve and returns the result.

- `get_order(self, p: tuple) -> int`: This method gets the order of a point `p` on the elliptic curve and returns the result.

Each of these methods is designed to perform a specific operation on elliptic curves over the Galois Field GF(2⁴).

## Authors

01-00-11-00

ex. [@01-00-11-00](https://github.com/01-00-11-00)

## Version History

- 0.1
    - Initial Release