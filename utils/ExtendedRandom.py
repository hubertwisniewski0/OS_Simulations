from random import Random


class ExtendedRandom(Random):
    def bounded_int_gaussian(self, a: int, b: int, mu: float, sigma: float) -> int:
        return round(min(max(self.gauss(mu, sigma), a), b))
