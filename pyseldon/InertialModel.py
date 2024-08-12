"""
This is the implementation of the all inclusive Activity Driven Inertial Model for Opinion Dynamics.

"""

from bindings import seldoncore
import pathlib
from typing import Optional
from ._othersettings import Other_Settings


class Inertial_Model:
    """
    Inertial Model base class for Simulation.

    Parameters:
    -----------
    max_iterations : int, default=None
      The maximum number of iterations to run the simulation. If None, the simulation runs infinitely.

    dt : float, default=0.01
      The time step for the simulation.

    m : int, default=10
      Number of agents contacted, when the agent is active.

    eps : float, default=0.01
      The minimum activity epsilon.

    gamma : float, default=2.1
      Exponent of activity power law distribution of activities.

    alpha : float default=3.0
      Controversialness of the issue, must be greater than 0.

    homophily : float, default=0.5
      The extent to which similar agents interact with similar other.
      Example: If 0.0, agents pick their interaction partners at random.
               If 1.0, agents interact only with agents of the same opinion.

    reciprocity : float, default=0.5
      The extent to which agents reciprocate interactions.
      Example: If 0.0, agents do not reciprocate interactions.
               If 1.0, agents reciprocate all interactions.

    K : float, default=3.0
      Social interaction strength.

    mean_activities : bool, default=False
      Whether use the mean value of the powerlaw distribution for the activities of all agents.

    mean_weights : bool, default=False
      Whether use the meanfield approximation of the network edges, by default is False.

    n_bots : int, default=0
      Number of bots in the simulation.

..note:: Bots are agents that are not influenced by the opinions of other agents, but they can influence the opinions of other agents. So they have fixed opinions and different parameters, the parameters are specified in the following lists.

    bot_m : list[int], default=[]
      Value of m for the bots, If not specified, defaults to `m`.

    bot_activity : list[float], default=[],
      The list of bot activities, If not specified, defaults to 0.

    bot_opinion : list[float], default=[]
      The fixed opinions of the bots.

    bot_homophily : list[float], default=[]
      The list of bot homophily, If not specified, defaults to `homophily`.

    use_reluctances : int, default=False
      Whether use reluctances, by default is False and every agent has a reluctance of 1.

    reluctance_mean : float, default=1.0
      Mean of distribution before drawing from a truncated normal distribution.

    reluctance_sigma : float, default=0.25
      Width of normal distribution (before truncating).

    reluctance_eps : float, default=0.01
      Minimum such that the normal distribution is truncated at this value.

    covariance_factor : float, default=0.0
      Covariance Factor, defines the correlation between reluctances and activities.

    rng_seed : int, default=None
      The seed for the random number generator. If not provided, a random seed is picked.

    agent_file : str, default=None
      The file to read the agents from. If None, the agents are generated randomly.

    network_file : str, default=None
      The file to read the network from. If None, the network is generated randomly

    other_settings : Other_Settings, default=None
      The other settings for the simulation. If None, the default settings are used.

    friction_coefficient : float, default=1.0
      The friction coefficient for the inertial model.

    Attributes:
    -----------
    Network : Network (Object)
      The network generated by the simulation.

    Opinion : Float
      The opinions of the agents or nodes of the network.

    Activity : Float
      The activity of the agents or nodes of the network.

    Reluctance : Float
      The reluctance of the agents or nodes of the network.

    See Also:
    --------- 
    seldoncore.Network
    """

    def __init__(
        self,
        max_iterations: int = None,
        dt: float = 0.01,
        m: int = 10,
        eps: float = 0.01,
        gamma: float = 2.1,
        alpha: float = 3.0,
        homophily: float = 0.5,
        reciprocity: float = 0.5,
        K: float = 3.0,
        mean_activities: bool = False,
        mean_weights: bool = False,
        n_bots: int = 0,
        bot_m: list[int] = [],
        bot_activity: list[float] = [],
        bot_opinion: list[float] = [],
        bot_homophily: list[float] = [],
        use_reluctances: int = False,
        reluctance_mean: float = 1.0,
        reluctance_sigma: float = 0.25,
        reluctance_eps: float = 0.01,
        covariance_factor: float = 0.0,
        friction_coefficient: float = 1.0,
        rng_seed: Optional[int] = None,
        agent_file: Optional[str] = None,
        network_file: Optional[str] = None,
        other_settings: Other_Settings = None,
    ):
        
        self.other_settings = Other_Settings()
        if other_settings is not None:
            self.other_settings = other_settings

        self._options = seldoncore.SimulationOptions()
        self._options.model_string = "ActivityDrivenInertial"
        self._options.model_settings = seldoncore.ActivityDrivenInertialSettings()
        self._options.output_settings = self.other_settings.output_settings
        self._options.network_settings = self.other_settings.network_settings
        self._options.model = seldoncore.Model.ActivityDrivenInertial

        if rng_seed is not None:
            self._options.rng_seed = rng_seed
        
        self._options.model_settings.max_iterations = max_iterations
        self._options.model_settings.dt = dt
        self._options.model_settings.m = m
        self._options.model_settings.eps = eps
        self._options.model_settings.gamma = gamma
        self._options.model_settings.alpha = alpha
        self._options.model_settings.homophily = homophily
        self._options.model_settings.reciprocity = reciprocity
        self._options.model_settings.K = K
        self._options.model_settings.mean_activities = mean_activities
        self._options.model_settings.mean_weights = mean_weights
        self._options.model_settings.n_bots = n_bots
        self._options.model_settings.bot_m = bot_m
        self._options.model_settings.bot_activity = bot_activity
        self._options.model_settings.bot_opinion = bot_opinion
        self._options.model_settings.bot_homophily = bot_homophily
        self._options.model_settings.use_reluctances = use_reluctances
        self._options.model_settings.reluctance_mean = reluctance_mean
        self._options.model_settings.reluctance_sigma = reluctance_sigma
        self._options.model_settings.reluctance_eps = reluctance_eps
        self._options.model_settings.covariance_factor = covariance_factor
        self._options.model_settings.friction_coefficient = friction_coefficient

        self._simulation = seldoncore.SimulationInertialAgent(
            options=self._options,
            cli_agent_file=agent_file,
            cli_network_file=network_file,
        )

        self.Network = self._simulation.network

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

    def run(self, output_dir: str = None):
        """
        Run the simulation.

        Parameters:
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

        Returns:
        --------
        seldoncore.Network
          The network generated by the simulation.
        """
        return self.Network

    def agent_opinion(self, index: int = None):
        """
        Access the agents opinion data from the simulated network.

        Parameters:
        -----------
        index : int
          The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
        """
        if index is None:
            result = [agent.data.opinion for agent in self.Network.agent]
            return result
        else:
            if index < 0 or index >= self.Network.n_agents():
                raise IndexError("Agent index is out of range.")
            return self.Network.agent[index].data.opinion

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
        
        self.Network.agent[index].data.opinion = opinion

    def agent_activity(self, index: int = None):
        """
        Access the agents activity data from the simulated network.

        Parameters:
        -----------
        index : int
          The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
        """
        if index is None:
            result = [agent.data.activity for agent in self.Network.agent]
            return result
        else:
            if index < 0 or index >= self.Network.n_agents():
                raise IndexError("Agent index is out of range.")
            return self.Network.agent[index].data.activity
      
    def set_agent_activity(self, index: int, activity: float):
        """
        Set the activity of a specific agent.

        Parameters
        ----------
        index : int
            The index of the agent whose opinion is to be set.
        activity : float
            The new activity value for the agent.
        """        
        if index < 0 or index >= self.Network.n_agents():
            raise IndexError("Agent index is out of range.")
        
        self.Network.agent[index].data.activity = activity

    def agent_reluctance(self, index: int = None):
        """
        Access the agents reluctance data from the simulated network.

        Parameters:
        -----------
        index : int
          The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
        """
        if index is None:
            result = [agent.data.reluctance for agent in self.Network.agent]
            return result
        else:
            if index < 0 or index >= self.Network.n_agents():
                raise IndexError("Agent index is out of range.")
            return self.Network.agent[index].data.reluctance

    def set_agent_reluctance(self, index: int, reluctance: float):
        """
        Set the reluctance of a specific agent.

        Parameters
        ----------
        index : int
            The index of the agent whose opinion is to be set.
        reluctance : float
            The new reluctance value for the agent.
        """        
        if index < 0 or index >= self.Network.n_agents():
            raise IndexError("Agent index is out of range.")
        
        self.Network.agent[index].data.reluctance =reluctance
        
    def agent_velocity(self, index: int = None):
        """
        Access the agents reluctance data from the simulated network.

        Parameters:
        -----------
        index : int
          The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
        """
        if index is None:
            result = [agent.data.velocity for agent in self.Network.agent]
            return result
        else:
            if index < 0 or index >= self.Network.n_agents():
              raise IndexError("Agent index is out of range.")
            return self.Network.agent[index].data.velocity

    def set_agent_velocity(self, index: int, velocity: float):
        """
        Set the velocity of a specific agent.

        Parameters
        ----------
        index : int
            The index of the agent whose opinion is to be set.
        velocity : float
            The new velocity value for the agent.
        """        
        if index < 0 or index >= self.Network.n_agents():
            raise IndexError("Agent index is out of range.")
        
        self.Network.agent[index].data.velocity =velocity