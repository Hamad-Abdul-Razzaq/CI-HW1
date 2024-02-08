from EA import *

class TSP(EA):
    def __init__(self, iterations, populations, p_size, off_size, mutation_rate) -> None:
        super().__init__(iterations, populations, p_size, off_size, mutation_rate)