# coding=utf-8


class Rational:

    def __init__(self, numerator, denominator=1):
        div = self.mcd(numerator, denominator)
        self.numerator = numerator // div
        self.denominator = denominator // div

    def mcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def __add__(self, rational):
        a = self.numerator * rational.denominator
        b = rational.numerator * self.denominator
        denominator = self.denominator * rational.denominator
        return Rational(a + b, denominator)

    def __sub__(self, rational):
        return self.__add__(rational * Rational(-1))

    def __mul__(self, rational):
        num = self.numerator * rational.numerator
        den = self.denominator * rational.denominator
        return Rational(num, den)

    def __truediv__(self, rational):
        num = self.numerator * rational.denominator
        den = rational.numerator * self.denominator
        return Rational(num, den)

    def __gt__(self, rational):
        return (self.numerator / self.denominator >
                rational.numerator / rational.denominator)

    def __ge__(self, rational):
        return (self.numerator / self.denominator >=
                rational.numerator / rational.denominator)

    def __lt__(self, rational):
        return (self.numerator / self.denominator <
                rational.numerator / rational.denominator)

    def __le__(self, rational):
        return (self.numerator / self.denominator <=
                rational.numerator / rational.denominator)

    def __eq__(self, rational):
        return (self.numerator == rational.numerator and
                self.denominator == rational.denominator)

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return ('%d/%d' % (self.numerator, self.denominator))

    def __repr__(self):
        if self.denominator == 1:
            return 'Rational(%d)' % self.numerator
        return ('Rational(%d/%d)' % (self.numerator, self.denominator))


if __name__ == "__main__":
    r1 = Rational(26, 4)
    r2 = Rational(-2, 6)
    r3 = Rational(34, 7)

    # 13/2 -1/3 34/7
    print(r1, r2, r3, sep=", ")

    # [Rational(1), Rational(-11/2)]
    print([Rational(1, 1), Rational(22, -4)])

    # 41/6
    print(r1 - r2)

    # 221/7
    print(r1 * r3)

    # 7/5
    print(r2 / Rational(5, -7))

    # True
    print(Rational(-4, 6) < Rational(1, -7))

    # True
    print(Rational(12, 8) == Rational(-24, -16))
