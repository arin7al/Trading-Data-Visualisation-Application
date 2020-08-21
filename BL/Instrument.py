import numpy, random


class Instrument:
    def __init__(self, name, variance, drift, startingPrice, price):
        self.data = []
        self.name = name
        self.__variance = variance
        self.__drift = drift

        self.__price = price
        self.__startingPrice = startingPrice
        return

    def calculateNextPrice(self, direction):
        newPriceStarter = self.__price + numpy.random.normal(0, 1) * self.__variance + self.__drift
        newPrice = newPriceStarter if (newPriceStarter > 0) else 0.0
        if self.__price < self.__startingPrice * 0.4:
            self.__drift = (-0.7 * self.__drift)
        self.__price = newPrice * 1.01 if direction == 'B' else newPrice * 0.99
        return self.__price
