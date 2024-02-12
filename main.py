from TSP import *
from JSSP import *
from EArt import *


# TSP Run
HyperParameters = {
    'Population Size': 50,
    'Generations': 50000,
    'Iterations': 1,
    'Mutation Rate': 1,
    'OffSpring Size': 10,
    'Parent Procedure': 'Fitness Proportional',
    'Survival Procedure': 'Truncation',
    'Tournament Size': 25,
    'Data Path': 'qa194.tsp'
}

TSP1 = TSP(HyperParameters)
TSP1.Simulate()


# Evolutionary Art Run
HyperParameters = {
    'Population Size': 2,
    'Generations': 10000,
    'Iterations': 1,
    'Mutation Rate': 1,
    'OffSpring Size': 1,
    'Parent Procedure': 'Truncation',
    'Survival Procedure': 'Truncation',
    'Tournament Size': 10,
    'Data Path': 'mona_lisa_v2.png',
    'Polygon Size': 50,
    'Points': 6
}

EArt1 = EArt(HyperParameters)
EArt1.Simulate()


# JSSP Run
HyperParameters = {
    'Population Size': 30,
    'Generations': 50,
    'Iterations': 10,
    'Mutation Rate': 0.95,
    'OffSpring Size': 10,
    'Parent Procedure': 'Truncation',
    'Survival Procedure': 'Truncation',
    'Tournament Size': 10
}
JSSP1 = JSSP(HyperParameters)
JSSP1.Simulate()