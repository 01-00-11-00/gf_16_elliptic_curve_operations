# ---------------------------- Classes ------------------------------- #

class GF16Operations:

    # Constructor
    def __init__(self):
        self.minimal_polynomial = 0b10011

    # Methods
    @staticmethod
    def get_degree(a) -> int:
        """
        Get the degree of a given polynomial.
        :param a: The polynomial to get the degree of.
        :return: The degree of the polynomial.
        """

        return a.bit_length() - 1

    @staticmethod
    def add(a: int, b: int) -> int:
        """
        Add two numbers in GF(2^4).
        :param a: The first number.
        :param b: The second number.
        :return: The result of the addition.
        """

        return a ^ b

    def multiply(self, a: int, b: int) -> int:
        """
        Multiply two numbers in GF(2^4).
        :param a: The first number.
        :param b: The second number.
        :return: The result of the multiplication.
        """

        result = 0

        while b:
            if b & 1:
                result ^= a

            a <<= 1

            if a & 0x10:
                a ^= self.minimal_polynomial

            b >>= 1

        return result & 0xf

    def divide(self, a: int, b: int) -> int:
        """
        Divide two numbers in GF(2^4).
        :param a: The first number.
        :param b: The second number.
        :return: The result of the division.
        """

        return self.multiply(a, self.invert(b))

    def modular_reduction(self, a: int) -> int:
        """
        Perform a modular reduction of a number in GF(2^4).
        :param a: The number to be reduced.
        :return: The result of the reduction.
        """

        while a >= 16:
            a ^= self.minimal_polynomial << (a.bit_length() - 5)

        return a

    def invert(self, a) -> int:
        """
        Invert a number in GF(2^4).
        :param a: The number to be inverted.
        :return: The inverse of the number.
        """

        min_pol = self.minimal_polynomial
        coefficient_1 = 1
        coefficient_2 = 0
        difference = self.get_degree(a) - 4

        while a != 1:
            if difference < 0:
                a, min_pol = min_pol, a
                coefficient_1, coefficient_2 = coefficient_2, coefficient_1
                difference = -difference

            a ^= min_pol << difference
            coefficient_1 ^= coefficient_2 << difference

            a %= 16
            coefficient_1 %= 16

            difference = self.get_degree(a) - self.get_degree(min_pol)

        return coefficient_1


class GF16EllipticCurveOperations:

    # Constructor
    def __init__(self, a: int):
        self.a = a
        self.calculator = GF16Operations()

    # Methods
    def add(self, p1: tuple, p2: tuple) -> tuple:
        """
        Add two points on the elliptic curve.
        :param p1: The first point.
        :param p2: The second point.
        :return: The result of the addition.
        """

        r1, s1 = p1
        r2, s2 = p2

        if p1 == (0, 0):
            return p2

        elif p2 == (0, 0):
            return p1

        elif p1 == self.invert(p2):
            return 0, 0

        elif p2 == self.invert(p1):
            return 0, 0

        elif p1 == p2:

            m = self.calculator.add(r1, self.calculator.divide(s1, r1))
            m_square = self.calculator.multiply(m, m)

            u = self.calculator.add(m_square, m)
            u = self.calculator.add(u, self.a)

            a = self.calculator.multiply(m, r1)
            b = self.calculator.multiply(m, u)
            v = self.calculator.add(a, b)
            v = self.calculator.add(v, u)
            v = self.calculator.add(v, s1)

            return u, v

        else:

            s = self.calculator.add(s2, s1)
            r = self.calculator.add(r2, r1)

            m = self.calculator.divide(s, r)
            m_square = self.calculator.multiply(m, m)

            u = self.calculator.add(m_square, m)
            u = self.calculator.add(u, self.a)
            u = self.calculator.add(u, r1)
            u = self.calculator.add(u, r2)

            v = self.calculator.add(u, r1)
            v = self.calculator.multiply(m, v)
            v = self.calculator.add(v, u)
            v = self.calculator.add(v, s1)

            return u, v

    def multiply(self, p: tuple[int, int], c: int) -> tuple[int, int]:
        """
        Multiplies a point on the elliptic curve by a scalar.
        :param p: The point to multiply.
        :param c: The coefficient to multiply the point by.
        :return: The result of multiplying the point by the scalar.
        """

        bin_c = bin(c)[3:]
        result = p

        for bit in bin_c:
            result = self.add(result, result)

            if bit == "1":
                result = self.add(result, p)

        return result

    def invert(self, p: tuple) -> tuple:
        """
        Get the inverse of a point on the elliptic curve.
        :param p: The point.
        :return: The inverse of the point.
        """

        u = p[0]
        v = self.calculator.add(p[0], p[1])

        return u, v

    def get_order(self, p: tuple) -> int:
        """
        Get the order of a point on the elliptic curve.
        :param p: The point.
        :return: The order of the point.
        """

        order = 1
        result = p

        while result != (0, 0):
            result = self.add(result, p)
            order += 1

        return order

