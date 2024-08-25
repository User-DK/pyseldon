"""
The Deffuant Model, also known as the "Mixing of Beliefs among Interacting Agents," describes how agents update their continuous opinions through random binary encounters. In this model, agents only adjust their opinions if the difference between their opinions is below a specified threshold, known as the Homophily Threshold.

Model Dynamics
--------------
Homophily Threshold:
  If the difference in opinions between two interacting agents is less than this threshold, they will update their opinions towards each other. This process leads to opinion convergence or clustering depending on the value of the threshold.

High Thresholds:
  When the Homophily Threshold is high, opinions tend to converge towards an average opinion, as agents are more selective about whom they interact with.

Low Thresholds:
  When the Homophily Threshold is low, the model results in the formation of several distinct opinion clusters. Agents within the same cluster share similar opinions and are less influenced by agents outside their cluster.

Example:
---------
>>> from pyseldonlib import Deffuant_Model
>>> # Create the Deffuant Model
>>> deffuant = Deffuant_Model(max_iterations=1000, homophily_threshold=0.2, mu=0.5)
>>> # Run the simulation
>>> deffuant.run("output_dir")
>>> # Access the network
>>> network = deffuant.get_Network()
>>> # Access the opinions of the agents
>>> opinions = deffuant.agents_opinions()

Reference:
----------
.. bibliography::
   :style: plain

   Deffuant_2000

*************
"""

from bindings import seldoncore
import pathlib
from typing import Optional
from ._basemodel import Base_Model
from ._othersettings import Other_Settings


class Deffuant_Model(Base_Model):
    """
    Deffuant Model base class for Simulation.

    Parameters
    -----------
    max_iterations : int, default=None
      The maximum number of iterations to run the simulation. If None, the simulation runs infinitely.

    homophily_threshold : float, default=0.2
      The threshold for homophily. If the difference in opinions between two agents is less than this value, they interact.

    mu : float, default=0.5
      The convergence rate of the agents.

    use_network : bool, default=False
      For using a square lattice network. Will throw error if sqrt(n_agents) is not an integer.

    rng_seed : int, default=None
      The seed for the random number generator. If not provided, a random seed is picked.

    agent_file : str, default=None
      The file to read the agents from. If None, the agents are generated randomly.

    network_file : str, default=None
      The file to read the network from. If None, the network is generated randomly

    other_settings : Other_Settings, default=None
      The other settings for the simulation. If None, the default settings are used.

    Attributes
    -----------
    Network : Network (Object)
      The network generated by the simulation.

    Opinion : Float
      The opinions of the agents or nodes of the network.
    """

    def __init__(
        self,
        max_iterations: int = None,
        homophily_threshold: float = 0.2,
        mu: float = 0.5,
        use_network: bool = False,
        rng_seed: Optional[int] = None,
        agent_file: Optional[str] = None,
        network_file: Optional[str] = None,
        other_settings: Other_Settings = None,
    ):
        # Other settings and Simulation Options are already intialised in super
        super().__init__()
        self.other_settings = Other_Settings()
        if other_settings is not None:
            self.other_settings = other_settings

        self._options.model_string = "Deffuant"
        self._options.model_settings = seldoncore.DeffuantSettings()
        self._options.output_settings = self.other_settings.output_settings
        self._options.network_settings = self.other_settings.network_settings
        self._options.model = seldoncore.Model.DeffuantModel

        if rng_seed is not None:
            self._options.rng_seed = rng_seed

        self._options.model_settings.max_iterations = max_iterations
        self._options.model_settings.homophily_threshold = homophily_threshold
        self._options.model_settings.mu = mu
        self._options.model_settings.use_network = use_network
        self._options.model_settings.use_binary_vector = False

        self._simulation = seldoncore.SimulationSimpleAgent(
            options=self._options,
            cli_agent_file=agent_file,
            cli_network_file=network_file,
        )

        self._network = self._simulation.network
