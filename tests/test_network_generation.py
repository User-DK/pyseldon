import pyseldon.seldoncore as pd
import pytest


# Testing the network generation functions
def test_network_generation():
    buffer_n_get = []
    buffer_w_get = []

    n_agents = 3
    neigh = [0, 1, 2]
    weight = 0.25
    weights = [weight, weight, weight]

    network = pd.generate_fully_connected_degroot(
        n_agents=n_agents, weight=weight, seed=None
    )

    assert network.n_agents() == n_agents

    for i in range(0, n_agents):
        buffer_n_get = network.get_neighbours(i)
        buffer_w_get = network.get_weights(i)
        assert buffer_n_get == neigh
        assert buffer_w_get == weights
