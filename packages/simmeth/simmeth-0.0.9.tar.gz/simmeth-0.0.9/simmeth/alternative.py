import numpy as np


class Alternative:
    """A class representing a choice in environment.

    Params:
      p (float): True success probability (unknown to the user)
      n (int): Counter for execution times (=how often alternative was executed)
    """

    def __init__(self, p):
        self.p = p
        self.n = 0

    def execute(self):
        """ Execute the alternative and obtain a result {0,1}."""
        self.n += 1
        return np.random.random() < self.p
