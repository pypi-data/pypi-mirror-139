import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from simmeth.alternative import Alternative
from simmeth.belief import Belief
from simmeth.strategy import Strategy


class Environment:
    """Class for simulating the environment. The length of the success probabilities
    list (strategy_probs) defines the number of available strategies.

    Params:
      strategy_probs (List[float]): list of success probabilities
      turb (float): the turbulence factor (probability of a change)
      T (int): number of days (i.e. number of times a strategy has to be selected)
      strategies (List[Strategy]): list of strategies to select from
      strategy_history (List[Tuple[Dict]]): stores history of strategies
      results (List[{0,1}]): list of results (length=T) from executing strategies
      switch_times (int): Counter for switching strategy
      name (string): Custom name for environment (can be used to differentiate between envs)
    """

    def __init__(self, name, strategy_probs, T, turb=0, belief=Belief, max_confidence=1, unlearn=False):
        self.strategy_probs = strategy_probs
        self.T = T
        self.t = 0  # counter for current step environment is in
        self.turb = turb
        self.strategies = [Strategy(Alternative(p), belief(max_confidence=max_confidence, unlearn=unlearn)) for p in
                           strategy_probs]
        self.strategy_history = []
        self.results = []
        self.switch_times = 0
        self.name = name

    def track(self, prev_strategy, strategy):
        """Store decision and increase switch counter."""
        self.t += 1
        self.strategy_history.append(tuple(
            {"env_name": self.name,
             "strategy_id": self.strategies.index(s),
             "t": self.t,
             "p": s.alternative.p,
             "conf": s.belief.get_confidence(),
             "mean": s.belief.get_mean_belief(),
             "selected": int(s == strategy),
             "alt_n": s.alternative.n,
             "switch_times": self.switch_times} for s in
            self.strategies))
        if prev_strategy != strategy:
            self.switch_times += 1

    def shock(self):
        """Simulates a turbulence (i.e. updates a random probability by chance)."""
        for s in self.strategies:
            if np.random.random() < self.turb:
                s.alternative.p = np.random.random()
                if s.belief.unlearn:
                    s.belief.a = 1
                    s.belief.b = 1

    def plot(self):
        """Plot beliefs of all strategies."""
        for s in self.strategies:
            s.belief.plot()
            plt.axvline(s.alternative.p, color='k', linestyle='--', linewidth=1, alpha=.3, label='_nolegend_')
        plt.title(f"(turb={self.turb}, switches={self.switch_times})")
        plt.legend(["p={:.2f} (n={} ({:.1f}%), conf={:.2f}, m={:.2f})".format(s.alternative.p, s.alternative.n,
                                                                              (s.alternative.n / self.T) * 100,
                                                                              s.belief.get_confidence(),
                                                                              s.belief.get_mean_belief())
                    for s in
                    self.strategies], loc="upper left")
        plt.show()

    def simulate(self):
        best_strategy = None
        for d in range(self.T):
            prev_strategy = best_strategy
            max_belief = 0

            for s in self.strategies:
                belief = s.belief.evaluate()  # get the belief of strategy s
                if belief > max_belief:
                    max_belief = belief  # keep the highest belief
                    best_strategy = s  # keep the best strategy

            # track decision
            self.track(prev_strategy, best_strategy)

            # execute the strategy with the largest belief (because it is the best strategy)
            x = best_strategy.alternative.execute()
            self.results.append(x)

            # update the distribution for the strategy we just executed
            best_strategy.belief.update(x)

            if self.turb > 0:
                self.shock()

    def get_strategy_df(self):
        df = pd.DataFrame()
        for s in self.strategy_history:
            df = df.append(pd.DataFrame(s))
        return df
