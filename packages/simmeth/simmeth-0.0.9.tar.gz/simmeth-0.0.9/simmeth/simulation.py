import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from simmeth.belief import Belief
from simmeth.environment import Environment


class Simulation:
    def __init__(self, scenarios, t: int = 100, n=1000, n_strategies=10):
        self.scenarios = scenarios
        self.t = t
        self.n = n
        self.n_strategies = n_strategies
        self.envs_history: [Environment] = []
        self.results = np.empty([len(self.scenarios), self.n, self.t])

    def run(self):
        for i in range(len(self.scenarios)):
            for j in range(self.n):
                strategy_probabilities = np.sort(np.random.rand(self.n_strategies))
                env = Environment(name=j,
                                  strategy_probs=strategy_probabilities,
                                  T=self.t,
                                  turb=self.scenarios[i]["turb"],
                                  belief=Belief,
                                  max_confidence=self.scenarios[i]["max_confidence"],
                                  unlearn=self.scenarios[i]["unlearn"])
                env.simulate()
                self.envs_history.append(env)
                self.results[i, j, :] = env.results

    def plot_scenarios(self):
        legend_arr = []
        for i in range(len(self.scenarios)):
            plt.plot(self.results[i, :].mean(0))
            plt.legend([
                f"turb: {self.scenarios[i]['turb']}, max_conf: {self.scenarios[i]['max_confidence']}, "
                f"unlearn: {self.scenarios[i]['unlearn']}"],
                loc="upper left")
            plt.ylim([.4, 1])
            plt.title(f"(T={self.t}, N={self.n}, n_strategies={self.n_strategies})")

            legend_arr.append(
                f"turb: {self.scenarios[i]['turb']}, max_conf: {self.scenarios[i]['max_confidence']}, "
                f"unlearn: {self.scenarios[i]['unlearn']}")

        plt.legend(legend_arr, loc="upper left")

        plt.show()

    def get_env_strategy_dfs(self, store_res=False):
        """Time-intensive calculation."""
        df = pd.DataFrame()
        for env in self.envs_history:
            df = df.append(env.get_strategy_df())

        df.reset_index(drop=True, inplace=True)

        res_best_p = []
        res_best_guess = []

        for index, row in df[df["selected"] == 1].iterrows():
            # TODO: this loop can be inserted into env.get_strategy_df
            env_name = row["env_name"]
            t = row["t"]
            group_df = df[(df["env_name"] == env_name) & (df["t"] == t)]

            max_mean = max(group_df["mean"])
            max_p = max(group_df["p"])
            selected_mean = row["mean"]

            res_best_p.append(int(max_p == row["p"]))
            res_best_guess.append(int(max_mean == selected_mean))
        df.loc[df["selected"] == 1, "best"] = res_best_p
        df.loc[df["selected"] == 1, "best_guess"] = res_best_guess

        if store_res:
            df.to_csv("test.csv", sep=";")

        return df
