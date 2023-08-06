from simmeth.simulation import Simulation


def test_basic_simulation():
    env_scenarios = [
        {
            'prefix': "no_turb",
            'turb': 0,
            'max_confidence': 1,
            'unlearn': True
        }
    ]
    sim = Simulation(scenarios=env_scenarios, n_strategies=3, t=100, n=100)
    sim.run()


test_basic_simulation()
