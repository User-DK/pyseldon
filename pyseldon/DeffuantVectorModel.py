"""
The Deffuant Vector Model extends the traditional Deffuant Model to multi-dimensional binary vectors. In this model, each agent’s opinion is represented as a binary vector, where each dimension of the vector can have a value of either 0 or 1. The model describes how agents adjust their binary opinions through random binary encounters, similar to the classical Deffuant approach.

Model Dynamics
--------------

Binary Opinions:
  Each opinion is represented as a binary vector, where the values are restricted to 0 or 1. The interaction and adjustment process involves comparing these vectors and updating them based on the Homophily Threshold.

Homophily Threshold:
  Agents will only adjust their opinions if the difference between their opinion vectors is below a specified threshold. This difference is computed in a way that considers the multi-dimensional nature of the opinion vectors.

The Deffuant Model provides insight into how personal interactions and opinion thresholds influence the dynamics of opinion formation and clustering within a group of agents.

Example:
---------
>>> from pyseldon import Deffuant_Vector_Model
>>> # Create the Deffuant Vector Model
>>> deffuant = Deffuant_Vector_Model(max_iterations=1000, homophily_threshold=0.2, mu=0.5)
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


class Deffuant_Vector_Model(Base_Model):
    """
    Deffuant Vector Model base class for Simulation.

    Parameters
    -----------
    max_iterations : int, default=None
      The maximum number of iterations to run the simulation. If None, the simulation runs infinitely.

    homophily_threshold : float, default=0.2
      The threshold for homophily. If the difference in opinions between two agents is less than this value, they interact.

    mu : float, default=0.5
      The convergence rate of the agents.

    use_network : bool, default=False
      For using a square lattice network. Will throw if sqrt(n_agents) is not an integer.

    dim : int, default=1
      For the multi-dimensional binary vector Deffuant model, define the number of dimensions in each opinion vector

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
        dim: int = 1,
        rng_seed: Optional[int] = None,
        agent_file: Optional[str] = None,
        network_file: Optional[str] = None,
        other_settings: Other_Settings = None,
    ):
        # Other settings and Simulation Options are already intialised in super
        super().__init__()
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
        self._options.model_settings.use_binary_vector = True
        self._options.model_settings.dim = dim

        self._simulation = seldoncore.SimulationDiscreteVectorAgent(
            options=self._options,
            cli_agent_file=agent_file,
            cli_network_file=network_file,
        )

        self._network = self._simulation.network