from random import Random


class ExtendedRandom(Random):
    """
    Extends `Random` class with some useful methods
    """
    def bounded_int_gaussian(self, a: int, b: int, mu: float, sigma: float) -> int:
        """
        Return a random integer with Gaussian distribution, bounded
        :param a: lower bound (minimum)
        :param b: upper bound (maximum)
        :param mu: mean
        :param sigma: standard deviation
        """
        return round(min(max(self.gauss(mu, sigma), a), b))
