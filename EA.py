class EA:
    def __init__(self, iterations, populations, p_size, off_size, mutation_rate) -> None:
        self.iterations = iterations
        self.populations = populations
        self.population_size = p_size
        self.offspring_size = off_size
        self.mutation_rate = mutation_rate


