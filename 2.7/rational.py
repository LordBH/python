# r1 = Rational(3, 4)
# r3 = r1 + Rational(5, 7)
# print str(r3)


class Rational(object):
    def __init__(self, numerator, divider):
        self.numerator = int(numerator)
        self.divider = int(divider)
        if divider == 0:
            raise ZeroDivisionError()

    def __add__(self, arg):
        if isinstance(arg, Rational):
            num, div = self.get_sum(arg)
            return self.__class__(num, div)
        else:
            raise AttributeError()

    def get_sum(self, arg):
        numerators = self.numerator * arg.divider + \
                     arg.numerator * self.divider
        dividers = self.divider * arg.divider

        return numerators, dividers

    def __str__(self):
        return '%r/%r' % (self.numerator, self.divider)


class SuperRational(Rational):
    pass

r1 = Rational(3, 2)
# r3 = r1 + Rational(5, 7)
r3 = SuperRational(5, 7) + r1
print r3.__class__
