"""
The Deffuant Vector Model extends the traditional Deffuant Model to multi-dimensional binary vectors. In this model, each agent’s opinion is represented as a binary vector, where each dimension of the vector can have a value of either 0 or 1. The model describes how agents adjust their binary opinions through random binary encounters, similar to the classical Deffuant approach.

Model Dynamics
~~~~~~~~~~~~~~

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
- Mixing beliefs among interacting agents. Guillaume Deffuant, David Neau, Frédéric Amblard, and Gérard Weisbuch. Advances in Complex Systems, 3(1-4):87-98, 2000. DOI: 10.1142/S0219525900000078

***
"""

from bindings import seldoncore
import pathlib
from typing import Optional

from ._othersettings import Other_Settings


class Deffuant_Vector_Model:
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
        
        self.other_settings = Other_Settings()
        if other_settings is not None:
            self.other_settings = other_settings

        self._options = seldoncore.SimulationOptions()
        self._options.model_string = "Deffuant"
        self._options.model_settings = seldoncore.DeffuantSettings()
        self._options.output_settings = self.output_settings
        self._options.network_settings = self.network_settings
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

        self.Network = self._simulation.network
    
    def run(self, output_dir: str = None):
        """
        Run the simulation.

        Parameters
        -----------
        output_dir : str, default="./output"
          The directory to output the files to.
        """
        seldoncore.validate_settings(self._options)
        seldoncore.print_settings(self._options)
        cwd = pathlib.Path.cwd()
        if output_dir is None:
            output_dir = "./output"
        output_path = cwd / pathlib.Path(output_dir)
        if output_path.exists():
          raise Exception("Output Directory already Exists!! Either delete it or change the path!!")
        print(f"Output directory path set to: {output_path}\n")
        output_path.mkdir(parents=True, exist_ok=True)
        self._simulation.run(output_dir )
        self.Network = self._simulation.network

    def print_settings(self):
        """
        Print the settings of the simulation.
        """
        seldoncore.print_settings(self._options)

    def get_Network(self):
        """
        Access the network generated by the simulation.

        Returns
        --------
        seldoncore.Network
          The network generated by the simulation.
        """
        return self.Network

    def agent_opinion(self, index: int = None):
        """
        Access the agents data from the simulation.

        Parameters
        -----------
        index : int
          The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
        """
        if index is None:
            result = [agent.data.opinion for agent in self._simulation.network.agent]
            return result
        else:
            if index < 0 or index >= self.Network.n_agents():
                raise IndexError("Agent index is out of range.")
            return self._simulation.network.agent[index].data.opinion

    def set_agent_opinion(self, index: int, opinion: float):
        """
        Set the opinion of a specific agent.

        Parameters
        ----------
        index : int
            The index of the agent whose opinion is to be set.
        opinion : float
            The new opinion value for the agent.
        """        
        if index < 0 or index >= self.Network.n_agents():
            raise IndexError("Agent index is out of range.")
        
        self._simulation.network.agent[index].data.opinion = opinion

    def __getattr__(self, name):
        if '_options' in self.__dict__ and hasattr(self.__dict__['_options'].model_settings, name):
            return getattr(self.__dict__['_options'].model_settings, name)
        elif name == "rng_seed":
            return self.__dict__['_options'].rng_seed
        elif name == "other_settings":
            return self.__dict__['other_settings']
        else:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        if '_options' in self.__dict__ and hasattr(self.__dict__['_options'].model_settings, name):
            setattr(self.__dict__['_options'].model_settings, name, value)
        elif name == "rng_seed":
            self.__dict__['_options'].rng_seed = value
        elif name == "other_settings":
            self.__dict__['other_settings'] = value
        else:
            self.__dict__[name] = value
