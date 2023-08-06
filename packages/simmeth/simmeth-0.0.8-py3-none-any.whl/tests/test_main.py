from simmeth.simulation import Simulation


def test_basic_simulation():
    env_scenarios = [
        {
            'turb': 0,
            'max_confidence': 1,
            'unlearn': True
        }
    ]
    sim = Simulation(scenarios=env_scenarios, n_strategies=3, t=100, n=100)

    sim.run()

    df = sim.get_env_strategy_dfs()
    print(df.head(10))

    sim.plot_scenarios()


test_basic_simulation()
