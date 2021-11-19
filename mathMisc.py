from typing import List, Tuple, Dict

from modifiableSystems import Singleton
from nullObj import null


class InfiniteRange:
    def __init__(self, start: int = 0):
        self.i = start - 1

    def __iter__(self):
        return self

    def __next__(self):
        self.i += 1
        return self.i


class PrimeNumberGenerator(Singleton):
    __instance__ = null

    def __init__(self):
        self._pos = 0
        self._cache = []
        self._iterator = InfiniteRange(2)
        self._lastN = 1

    @property
    def cache(self) -> List[int]:
        return self._cache.copy()

    @cache.deleter
    def cache(self):
        self._cache.clear()

    def __getitem__(self, item):
        while self._pos <= item:
            self._lastN = next(self._iterator)
            if self._isPrime(self._lastN):
                self._cache.append(self._lastN)
                self._pos += 1
        return self._cache[item]

    def isPrime(self, number: int):
        while number > self._lastN:
            self.__getitem__(self._pos)
        return number in self._cache

    @staticmethod
    def _isPrime(number: int):
        if number == 1:
            return False
        i = 2
        while i * i <= number:
            if number % i == 0:
                return False
            i += 1
        return True


class ExponentSplitter(Singleton):
    def __init__(self):
        self.png = PrimeNumberGenerator()
        self._cache = {}

    @property
    def cache(self) -> Dict[int,
                            Tuple[int, int]]:
        return self._cache.copy()

    @cache.deleter
    def cache(self):
        self._cache.clear()

    def splitInExponents(self, number: int):
        x: List[int] = []
        while number != 1:
            if number in self._cache:
                x.append(self._cache[number][0])
                number = self._cache[number][1]
            else:
                i = 0
                while True:
                    if (number % self.png[i]) == 0:
                        self._cache[number] = (self.png[i], number // self.png[i])
                        x.append(self.png[i])
                        number //= self.png[i]
                        break
                    else:
                        i += 1
        return x
