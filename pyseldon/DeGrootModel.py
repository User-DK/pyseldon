"""
DeGroot Model
-------------

This is the implementation of the Classical DeGroot Model in Opinion Dynamics.

The DeGroot Model is a model of social influence that describes how agents in a network update their opinions based on the opinions of their neighbors. 
The model is based on the idea that agents update their opinions by taking the average of the opinions of their neighbors. 
The model is iterative, with agents updating their opinions in each iteration based on the opinions of their neighbors.

Consider a group of Individuals(committee or team), with individuals having subjective probability distribution for some unknown value of a parameter.
This Model decribes how the group might reach agreement on a common subjective probability distribution for the parameter by pooling their individual opinions.
The model can also be applied to problems of reaching a consensus when the opinion of each member of the group is represented simply as a point estimate of the parameter rather than as a probability distribution.

Example:
---------
```python
from pyseldon import DeGrootModel

# Create the DeGroot Model
degroot = DeGrootModel(max_iterations=1000, convergence_tol=1e-6)

# Run the simulation
degroot.run("output_dir")

# Access the network
network = degroot.get_Network()

# Access the opinions of the agents
opinions = degroot.agents_opinions()

```

read also: Network, Other_Settings

Reference:
----------
    - DeGroot, Morris H. (1974). "Reaching a Consensus". Journal of the American Statistical Association. 69 (345): 118–121. doi:10.2307/2286313. JSTOR 2286313.
"""

from bindings import seldoncore
import pathlib
from typing import Optional

from ._othersettings import Other_Settings

class DeGrootModel:
  """
  DeGroot Model base class for Simulation.
  
  Parameters:
  -----------
  max_iterations : int, default=None
    The maximum number of iterations to run the simulation. If None, the simulation runs infinitely.
  
  convergence_tol : float, default=1e-6
    The tolerance for convergence of the simulation.
  
  rng_seed : int, default=None
    The seed for the random number generator. If not provided, a random seed is picked. 
  
  agent_file : str, default=None
    The file to read the agents from. If None, the agents are generated randomly.
  
  network_file : str, default=None
    The file to read the network from. If None, the network is generated randomly

  other_settings : Other_Settings, default=None
    The other settings for the simulation. If None, the default settings are used.

  Attributes:
  -----------
  Network : Network (Object)
    The network generated by the simulation.

  Opinion : Float
    The opinions of the agents or nodes of the network.

  see also: seldoncore.Network
  """
  def __init__(self,max_iterations: int=None, convergence_tol: float=1e-6, rng_seed: Optional[int]=None, agent_file: Optional[str]=None, network_file: Optional[str]=None, other_settings: Other_Settings=None):
    self.model_settings = seldoncore.DeGrootSettings()
    self.model_settings.max_iterations=max_iterations
    self.model_settings.convergence_tol=convergence_tol
    if other_settings is not None:
      self._output_settings = other_settings.output_settings
      self._network_settings = other_settings.network_settings
    else:
      self._output_settings = seldoncore.OutputSettings()
      self._network_settings = seldoncore.InitialNetworkSettings()

    self._options = seldoncore.SimulationOptions()
    self._options.model_string = "DeGroot"
    self._options.model_settings = self.model_settings
    self._options.output_settings = self._output_settings
    self._options.network_settings = self._network_settings
    self._options.model = seldoncore.Model.DeGroot

    if rng_seed is not None:
      self._options.rng_seed = rng_seed
    self._simulation = seldoncore.SimulationSimpleAgent(options = self._options, cli_agent_file = agent_file, cli_network_file = network_file)

    self.Network = self._simulation.network

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
    if output_dir is not None:
      output_path = cwd / pathlib.Path(output_dir)
      if output_path.exists():
         user_input = input("The directory already exists. Do you want to overwrite it? (y/n): ")
         if user_input.lower() != "y":
            raise Exception("Ouput Directory Exists. Simulation Terminated!!")
      print(f"Output directory path set to: {output_path}\n");
      output_path.mkdir(parents=True, exist_ok=True)
      self._simulation.run(output_dir)
      
    else:
      self._simulation.run("./output")

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
  
  def agents_opinions(self, index: int = None):
      """
      Access the agents data from the simulation.

      Parameters:
      -----------
      index : int
        The index of the agent to access. The index is 0-based. If not provided, all agents are returned.
      """
      if index is None:
          result = []
          for agent in self.Network.agent:
              result.append(agent.data.opinion)
          return result
      else:
          return self.Network.agent[index].data.opinion