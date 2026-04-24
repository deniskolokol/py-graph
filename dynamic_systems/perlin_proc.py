import numpy as np
from perlin import PerlinNoiseFactory


dimensions = 3
pnf = PerlinNoiseFactory(dimensions, octaves=5, unbias=True)

step_count = 1000
for i in range(step_count):
    point = [i/1000., .1, .1]
    print("%s," %pnf(*point))
