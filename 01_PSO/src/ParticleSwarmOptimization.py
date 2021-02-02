from typing import Callable, List
import Constants as Const
from Swarm import Swarm

import numpy as np


class PSO:
    def __init__(self, function: Callable[[np.ndarray], float]):
        self.team = Swarm(Const.N_PARTICLES)  # Object that holds every particle and shares info
        self.environment: Callable[[np.ndarray], float] = function  # Function used for which the min has to be found
        self.best_history: List[float] = []
        self.average_history: List[float] = []

    def optimize(self):
        for i in range(Const.N_ITERATIONS):
            self.average_history.append(self.team.update(self.environment))
            self.best_history.append(self.team.altitude_history[-1])
